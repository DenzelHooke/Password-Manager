import helpfulFuncs
import sys
import pickle
import sqlite3
import time


def ws_error():
    """
    Throws 'error' message
    """
    print("Please Enter Characters")
    time.sleep(1)


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
        choice = helpfulFuncs.read_text_no_ws("""
    Please enter what website or category these credentials will be used on.
            
            eg. Youtube
                Netflix
            
    ..type "quit" to close this program.
            
    Category: """)

        if choice == "QUIT" or choice == "Q":
            sys.exit()

        elif choice == "quit":
            sys.exit()

        if choice:
            category = choice
            break

        elif not choice:
            ws_error()
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
                ws_error()
                continue
            # To Add: Quit button

        elif choice == "BOTH":

            while True:

                email = helpfulFuncs.verifyEmail(
                    input("Please enter an email address: "))
                if not email:
                    ws_error()
                    continue

                username = helpfulFuncs.verifyUsername(
                    input("Please enter a username: "), min_char, max_char)
                # To Add: Quit button
                if username:
                    done = True
                    break
                else:
                    ws_error()
                    continue

        else:
            print("I don't understand that.")
            continue
    while True:
        password = helpfulFuncs.read_text_no_ws("Enter a password: ")
        if password:
            break
        else:
            ws_error()
            continue
    try:
        addUser(category, username, email, password)
        print()
        print("Information Added.")
        time.sleep(1)
    except:
        print("Error while attempting to save information to Database.")


def addUser(category, username, email, password):
    with conn:
        cursor.execute("INSERT INTO userInfo VALUES(:category, :username, :email, :password)",
                       {'category': category, 'username': username, 'email': email, 'password': password})


def displayCategories():
    print("Categories Listed Below:")
    print()
    with conn:
        cursor.execute("SELECT category FROM userInfo")
        for i in cursor.fetchall():
            print(i[0])


def displayUser():
    sleep_value = 0.3
    displayCategories()

    print()
    search_value = helpfulFuncs.read_text("Enter the category name: ")
    time.sleep(1)
    print()
    search_value = search_value.strip()
    values = findUser(search_value)
    if values:
        print(f'Retrieving values for category: "{search_value}"')
        time.sleep(1)
        for tuple in values:
            time.sleep(sleep_value)
            print(f"UserID: {tuple[0]}")
            time.sleep(sleep_value)
            print(f"Category: {tuple[1]}")
            time.sleep(sleep_value)
            print(f"Username: {tuple[2]}")
            time.sleep(sleep_value)
            print(f"Email: {tuple[3]}")
            time.sleep(sleep_value)
            print(f"Password: {tuple[4]}")
            print()
    else:
        print(f"There was no category found named {search_value}")


def findUser(category):
    cursor.execute("""
                       SELECT rowid, * FROM userInfo
                       WHERE category =:category""",
                        {'category': category})
    values = cursor.fetchall()
    if values is None:
        return False
    else:
        return values

def removeUser():
    print(""" 
    
    *****************
    User REMOVAL Mode
    *****************
    """)
    time.sleep(2)

    displayUser()
    while True:
        choice_id = helpfulFuncs.read_text("Please enter the UserID of the user you wish to remove: ")
        confirm_choice = helpfulFuncs.read_text("""
Are you sure you want to DELETE all of this user's information?
                        Y/N
: """).upper()

        if confirm_choice == 'Y':
            cursor.execute("""
            DELETE FROM userInfo
            WHERE rowid = :choice""", {'choice': choice_id})
            print("User Information Deleted.")
            break
        elif confirm_choice == 'N':
            print("Deletion Aborted.")
            break
        else:
            print("I don't understand that.")
            continue

def editMode():
    print()
    print("Edit mode selected.")
    print()
    while True:
        choice = helpfulFuncs.read_int_ranged("""
Would you like to display all user categories or search for a certain user if you already know the category?

1. Display all existing user categories.
2. Search by category.
3. Quit edit mode.

choice: """, 1, 3)

        if choice == 1:
            displayCategories()
        elif choice == 2:
            search_user = findUser(helpfulFuncs.read_text_no_ws("Please enter the category name: "))
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


def menu_screen():
    prompt = f"""
    | Password Manager |

    1. Save a password
    2. Find User
    3. Edit User info
    4. Remove User
    5. Quit Program

    Please select an option: """

    while True:
        choice = helpfulFuncs.read_float_ranged(prompt, 1, 5)

        if choice == 1:
            createUser()
        elif choice == 2:
            print()
            print("Find user mode selected.")
            print()
            displayUser()
        elif choice == 3:
            editMode()
        elif choice == 4:
            removeUser()
        elif choice == 5:
            sys.exit()


def spinUpDB():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS userInfo(
    category text COLLATE NOCASE,
    username text,
    email text,
    password text
    )""")


if __name__ == "__main__":
    conn = sqlite3.connect('userinfo.db')
    cursor = conn.cursor()
    spinUpDB()
    # Add test Data


    menu_screen()
