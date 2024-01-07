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
        url2 = '/registrarionForm'

    return render_template('home.html', loggedIn=loggedIn, url1=url1, url2=url2)




# --------------------------------------------------------------------------------------------------
# -------------------------------------- USER LOGIN  -----------------------------------------------

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('/'))
    else:
        return render_template('login.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('/'))
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
                cur.execute('INSERT INTO users (password, email, firstName, lastName, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, city, state, country, phone))

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







    







if __name__ == '__main__':
    app.run(debug=True)