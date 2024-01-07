from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






## ------------------------------------------------------------------------------------
###  ---------------------------------------ALL ROUTES------------------------------------
## ------------------------------------------------------------------------------------

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            userID = None
        else:
            loggedIn = True
            cur.execute("SELECT userID, firstName FROM Users WHERE email = ?", (session['email'], ))
            userID, firstName = cur.fetchone()
    conn.close()
    return (loggedIn, userID, firstName)




# --------------------------------------------------------------------------------------------------
# -------------------------------------- HOME PAGE --------------------------------------------------

## Load Home page and Lead user if logged in, to summarizer and qna page else, to login or register page
@app.route('/')
def home():
    loggedIn, userID, firstName = getLoginDetails()
    
    if loggedIn == True:
        url1 = '/summarizer'
        url2 = '/qna'
    else:
        url1 = '/loginForm'
        url2 = '/registrationForm'

    return render_template('home.html', loggedIn=loggedIn, url1=url1, url2=url2)




# --------------------------------------------------------------------------------------------------
# -------------------------------------- USER LOGIN  -----------------------------------------------

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect('/')
    else:
        return render_template('login.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect('/')
        else:
            error = 'Invalid UserID / Password'
            return render_template('login.html', error=error)


def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM Users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False




# --------------------------------------------------------------------------------------------------
# -------------------------------------- USER REGISTRATION -----------------------------------------



@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO Users (password, email, firstName, lastName, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registrationForm")
def registrationForm():
    return render_template("register.html")




# --------------------------------------------------------------------------------------------------
# --------------------------------------  Profile, Updates and Change Password ----------------------

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect('/')
    loggedIn, userID, firstName = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, city, state, country, phone FROM Users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    return render_template("profileHome.html", profileData=profileData, loggedIn=loggedIn, userID=userID, firstName=firstName)



@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect('/')
    loggedIn, _, firstName = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, city, state, country, phone FROM Users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName)


@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    if 'email' not in session:
        return redirect('/')
    if request.method == 'POST':
        loggedIn, userID, firstName = getLoginDetails()
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE Users SET firstName=?, lastName=?, city=?, state=?, country=?, phone=? where email=?",(firstName, lastName, city, state, country, phone, email))
                conn.commit()  
                msg="Profile Updated Successfully."
            except:
                conn.rollback
                msg="Couldn't update profile."
                return render_template("editProfile.html",msg=msg)
        
        cur.execute("SELECT userId, email, firstName, lastName, city, state, country, phone FROM Users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
        conn.close()

        return render_template('profileHome.html', profileData=profileData, msg=msg, loggedIn=loggedIn)
            


@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM Users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE Users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")



# --------------------------------------------------------------------------------------------------
# --------------------------------------  Logout -----------------------------------------------


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))
    
# --------------------------------------------------------------------------------------------------
# --------------------------------------  Summarizer -----------------------------------------------

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    pass




# --------------------------------------------------------------------------------------------------
# --------------------------------------  Summarizer -----------------------------------------------

@app.route('/qna', methods=['GET', 'POST'])
def qna():
    pass





if __name__ == '__main__':
    app.run(debug=True)