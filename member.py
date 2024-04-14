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


class Member:
    #__init__
    def __init__(self, memberID, firstName, lastName, email, password, address, phoneNum, birthday, gender, goals, regDate, payment):
        self.memberID = memberID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.address = address
        self.phoneNum = phoneNum
        self.birthday = birthday
        self.gender = gender
        self.goals = goals
        self.regDate = regDate
        self.payment = payment


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


def register():
    """
        This function acts as a registration form. It prompts the user for information, will ask user to double check information,
        and calls registerToDB if all information is correct
    """
    print("Welcome to Graveler's Gritty Gymu. Please fill out the registration form below: \n")

    correct = "no"

    while(correct == "no"):
        #getting member info
        firstName = input('First Name: ')
        lastName = input('Last Name: ')
        email = input('Email: ')
        password = input('Password: ')
        phoneNum = input('Phone Number: ')
        birthday = input('Birthday (YYYY-MM-DD): ')
        gender = input('Gender (M / F): ')
        address = input('Address: ')
        goal = input('Fitness Goals (255 characters): ')
        regDate = date.today()
        paymentMethod = input('Method of payment: ')

        print(
        "\n",
        "First Name:", firstName, "\n",
        "Last Name:", lastName, "\n",
        "Email:", email, "\n",
        "Password:", password, "\n",
        "Phone Number:", phoneNum, "\n",
        "Birthday:", birthday, "\n",
        "Gender:", gender, "\n",
        "Address:", address, "\n",
        "Fitness Goals:", goal, "\n",
        "Registration Date:", regDate, "\n",
        "Method of payment:", paymentMethod, "\n",
        )

        correct = input('Is the information provided correct? (yes/no): ')
    
    #if all information is correct, then add member to database
    registerToDB(firstName, lastName, email, password, phoneNum, birthday, gender, address, goal, regDate, paymentMethod)


def registerToDB(firstName, lastName, email, password, phoneNum, birthday, gender, address, goal, regDate, paymentMethod):
    """
        This function updates the database with the new member from register()
    """

    try:
        database = connectToDatabase()
        cursor = database.cursor()

        #insert new Member into table
        cursor.execute("INSERT INTO Members (FirstName, LastName, Email, Password, Phone, Birthday, Gender, Address, Goal, RegistrationDate, PaymentMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (firstName, lastName, email, password, phoneNum, birthday, gender, address, goal, regDate, paymentMethod))
        
        database.commit()

        print("You're registered! \n")

        
        #getting memberID for Metrics
        cursor.execute("SELECT MemberID FROM Members WHERE Email = %s", (email,))

        memberID = cursor.fetchone()

        #asking user for height and weight
        height = input("How tall are you (cm): ")
        weight = input("How much do you weight (lbs): ")

        #initialize metrics
        cursor.execute("INSERT INTO Metrics (MemberID, Height, Weight) VALUES (%s, %s, %s);", (memberID, height, weight))
        database.commit()

        
        print("All done!")
        
        

        

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
        It first checks if the email belongs to a user in the database, and if so, it will retrieve the password for that user,
        and ask the user to enter their password. If the password matches the password associated with the account, 
        they will log in successfully.
        The function will then retrieve all attributes for that member, and make a new Member object, and return it to memberMain.
    """
    try:
        
        print("Login: ")

        database = connectToDatabase()
        cursor = database.cursor()

        #prompts user for email
        email = input("Email: ")

        #looks for user with the email given
        cursor.execute("SELECT * FROM Members WHERE Email = %s;", (email,))
        member = cursor.fetchone()
        

        #if member with given email is found
        if member:
            print("Member found")
            #gets member's password
            cursor.execute("SELECT Password FROM Members WHERE Email = %s;", (email,))
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
                    #memberID 
                    cursor.execute("SELECT MemberID FROM Members WHERE Email = %s", (email,))
                    memberID = cursor.fetchone()[0]

                    
                    #first name
                    cursor.execute("SELECT FirstName FROM Members WHERE Email = %s;", (email,))
                    firstName = cursor.fetchone()[0]
                    

                    #last name
                    cursor.execute("SELECT LastName FROM Members WHERE Email = %s", (email,))
                    lastName = cursor.fetchone()[0]
                    


                    #address
                    cursor.execute("SELECT Address FROM Members WHERE Email = %s;", (email,))
                    address = cursor.fetchone()[0]
                   

                    #phoneNum
                    cursor.execute("SELECT Phone FROM Members WHERE Email = %s", (email,))
                    phoneNum = cursor.fetchone()[0]
                    

                    #birthday
                    cursor.execute("SELECT Birthday FROM Members WHERE Email = %s;", (email,))
                    birthday = cursor.fetchone()[0]
                    

                    #gender
                    cursor.execute("SELECT Gender FROM Members WHERE Email = %s", (email,))
                    gender = cursor.fetchone()[0]

                    #goals
                    cursor.execute("SELECT Goal FROM Members WHERE Email = %s;", (email,))
                    goals = cursor.fetchone()[0]

                    #regDate
                    cursor.execute("SELECT RegistrationDate FROM Members WHERE Email = %s;", (email,))
                    regDate = cursor.fetchone()[0]

                    #payment
                    cursor.execute("SELECT PaymentMethod FROM Members WHERE Email = %s;", (email,))
                    payment = cursor.fetchone()[0]

                    


                    #making Member object 
                    currMember = Member(memberID, firstName, lastName, email, password, address, phoneNum, birthday, gender, goals, regDate, payment)
                    
                    return currMember
                    
                    

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

        

def printInfo(member1):
    """
        This function takes a Member object as an arguement. It takes the memberID of the object,
        finds the member in the database with the matching ID, and prints out the attributes
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()
        #gets all members from table in database
        cursor.execute("SELECT * FROM Members WHERE MemberID = %s;", (member1.memberID,))
        member = cursor.fetchone()

        #prints info from current member if found
        if member:
            print("Your ID:", member[0])
            print("Name:", (member[1] + " " + member[2]))
            print("Email:", member[3])
            print("Phone Number:", member[5])
            print("Birthday:", member[6])
            print("Gender:", member[7])
            print("Address:", member[8])
            print("Fitness Goal:", member[9])
            print("Registration date:", member[10])
            print("Payment Method:", member[11])
            viewMetrics(member1)
            print("\n")
            
            input("Press Enter to continue...")
            

        #if no matching MemberID is found
        else:
            print("Member not found")
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured in printInfo\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

def update(member1):
    """
        This function asks the user what they want to update. The user is then asked what they want it to be updated to
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #gets attribute the user wants to update
        attribute = input("What would you like to update? ")

        if(attribute == "firstname"):
            newInfo = input("What do you want to update it to? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET FirstName = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.firstName = newInfo
            print("Successfully updated!")

        elif(attribute == "lastName"):
            newInfo = input("What do you want to update it to? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET LastName = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.lastName = newInfo
            print("Successfully updated!")

        elif(attribute == "password"):
            newInfo = input("What is your new password? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET Password = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.password = newInfo
            print("Successfully updated!")


        elif(attribute == "email"):
            newInfo = input("What is the new email? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET Email = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.email = newInfo
            print("Successfully updated!")


        elif(attribute == "phone"):
            newInfo = input("What is the new phone number? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET Phone = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.phoneNum = newInfo
            print("Successfully updated!")


        elif(attribute == "address"):
            newInfo = input("What is your new address? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET Address = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.address = newInfo
            print("Successfully updated!")

        elif(attribute == "goals"):
            newInfo = input("What are your new goals? ")
            #updates the database and Member object
            cursor.execute("UPDATE Members SET Goal = %s WHERE MemberID = %s;", (newInfo, member1.memberID))
            database.commit()
            member1.goals = newInfo
            print("Successfully updated!")


        elif(attribute == "metrics"):
            metricType = input("Which metric would you like to update? ")
            if(metricType == "height"):
                newInfo = input("What is your new height? ")
                
                cursor.execute("UPDATE Metrics SET Height = %s  WHERE MemberID = %s", (newInfo, member1.memberID))
                database.commit()
                print("Successfully updated!")
            elif(metricType == "weight"):
                newInfo = input("What is your new weight? ")
                cursor.execute("UPDATE Metrics SET Weight = %s WHERE MemberID = %s", (newInfo, member1.memberID))
                database.commit()
                print("Successfully updated!")
        else:
            print("Not an attribute")


        

        cursor.close()
        database.close()

    except:
        print("Could not update D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()


def viewMetrics(member1):
    """
        This function finds the metrics with the matching MemberID and prints it
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #print("Selecting")
        cursor.execute("SELECT Height, Weight FROM Metrics WHERE MemberID = %s;", (member1.memberID,))
        #print("Selected")

        metrics = cursor.fetchone()

        if metrics:
            height, weight = metrics
            print("Your metrics: ")
            print("Height: ", height, "cm")
            print("Weight: ", weight, "lbs")

        else:
            print("No metrics found.")

        cursor.close()
        database.close()

    except:
        
        print("Error getting metrics D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()


def scheduleSession(member1):
    """
        This function allows the member to set a day and time for their session, and if their is a trainer available at that time,
        the session is created, and the availability of that trainer at that time is deleted
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()
       
        
        sessionDate = input("What day is this session (yyyy-mm-dd): ")
        sessionTime = input("When is this session (hh:mm:ss): ")

        #checking trainer availability

        cursor.execute("SELECT TrainerID FROM Available WHERE Day = %s AND Time = %s;", (sessionDate, sessionTime))
        avail = cursor.fetchone()
        
        #if someone is available
        if(avail):
            trainerID = avail[0]
            print("A trainer is available!")
            cursor.execute("INSERT INTO Sessions (MemberID, TrainerID, SessionName, SessionCost, SessionDate, SessionTime) VALUES (%s, %s, %s, %s, %s, %s)", (member1.memberID, trainerID, member1.firstName, '20', sessionDate, sessionTime))
            database.commit()

            print("Session created!")

            #deleting that availablity
            cursor.execute("DELETE FROM Available WHERE Day = %s AND Time = %s AND TrainerID = %s", (sessionDate, sessionTime, trainerID))
            database.commit()
            print("That time is now longer available")

        #if no availablity is found
        else:
            print("No one is available on that day at that time")
        
        
        cursor.close()
        database.close()
    
    except:
        print("An error has occured creating this session\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()




def cancelSession(member1):
    """
        This function allows the member to cancel their scheduled session
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #looking for sessions with NULL MemberIDs (where there are no members registered)
        cursor.execute("SELECT * FROM Sessions Where MemberID = %s", (member1.memberID,))
        
        #get all of them with NULL MemberID
        bookedSessions = cursor.fetchall()

        #if there are any
        if bookedSessions:
            ans = ""
            #print each session
            for session in bookedSessions:
                print(session)

            #while user does not wanna quit
            

            
            cursor.close()
            database.close()



        else:
            print("No available sessions found.")

        cursor.close()
        database.close()

    except:
        
        print("Error getting sessions D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()


def viewSessions(member1):
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #looking for sessions with member1.memberID
        cursor.execute("SELECT * FROM Sessions Where MemberID = %s", (member1.memberID,))
        
        sessions = cursor.fetchall()

        #if there are sessions
        if(sessions):
            for session in sessions:
                print(session)



        else:
            print("No sessions found.")

        cursor.close()
        database.close()

    except:
        
        print("Error viewing sessions D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

def viewExercises(member1):
    """
        This function allows the user to view their exercises
    """
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        #looking for sessions with member1.memberID
        cursor.execute("SELECT * FROM Exercises WHERE MemberID = %s", (member1.memberID,))

        exercises = cursor.fetchall()
        if(exercises):
            for exercise in exercises:
                print(exercise[1])

        else:
            print("No exercises found")
    except:
        
        print("Error viewing exercises D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()


def addExercises(member1):
    try:
        #connects to database
        database = connectToDatabase()
        #sets up cursor which allows python code to execute PostgreSQL commands
        cursor = database.cursor()

        exercise = input("What exercise would you like to add?")
        
        cursor.execute("INSERT INTO Exercises (Exercise, MemberID) VALUES (%s, %s)", (exercise, member1.memberID,))
        database.commit()

        print("Exercise added")

        cursor.close()
        database.close()

       

        
    except:
        
        print("Error adding exercises D:\n")

        #checks and closes cursor and database connection if not yet closed
        if cursor:
            cursor.close()
        if database:
            database.close()

    
    
def memberMain():
    """
    The main function for members
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
            print("What would you like to do?\n")
            print("Log In")
            print("Register")
            print("Exit")
            ans = input().lower()

            #log in
            if(ans == "login" or ans == "log in"):
                os.system('cls' if os.name == 'nt' else 'clear')
                member1 = login()
                if member1:
                    print("Logged in successfully")
                    loggedIn = True
                    
            #register
            elif(ans == "register" or ans == "sign up"):
                os.system('cls' if os.name == 'nt' else 'clear')
                register()
            
            #exit program
            elif(ans == "exit"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("See you next time!")
                break
            
            #unknown commands
            else:
                    
                print("That's not an option.")

        #if the user is logged in
        else:
            print("Graveler's Gritty Gymu!\n")
            print("Hello ", member1.firstName, "!")
            print("What would you like to do?\n")
            print("Profile")
            print("Update profile")   
            print("Exercises")
            print("Manage Personal Training Sessions")
            print("Group fitness classes")
            print("exit")
            ans = input().lower()

            #login (already logged in)
            if(ans == "login" or ans == "log in"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Your already logged in!")

            #register (already logged in)
            elif(ans == "register" or ans == "sign up"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Your already logged in! Please start new session to register")

            #view profile
            elif(ans == "profile"):
                os.system('cls' if os.name == 'nt' else 'clear')
                printInfo(member1)

            #update info, metrics, 
            elif(ans == "update"):
                os.system('cls' if os.name == 'nt' else 'clear')
                update(member1)

            #managing sessions
            elif(ans == "manage" or ans == "sessions"):
                os.system('cls' if os.name == 'nt' else 'clear')
                #schedule, reschedule or cancel session
                action = input("What would you like to do regarding sessions? ")
                if(action == "schedule"):
                    scheduleSession(member1)

                elif(action == "cancel"):
                    cancelSession(member1)

                elif(action == "view"):
                    viewSessions(member1)

            elif(ans == "exercises"):
                os.system('cls' if os.name == 'nt' else 'clear')
                #schedule, reschedule or cancel session
                action = input("What would you like to do regarding exercises? ")
                if(action == "view"):
                    viewExercises(member1)

                elif(action == "add"):
                    addExercises(member1)

            #exit program
            elif(ans == "exit"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("See you next time!")
                break

            else:
                print("That is not an option.")