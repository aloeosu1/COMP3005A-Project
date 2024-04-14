"""
    Michael Han
    101157504
    COMP3005A
    Final Project V2

    

"""

import psycopg2
from psycopg2 import sql
from datetime import date, datetime
import os

import member
import trainer
import admin

def main():
    #asking user what type of user they are
    userType = input("Are you a member, trainer or admin? ")

    #if user is a member
    if(userType == "member"):
        os.system('cls' if os.name == 'nt' else 'clear')
        member.memberMain()

    elif(userType == "trainer"):
        os.system('cls' if os.name == 'nt' else 'clear')
        trainer.trainerMain()

    else:
        print("Unknown type")

    



main()