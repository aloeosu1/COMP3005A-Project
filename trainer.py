"""
    Michael Han
    101157504
    COMP3005A
    Final Project V2


    trainer.py
    
    trainer related classes and functions

    connectToDatabase()
    registerTrainer()
    registerTrainerToDB()
    login()
    viewMember()
    setAvail()
    checkAvail()
    viewSessions()


"""

import psycopg2
from psycopg2 import sql
from datetime import date, datetime
import os
import member


class Trainer:

    def __init__(self, trainerID, firstName, lastName, email, password, availTime, startDate):
        self.trainerID = trainerID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.availTime = availTime
        self.startDate = startDate


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


def registerTrainer():
    """
        This function acts as a registration form. It prompts the user for information, will ask user to double check information,
        and calls registerToTrainerDB if all information is correct
    """
    print("Trainer registration: \n")

    correct = "no"

    while(correct == "no"):
        #getting member info
        firstName = input('First Name: ')
        lastName = input('Last Name: ')
        email = input('Email: ')
        password = input('Password: ')
        availTime = input("Available time (hh:mm:ss): ")
        startDate = date.today()
        

        print(
        "\n",
        "First Name:", firstName, "\n",
        "Last Name:", lastName, "\n",
        "Email:", email, "\n",
        "Password:", password, "\n", 
        "Available Time:", availTime, "\n"
        "Start Date:", startDate, "\n",
        )

        correct = input('Is the information provided correct? (yes/no): ')
    
    #if all information is correct, then add member to database
    registerTrainerToDB(firstName, lastName, email, password, availTime, startDate)

def registerTrainerToDB(firstName, lastName, email, password, availTime, startDate):
    """
        This function registers trainers to the database. Same logic as member registerToDB function
    """
    try:
        database = connectToDatabase()
        cursor = database.cursor()

        #insert new Member into table
        cursor.execute("INSERT INTO Trainers (FirstName, LastName, Email, Password, AvailTime, StartDate) VALUES (%s, %s, %s, %s, %s, %s)", 
                            (firstName, lastName, email, password, availTime, startDate))
            
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
        It first checks if the email belongs to a trainer in the database, and if so, it will retrieve the password for that user,
        and ask the user to enter their password. If the password matches the password associated with the account, 
        they will log in successfully.
        The function will then retrieve all attributes for that trainer, and make a new Trainer object, and return it to trainerMain.
        Same logic as login() for members
    """
    try:
        
        print("Trainer Login: ")

        database = connectToDatabase()
        cursor = database.cursor()

        #prompts user for email
        email = input("Email: ")

        #looks for user with the email given
        cursor.execute("SELECT * FROM Trainers WHERE Email = %s;", (email,))
        trainer = cursor.fetchone()
        

        #if trainer with given email is found
        if trainer:
            print("Member found")
            #gets trainer's password
            cursor.execute("SELECT Password FROM Trainers WHERE Email = %s;", (email,))
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
                    cursor.execute("SELECT TrainerID FROM Trainers WHERE Email = %s", (email,))
                    trainerID = cursor.fetchone()[0]

                    
                    #first name
                    cursor.execute("SELECT FirstName FROM Trainers WHERE Email = %s", (email,))
                    firstName = cursor.fetchone()[0]
                    

                    #last name
                    cursor.execute("SELECT LastName FROM Trainers WHERE Email = %s", (email,))
                    lastName = cursor.fetchone()[0]
                    

                    cursor.execute("SELECT AvailTime FROM Trainers WHERE Email = %s", (email,))
                    availTime = cursor.fetchone()[0]


                    
                    #start
                    cursor.execute("SELECT StartDate FROM Trainers WHERE Email = %s;", (email,))
                    startDate = cursor.fetchone()[0]

                    

                    


                    #making Trainer object 
                    currTrainer = Trainer(trainerID, firstName, lastName, email, password, availTime, startDate)
                    
                    return currTrainer
                    
                    

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


def viewMember():
    """
        This function prompts the trainer for the full name of the member they are trying to view
        This function then splits the input into first and last name, then prints out the member with the
        matching first and last name if found.
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()
       

        memberName = input("Which member are you looking for? Please give first and last name:")
        #splits name into first and last
        firstName, lastName = memberName.split()

        #capitalizes first letter of names
        firstName = firstName.capitalize()
        lastName = lastName.capitalize()

        #selecting a member with matching first and last names
        cursor.execute("SELECT * FROM Members WHERE FirstName = %s AND LastName = %s;", (firstName, lastName, ))
        member = cursor.fetchone()

        #prints info from current member if found
        if member:
            print("Member ID:", member[0])
            print("Name:", (member[1] + " " + member[2]))
            print("Email:", member[3])
            print("Phone Number:", member[5])
            print("Birthday:", member[6])
            print("Gender:", member[7])
            print("Address:", member[8])
            print("Fitness Goal:", member[9])
            print("Registration date:", member[10])
            print("Payment Method:", member[11])
            member.viewMetrics(member)
            print("\n")
            
            input("Press Enter to continue...")
            

        #if no matching MemberID is found
        else:
            print("Member not found")
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured in viewMember\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

def setAvail(trainer1):
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #asks trainer when he is available
        day = input("What day are you available (yyyy-mm-dd)? ")
        time = input("What time are you available on that day (hh:mm:ss)? ")

        #insert into availability table when trainer1 is available
        cursor.execute("INSERT INTO Available (TrainerID, Day, Time) VALUES (%s, %s, %s);", (trainer1.trainerID, day, time))
        database.commit()
        
        print("Availablity Updated!")
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured setting availability\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

def checkAvail(trainer1):
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #insert into availability table when trainer1 is available
        cursor.execute("SELECT * FROM Available WHERE TrainerID = %s", (trainer1.trainerID,))
        available = cursor.fetchall()
        if(available):
            for days in available:
                print(days)

        else:
            print("No availability")
        
       
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured checking availability\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()


def viewSessions(trainer1):
    """
        This function prints out all sessions trainer1 has
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()
       

        cursor.execute("SELECT * FROM Sessions WHERE TrainerID = %s;", (trainer1.trainerID,))
        sessions = cursor.fetchall()

        if(sessions):
            for session in sessions:
                print(session)
        else:
            print("You have no sessions booked at the moment")
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured viewing sessions\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()



def listMembers():
    """
    This function prints out all members currently in database
    """

    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()
        #gets all members from table in database
        cursor.execute("SELECT * FROM Members;")
        members = cursor.fetchall()

        #prints all members in Members table
        for member in members:
            print(list(member))
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()
        




def trainerMain():
    """
        The main function for trainers
    """

    #setting blank ans
    ans = ""
    #initally not logged in
    loggedIn = False

    #while user doesn't want to exit
    while(ans!='exit'):

            
        #if the user is not logged in
        if(not(loggedIn)):
            print("Graveler's Gritty Gymu!\n")
            print("Hello Trainer! What would you like to do?\n")
            print("Log In")
            print("Register")
            print("Exit")
            ans = input().lower()

            if(ans == "login" or ans == "log in"):
                os.system('cls' if os.name == 'nt' else 'clear')
                trainer1 = login()
                if trainer1:
                    print("Logged in successfully")
                    loggedIn = True
                    

            elif(ans == "register" or ans == "sign up"):
                os.system('cls' if os.name == 'nt' else 'clear')
                registerTrainer()

            elif(ans == "exit"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("See you next time!")
                break

            else:
                    
                print("That's not an option.")

        #if the user is logged in
        else:
            print("Hello Trainer ", trainer1.firstName, "!")
            print("What would you like to do?\n")
            print("Manage availability")
            print("View member")
            print("List members")
            print("Exit")
            ans = input().lower()

            if(ans == "login" or ans == "log in"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Your already logged in!")

            elif(ans == "register" or ans == "sign up"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Your already logged in! Please start new session to register")

            #manage availability
            elif(ans == "availability" or ans == "available"):
                os.system('cls' if os.name == 'nt' else 'clear')
                do = input("What do you want to do with your availability?")

                if(do == "check"):
                    checkAvail(trainer1)
                
                elif(do == "set"):
                    setAvail(trainer1)

                else:
                    print("Unknown command")

            #check schedule
            elif(ans == "schedule"):
                
                viewSessions(trainer1)
                


            #view member
            elif(ans == "view" or ans == "view member"):
                os.system('cls' if os.name == 'nt' else 'clear')
                viewMember()

            elif(ans == "list" or ans == "list members"):
                os.system('cls' if os.name == 'nt' else 'clear')
                listMembers()

            elif(ans == "exit"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("See you next time!")
                break

            else:
                print("That is not an option.")