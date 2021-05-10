import helpfulFuncs
import sys

users = []


class User:
    """Creates objects containing user information"""

    def __init__(self, category, email, username, password):
        self.category = category
        self.email = email
        self.username = username
        self.password = password
        self.__version = 1

    def __str__(self):
        return f"""
Category: {self.category}
Email: {self.email}
Username: {self.username}
Password: {self.password}
"""


def menuScreen():
    """The login screen that allows user input"""


def createUser():
    """
    Asks user for input.
    Verifies length.
    """

    # TODO See if we can optimize this process by elim some loops
    min_char = 3
    max_char = 30

    category = "empty"
    username = "empty"
    email = "empty"

    while True:

        while True:

            done = False
            choice = helpfulFuncs.read_text("""
        Please enter what website or category these credentials will be used on.
                
                eg. Youtube
                    Netflix
                
        ..type "quit" to close this program.
                
        Category: """)


            if choice == "QUIT" or choice == "Q":
                sys.exit()

            elif choice == "quit" or choice == "q":
                sys.exit()

            if choice:
                category = choice
                break

            elif not choice:
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
                    break
                else:
                    continue

            elif choice == "USER" or choice == "USERNAME":
                username = helpfulFuncs.verifyUsername(input("Enter your username: "), min_char, max_char)
                if username:
                    break
                else:
                    continue
                # To Add: Quit button

            elif choice == "BOTH":

                while True:

                    # TODO put both the email and user creation into their own functions

                    email = helpfulFuncs.verifyEmail(
                        input("Please enter an email address: "))
                    if not email:
                        continue

                    username = helpfulFuncs.verifyUsername(
                        input("Please enter a username: "), min_char, max_char)
                    # To Add: Quit button
                    if username:
                        done = True
                        break
                    else:
                        continue

            else:
                print("I don't understand that.")
                continue

        while True:
            password = helpfulFuncs.read_text("Enter a password: ")
            newUser = User(category=category, email=email, username=username, password=password)

            # Add user
            users.append(newUser)
            print(users)

            print()
            print(f"Info for {newUser.category} ")
            print(newUser)

            done = False
            break


createUser()
