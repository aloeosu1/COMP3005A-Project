"""
    Michael Han
    101157504
    COMP3005A
    Final Project V2


    member.py
    
    member related classes and functions

    connectToDatabase()
    register()
    registerToDB()
    login()
    printInfo()
    update()
    viewMetrics()
    scheduleSession()
    viewSessions()
    viewExercises()
    addExercise()
"""

import psycopg2
from psycopg2 import sql
from datetime import date, datetime
import os

class Admin:

    def __init__(self, adminID, firstName, lastName, email, password):
        self.adminID = adminID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password


def connectToDatabase():
    """
        This function connects this Python script to the PostgreSQL database
    """
    try:
        database = psycopg2.connect(
            dbname = "GravelerGrittyGym",
            user = "postgres",
            password = "lmaoturtles1",
            host = "localhost",
            port = "5432"
        )
        return database

    except:
        print("Connection failed D:\n")



def registerAdmin():
    """
        This function acts as a registration form. It prompts the user for information, will ask user to double check information,
        and calls registerToAdminDB if all information is correct
    """
    print("Admin registration: \n")

    correct = "no"

    while(correct == "no"):
        #getting member info
        firstName = input('First Name: ')
        lastName = input('Last Name: ')
        email = input('Email: ')
        password = input('Password: ')
        
        

        print(
        "\n",
        "First Name:", firstName, "\n",
        "Last Name:", lastName, "\n",
        "Email:", email, "\n",
        "Password:", password, "\n", 
        
        )

        correct = input('Is the information provided correct? (yes/no): ')
    
    #if all information is correct, then add member to database
    registerAdminToDB(firstName, lastName, email, password)

def registerAdminToDB(firstName, lastName, email, password):
    """
        This function registers admins to the database. Same logic as member registerToDB function
    """
    try:
        database = connectToDatabase()
        cursor = database.cursor()

        #insert new Member into table
        cursor.execute("INSERT INTO Admins (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)", 
                            (firstName, lastName, email, password))
            
        database.commit()

        print("You're registered! \n")

        #closes connection
        cursor.close()
        database.close()

    except:
        print("Oops! An error occured D: \n")
        database.rollback()

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

def login():
    """
        This function lets the user login if they give the email of an existing account and the correct password.
        It first checks if the email belongs to a admin in the database, and if so, it will retrieve the password for that user,
        and ask the user to enter their password. If the password matches the password associated with the account, 
        they will log in successfully.
        The function will then retrieve all attributes for that admin, and make a new Admin object, and return it to adminMain.
        Same logic as login() for members
    """
    try:
        
        print("Admin Login: ")

        database = connectToDatabase()
        cursor = database.cursor()

        #prompts user for email
        email = input("Email: ")

        #looks for user with the email given
        cursor.execute("SELECT * FROM Admins WHERE Email = %s;", (email,))
        trainer = cursor.fetchone()
        

        #if admin with given email is found
        if trainer:
            print("Member found")
            #gets trainer's password
            cursor.execute("SELECT Password FROM Admins WHERE Email = %s;", (email,))
            correctPwd = cursor.fetchone()
            #print(correctPwd)

            #3 times for login attempt
            for i in range(3):
                #asks user for password
                password = input("Password: ")

                #if user's password matches password associated with email
                #correctPwd = ('password',) so correctPwd[0] = password
                if password == correctPwd[0]:
                    #print("Logged in successfully!")

                    
                    #getting all attributes
                    #trainerID 
                    cursor.execute("SELECT AdminID FROM Trainers WHERE Email = %s", (email,))
                    adminID = cursor.fetchone()[0]

                    
                    #first name
                    cursor.execute("SELECT FirstName FROM Admins WHERE Email = %s", (email,))
                    firstName = cursor.fetchone()[0]
                    

                    #last name
                    cursor.execute("SELECT LastName FROM Admins WHERE Email = %s", (email,))
                    lastName = cursor.fetchone()[0]
                    

                

                    

                    


                    #making admin object 
                    currAdmin = Admin(adminID, firstName, lastName, email, password)
                    
                    return currAdmin
                    
                    

                #if password is incorrect
                else:
                    print("Incorrect Password")
                    

            #if user reaches maximum number of incorrect attempts (3)
            else:
                print("You have exceeded the maximum number of attempts. Please try again later.")
                

        #if email is not found within database
        else:
            print("This email is not tied to any existing account")

        #closes connection
        cursor.close()
        database.close()

        
        

    except:
        print("Oops! An error occured in login: \n")
        

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

