import sqlite3

# open database
conn = sqlite3.connect('database.db')

# create table
conn.execute('''CREATE TABLE Users
            (
            userID INTEGER PRIMARY KEY,
            password TEXT,
            email TEXT,
            firstName TEXT,
            lastName TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            phone TEXT
            )''')


# Context Table
# Create Context
conn.execute('''CREATE TABLE contexts
            (
                contextID INTEGER PRIMARY KEY,
                summary TEXT,
                userID INTEGER,
                FOREIGN KEY (userID) REFERENCES Users(userID)
            )''')



# Question Table
# References Context
conn.execute('''CREATE TABLE questions
            (
                questionID INTEGER PRIMARY KEY,
                text TEXT,
                contextID INTEGER,
                FOREIGN KEY (contextID) REFERENCES contexts(contextID)
            )''')


# Answer Table
# References Question
conn.execute('''CREATE TABLE answers 
            (
                answerID INTEGER PRIMARY KEY,
                text TEXT,
                questionID INTEGER,
                FOREIGN KEY (questionID) REFERENCES questions(questionID)
            )''')


conn.close()