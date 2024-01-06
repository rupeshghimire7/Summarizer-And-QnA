from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






## ------------------------------------------------------------------------------------
###  ---------------------------------------ROUTES------------------------------------

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


@app.route('/')
def home():
    loggedIn, userID, firstName = getLoginDetails()

    return render_template('home.html', loggedIn=loggedIn, userID=userID, firstName=firstName)

    







if __name__ == '__main__':
    app.run(debug=True)