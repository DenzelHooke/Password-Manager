import helpfulFuncs
import sys
import os


class User:
    """Creates objects containing user information"""

    def __init__(self, category, email, username, password):
        self.__category = category
        self.__email = email
        self.__username = username
        self.__password = password
        self.__version = 1

    def __str__(self):
        return f"""
Category: {self.__category}
Email: {self.__email}
Username: {self.__username}
Password: {self.__password}
"""


def menuScreen():
    """The login screen that allows user input"""


def createUser():
    """
    Asks user for input.
    Verifies length.
    """

    user_list = []

    min_char = 3
    max_char = 30

    done = False

    category = "empty"
    username = "empty"
    email = "empty"
    password = "empty"

    while True:
        choice = helpfulFuncs.read_text("""
    Would you like to enter in a category?
                Y/N/quit
    Choice: """).upper()

        if choice == "Y" or choice == "YES":
            category = helpfulFuncs.read_text("Enter in the category: ")
            break

        elif choice == "N" or choice == "NO":
            break

        else:
            print("I don't understand that.")
            continue

    while True:
        if done:
            break

        choice = helpfulFuncs.read_text("""
    Would you like to enter in an email address, username or both??
                Type "email", "username", "both"
    Choice: """).upper()

        if choice == "EMAIL":
            email = helpfulFuncs.verifyEmail(input("Enter an email address: "))
            if email:
                done = True
                break
            else:
                continue

        elif choice == "USER" or choice == "USERNAME":
            username = helpfulFuncs.verifyUsername(input("Enter your username: "), min_char, max_char)
            if not username:
                continue
            else:
                done = True
                break
            # To Add: Quit button


        elif choice == "BOTH":

            while True:
                email = helpfulFuncs.verifyEmail(
                    input("Please enter an email address: "))
                if not email:
                    continue

                username = helpfulFuncs.verifyUsername(
                    input("Please enter a username: "), min_char, max_char)
                # To Add: Quit button
                if not username:
                    continue
                else:
                    done = True
                    break

        else:
            print("I don't understand that.")
            continue

    if done:
        password = helpfulFuncs.read_text("Enter a password: ")
        newUser = User(category=category, email=email, username=username, password=password)
        print(f"\n{newUser}")
        sys.exit()

        # To Add: Quit button


createUser()
