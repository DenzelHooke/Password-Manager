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


def displayCategories():
    print("Here's a list of each category I currently have: ")
    print()
    time.sleep(1)
    for user in user_info:
        category = user.category
        print(category)


def displayUser():
    print()
    print("Find user mode selected.")
    print()
    displayCategories()

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


def findUser(category):
    search_user = category
    search_user = search_user.strip()
    search_user = search_user.lower()

    result = None
    for user in user_info:
        category = user.category
        category = category.strip()
        category = category.lower()

        if category.startswith(search_user):
            result = user
            break

    if result != None:
        return result
    else:
        return None


def editMode():
    print()
    print("Edit mode selected.")
    print()
    while True:
        choice = helpfulFuncs.read_int_ranged("""
Would you like to display all user information or search for a certain user if you already know the category?

1. Display all user information.
2. Display a certain user.
3. Quit edit mode.

choice: """, 1, 3)

        if choice == 1:
            displayCategories()
        elif choice == 2:
            search_user = findUser(helpfulFuncs.read_text("Please enter the category name: "))
            if search_user:
                print()
                print(f"Current user information for {search_user.category}: ")
                print(search_user)
                choice = helpfulFuncs.read_text("""Are you sure you want to edit this information?
                Y/N
choice: """).upper()
                if choice == "Y" or choice == "YES":
                    print()
                    print('Type "-SAME-" in any field to keep existing info the same.')
                    print()
                    new_category = helpfulFuncs.read_text("Enter a new category: ")
                    if new_category == "-same-" or new_category == "-SAME-":
                        pass
                    else:
                        search_user.category = new_category

                    new_email = helpfulFuncs.read_text("Enter a new email address: ")
                    if new_email == "-same-" or new_email == "-SAME-":
                        pass
                    else:
                        search_user.email = new_email

                    new_username = helpfulFuncs.read_text("Enter a new username: ")
                    if new_username == "-same-" or new_username == "-SAME-":
                        pass
                    else:
                        search_user.username = new_username

                    new_password = helpfulFuncs.read_text("Enter a new password: ")
                    if new_password == "-same-" or new_password == "-SAME-":
                        pass
                    else:
                        search_user.password = new_password

                elif choice == "N" or choice == "NO":
                    print()
                    print(f"Edit for {search_user.category} cancelled.")
                else:
                    continue

            else:
                print("Category not found.")
                time.sleep(2)
                continue

        elif choice == 3:
            break


user_info = []

file_name = "user-info.pickle"

prompt = f"""
| Password Manager |

1. Save a password
2. Find User
3. Edit User info
4. Quit Program

Please select an option: """

try:
    loadUser(file_name)
except:
    print("File not loaded.")

while True:
    choice = helpfulFuncs.read_float_ranged(prompt, 1, 5)

    if choice == 1:
        createUser()
    elif choice == 2:
        displayUser()
    elif choice == 3:
        editMode()
    elif choice == 4:
        sys.exit()
