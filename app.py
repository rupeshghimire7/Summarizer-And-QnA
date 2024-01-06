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




@app.route('/')
def home():
    






if __name__ == '__main__':
    app.run(debug=True)