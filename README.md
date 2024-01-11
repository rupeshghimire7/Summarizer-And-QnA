# Summarization and QnA


Your Gateway to AI-Powered Brilliance, Crafting Data Narratives One Insight at a Time!🚀


Welcome to the Summarization and QnA Flask App! This application leverages the power of T5-Base for text summarization and deepset/roberta-base-squad2 for question-answering capabilities. Whether you need to generate concise summaries or obtain answers to specific questions, this app has you covered.




## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Database](#database)
5. [License](#license)




## Features

### 1. User Authentication


- **User Login:** Secure user login functionality.

  
  ![Login](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/LoginPage.jpg)
 
    
- **User Register:** New users can create an account.

  
  ![Register](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/RegisterPage.jpg)

  
- **User Profile View:** View and access user profiles.


  ![Profile View](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/UserProfile.jpg)


- **Profile Edit:** Users can modify their profile details.


  ![Profile Edit](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/EditProfile.jpg)


- **Change Password:** Securely update the password.


  ![Change Password](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/ChangePassword.jpg)




 
### 2. Home, About and Contact:


- **Home Page:** Depending on user authentication status, the home page provides links to either the summarization and QnA features or login and register pages.
  
  
  ![Home](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/HomePage.jpg)
  
  ![Home](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/HomePage2.jpg)



 
-  **Contact Page:** Means to contact me.

    ![Contact](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/ContactPage.jpg)



-  **About Page:** Something about me and this project.

    ![Contact](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/AboutPage.jpg)



### 3. Summarizer


- **Model**: T5-Base model is utilized for summarization task. The implementation is made simple by using the transformers pipeline from HuggingFace.

    ![Summarizer Form](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/SummaryForm.jpg)


    ![Summarized](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/Summary.jpg)


### 4. QnA

- **Model**: Roberta-Base model from deepset trained on squad2 dataset is utilized for QnA task where model answers the question based on provided user context. The implementation is made simple by using the transformers pipeline from HuggingFace.

    ![QnA Form](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/QnAForm.jpg)


    ![QnA](https://github.com/rupeshghimire7/Summarizer-And-QnA/blob/main/Results/QnA.jpg)




## Getting Started

### 1. Clone the repository:
    
    git clone git@github.com:rupeshghimire7/Summarizer-And-QnA.git
    cd your-Summarizer-And-QnA
    



### 2. Create Python Virtual Environment

      python3 -m venv your-env-name
      source your-env-name/bin/activate
      


### 3. Install dependencies:

    pip install -r requirements.txt


### 4. Create Database:

    python3 database.py


### 5. Run the Flask app:

    python3 app.py


### 6. Access the app
  
  Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the app.




## Usage

- Navigate to the home page.

  
- If logged in, use the provided links for summarization and QnA.

  
- If not logged in, use the links to access the login and register pages.

  
- Follow the instructions on each page for input and interaction.

  
  
  


## Database
This app utilizes SQLite3 as the database, and Raw SQL queries are used to perform all database-related tasks such as INSERT into, UPDATE from, Select from tables of database.





## License
This project is licensed under the [MIT License](LICENSE).






  


  






