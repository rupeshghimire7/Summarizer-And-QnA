from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

from ML_models.qna import inference_model_qna
from ML_models.summarizer import inference_model_summarize

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
        url1 = '/summarizerForm'
        url2 = '/qnaForm'
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
        if len(password) < 8:
            return render_template('register.html', msg="Password Length Should Be Minimum 8 Characters.")
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO Users (password, email, firstName, lastName, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, city, state, country, phone))

                conn.commit()

                msg = "Registered Successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return render_template("login.html", msg=msg)

@app.route("/registrationForm")
def registrationForm():
    return render_template("register.html")




# --------------------------------------------------------------------------------------------------
# --------------------------------------  Profile, Updates and Change Password ----------------------

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect('/loginForm')
    loggedIn, userID, firstName = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, city, state, country, phone FROM Users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    return render_template("profileHome.html", profileData=profileData, loggedIn=loggedIn, userID=userID, firstName=firstName,logo="../")



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
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, logo="../../")


@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    if 'email' not in session:
        return redirect('/')
    if request.method == 'POST':
        loggedIn, _, _ = getLoginDetails()
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
                msg="Changed successfully"
            except:
                conn.rollback
                msg="Couldn't update profile."
                return render_template("editProfile.html",msg=msg)
        
        cur.execute("SELECT userId, email, firstName, lastName, city, state, country, phone FROM Users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
        conn.close()

        return render_template('profileHome.html', profileData=profileData, msg=msg, loggedIn=loggedIn,logo="../../")
            


@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn,_, firstName = getLoginDetails()
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        if len(newPassword) < 8:
            return render_template('changePassword.html', msg="Password Length Should Be Minimum 8 Characters.")
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
                    return redirect('/')
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg,logo="../../")
            else:
                msg = "Wrong password"
        conn.close()

        return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, firstName=firstName,logo="../../" )
    else:
        return render_template("changePassword.html", loggedIn=loggedIn, firstName=firstName,logo="../../")



# --------------------------------------------------------------------------------------------------
# --------------------------------------  Logout -----------------------------------------------


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))
    
# --------------------------------------------------------------------------------------------------
# --------------------------------------  Summarizer -----------------------------------------------

@app.route("/summarizerForm")
def summarizerForm():
    return render_template("summarize.html")


@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    loggedIn, userID, _ = getLoginDetails()
    if not loggedIn:
        return url_for('home')
    
    if request.method == "POST":

        context = request.form['context']
        summary = inference_model_summarize(context)
        summary = summary[0]['summary_text']

        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO contexts (context, summary, userID) VALUES (?,?,?)', (context, summary, userID))
                conn.commit()
            except:
                conn.rollback()

        conn.close()
        return render_template('summarize.html', context=context, summary=summary)
    
    else:
        return render_template('summarize.html')




# --------------------------------------------------------------------------------------------------
# --------------------------------------  QnA ------------------------------------------------------

@app.route("/qnaForm")
def qnaForm():
    return render_template("qna.html")

@app.route('/qna', methods=['GET', 'POST'])
def qna():
    loggedIn, userID, _ = getLoginDetails()
    if not loggedIn:
        return url_for('home')

    if request.method == "POST":

        context = request.form['context']
        question = request.form['question']

        answer = inference_model_qna(question, context)
        answer = answer['answer']

        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                # Add context to database
                cur.execute("INSERT INTO contexts (context, userID) VALUES (?, ?)",(context,userID))
                conn.commit()

                # Get context id
                cur.execute("SELECT contextID FROM contexts WHERE context=?",(context))
                contextID = cur.fetchone()

                # add question to database
                cur.execute("INSERT INTO questions (text, contextID) VALUES (?, ?)",(question,contextID))
                conn.commit()

                # Get question id
                cur.execute("SELECT questionID FROM contexts WHERE text=?",(question))
                questionID = cur.fetchone()

                # add answer to database
                cur.execute("INSERT INTO answers (text, questionID) VALUES (?, ?)",(answer,questionID))
                conn.commit()

            except:
                conn.rollback()

        conn.close()
        return render_template('qna.html', context=context, question=question, answer=answer)
    
    else:
        return render_template('qna.html')
    

# --------------------------------------------------------------------------------------------------
# --------------------------------------  About Page ----------------------------------------------
@app.route('/about', methods=["GET"])
def about():
    loggedIn,_,_ = getLoginDetails()
    if loggedIn == True:
        url1 = '/summarizerForm'
        url2 = '/qnaForm'
    else:
        url1 = '/loginForm'
        url2 = '/registrationForm'
    return render_template('about.html', url1=url1, url2=url2)



# --------------------------------------------------------------------------------------------------
# --------------------------------------  Contact Page ----------------------------------------------
@app.route('/contact', methods=["GET"])
def contact():
    loggedIn,_,_ = getLoginDetails()
    if loggedIn == True:
        url1 = '/summarizerForm'
        url2 = '/qnaForm'
    else:
        url1 = '/loginForm'
        url2 = '/registrationForm'
    return render_template('contact.html', url1=url1, url2=url2)








if __name__ == '__main__':
    app.run(debug=True)