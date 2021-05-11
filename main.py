import helpfulFuncs
import sys
import pickle
import time


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
    Creates user info and stores it as an object.
    """

    # TODO See if we can optimize this process by elim some loops
    min_char = 3
    max_char = 30

    category = "empty"
    username = "empty"
    email = "empty"

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
        user_info.append(newUser)
        saveUser(file_name)

        print(user_info)

        print()
        print(f"Info for {newUser.category} saved.")
        print(newUser)

        break


def saveUser(file_name):
    """
    Saves the users to the given file name.
    Users are stored as binary as a pickled file.
    Exceptions will be raised if the save fails.
    """

    print("Saved user info")

    with open(f'C:\\Users\\Denze\Documents\\user-info\\{file_name}', 'wb') as output_file:
        pickle.dump(user_info, output_file)


def loadUser(file_name):
    """
    Loads the user info from the given file name.
    exceptions will be raised if the file fails to load.
    """

    global user_info

    with open(f'C:\\Users\\Denze\Documents\\user-info\\{file_name}', 'rb') as input_file:
        user_info = pickle.load(input_file)




def displayUser():

    print("Here's a list of each category I currently have: ")
    time.sleep(1)
    for user in user_info:
        category = user.category
        print(category)

    print()
    search_name = helpfulFuncs.read_text("Enter the category name: ")
    search_name = search_name.strip()
    search_name = search_name.lower()

    result = None
    for user in user_info:
        category = user.category
        category = category.strip()
        category = category.lower()

        if category.startswith(search_name):
            result = user
            break

    if result != None:
        print()
        print(f'Category "{category}" selected.')
        print(result)
    else:
        print("User not found.")



user_info = []

file_name = "user-info.pickle"

prompt = f"""
| Password Manager |

1. Save a password
2. Find User
3. Edit User info
4. Save User info
5. Quit Program

Please select an option: """



try:
    loadUser(file_name)
except:
    print("File not loaded.")

while True:
    choice = helpfulFuncs.read_float_ranged(prompt, 1, 5)

    if choice == 1:
        createUser()
    if choice == 2:
        displayUser()
    if choice == 3:
        pass
    if choice == 4:
        pass
    if choice == 5:
        pass