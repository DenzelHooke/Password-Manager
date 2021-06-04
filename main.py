import helpfulFuncs
import sys
import sqlite3
import time


def ws_error():
    """
    Throws 'error' message.
    """
    print("Please Enter Characters")
    time.sleep(1)


def createUser():
    """
    Runs through the user creation process.
    Stores user information within database with the help of the addUser function.
    """

    min_char = 3
    max_char = 30

    category = None
    username = None
    email = None
    done = False

    while not done:
        prompt = """

Welcome to user creation mode. 

Please select an option below: 

1. Create user
2. Go back to main menu

Choice: """

        choice = helpfulFuncs.read_int_ranged(prompt, 1, 2)
        if choice == 1:
            while True: 
                    done = False
                    choice = helpfulFuncs.read_text_no_ws("""
Please enter what website or category these credentials will be used on.
        
        eg. Youtube
            Netflix
        
Category: """)


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


                elif choice == "BOTH":

                    while True:
                        # Think about eliminating this while loop and bringing the user back to the sub menu if they mess up...???
                        email = helpfulFuncs.verifyEmail(
                            input("Please enter an email address: "))
                        if not email:
                            continue

                        username = helpfulFuncs.verifyUsername(
                            input("Please enter a username: "), min_char, max_char)
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
                    done = True
                else:
                    ws_error()
                    continue
            try:
                addUser(category, username, email, password)
                print()
                print("Information Added.")
                time.sleep(1)
            except Exception as error:
                print("**Error while attempting to save information to Database**")
                print(f"Reason: {error}")
                time.sleep(3)
                
                
        elif choice == 2:
            break
            


def addUser(category, username, email, password):
    """
    Takes user information as parameters such as:
    category, username, email, password and inserts them into the database. 
    """
    with conn:
        cursor.execute("INSERT INTO userInfo VALUES(:category, :username, :email, :password)",
                       {'category': category, 'username': username, 'email': email, 'password': password})


def displayCategories():
    """
    Displays all categories that currently exist within the database.
    """
    print("Categories Listed Below:")
    print()
    with conn:
        cursor.execute("SELECT category FROM userInfo")
        for i in cursor.fetchall():
            print(i[0])


def displayInfo(values):
    """
    Takes a tuple from a select query as a parameter and prints out each value.
    """
    sleep_value = 0.3
    for item in values:
        time.sleep(sleep_value)
        print(f"UserID: {item[0]}")
        time.sleep(sleep_value)
        print(f"Category: {item[1]}")
        time.sleep(sleep_value)
        print(f"Username: {item[2]}")
        time.sleep(sleep_value)
        print(f"Email: {item[3]}")
        time.sleep(sleep_value)
        print(f"Password: {item[4]}")
        print()


def displayUser():
    """
    Takes category name as input and passes those values off 
    to other functions. 
    """

    while True: 
        print("Find user mode selected.")
        prompt = """

1. Find user
2. Go back to main menu

Please select an option: """
        choice = helpfulFuncs.read_int_ranged(prompt, 1, 2)

        if choice == 1:
                displayCategories()

                print()
                search_value = helpfulFuncs.read_text("Enter the category name: ")
                time.sleep(1)
                print()
                search_value = search_value.strip()
                values = findUser(search_value)
                if values:
                    print(f'Retrieving values for category {search_value}:')
                    print()
                    time.sleep(0.5)
                    displayInfo(values)
                else:
                    print(f"There was no category found named {search_value}")
                    continue
        elif choice == 2:
            break


def verifyRowid(rowid):
    """
    Takes a rowid as a parameter and returns True if that rowid exists and False if it does not.
    """
    cursor.execute("""
        SELECT EXISTS(SELECT rowid, * FROM userInfo
        WHERE rowid = :rowid)""",
                   {'rowid': rowid})
    check_list = cursor.fetchone()

    for item in check_list:
        if item == 1:
            return True
        else:
            return False


def displayRowid(rowid):
    """
    Takes a rowid as input and prints that rows information.
    """
    sleep_value = 0

    cursor.execute("""
        SELECT rowid, * FROM userInfo
        WHERE rowid = :rowid""",
                   {'rowid': rowid})
    values = cursor.fetchone()

    time.sleep(sleep_value)
    print(f"Category: {values[1]}")
    time.sleep(sleep_value)
    print(f"Username: {values[2]}")
    time.sleep(sleep_value)
    print(f"Email: {values[3]}")
    time.sleep(sleep_value)
    print(f"Password: {values[4]}")
    print()


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
    """
    Asks a user for a prompt.
    Removes user from database based on user ID entered.
    Loops back to main sub menu if that category doesn't exist.
    """
    while True:
        print(""" 
        
*****************
User REMOVAL Mode
*****************

""")
        time.sleep(2)
        prompt = """

Please select an option

1. Search by category
2. Go back to main menu

Choice: """
        choice = helpfulFuncs.read_int_ranged(prompt, 1, 2)
        if choice == 1:
            displayCategories()
            print()
            search_value = helpfulFuncs.read_text_no_ws("Enter the category name: ")
            if search_value != False: 
                values = findUser(search_value)
                if values:
                    print(f'Retrieving values for category {search_value}:')
                    print()
                    time.sleep(0.5)
                    displayInfo(values)

                    choice_id = helpfulFuncs.read_text("Please enter the UserID of the user you wish to remove: ")
                    if verifyRowid(choice_id) is False:
                        print()
                        print("That UserID doesn't exist.")
                        print()
                        time.sleep(1)
                        continue

                    else:
                        displayRowid(choice_id)
                    
                    confirm_choice = helpfulFuncs.read_text("""
Are you sure you want to DELETE all of this user's information?
                        Y/N
> """).upper()

                    if confirm_choice == 'Y':
                        with conn:
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
                        print("Deletion Aborted.")
                        continue
                else:
                    print(f"There was no category found named {search_value}")
                    continue
            else:
                ws_error()
                continue
        elif choice == 2:
            break

def editMode():
    """
    Allows the ability to edit user information.
    Asks users for their new info via self-created input functions.
    Returns False if user enters a number that doesn't exist.
    """
    print()
    print("Edit mode selected.")
    print()
    while True:
        displayCategories()
        choice = helpfulFuncs.read_int_ranged("""
Welcome to edit mode.

1. Search by category.
2. Quit edit mode.

choice: """, 1, 2)

        if choice == 1:
            search_user = helpfulFuncs.read_text("Please enter the category name: ")
            found = findUser(search_user)
            if found:
                print()
                print(f"Printing results for {search_user}: ")
                print()
                displayInfo(found)
                print()
                choice_id = helpfulFuncs.read_text("Please enter the UserID of the user you wish to edit: ")
                if verifyRowid(choice_id) is False:
                    print()
                    print("That UserID doesn't exist.")
                    print()
                    continue
                else:
                    confirm_choice = helpfulFuncs.read_text(f"""
Are you sure you want to MODIFY all of USER {choice_id}'s information?
                        Y/N
> """).upper()
                    if confirm_choice == "Y":
                        print(f"Existing info for user {choice_id}: ")
                        print()
                        displayRowid(choice_id)
                        print('Type "-SAME-" in any field to keep existing info the same.')
                        print()

                        # category

                        newCategory = helpfulFuncs.read_text_no_ws("Enter a new category: ")
                        if newCategory == "-same-" or newCategory == "-SAME-" or newCategory is False:
                            print("Skipped.")
                            pass
                        else:
                            with conn:
                                cursor.execute("""
                                UPDATE userInfo
                                SET category = :category
                                WHERE rowid = :rowid 
                                """, {'category': newCategory, 'rowid': choice_id})
                        print()

                        # username

                        newUsername = helpfulFuncs.read_text_no_ws("Enter a new username: ")
                        if newUsername == "-same-" or newUsername == "-SAME-" or newUsername is False:
                            print("Skipped.")
                            pass
                        else:
                            with conn:
                                cursor.execute("""
                                UPDATE userInfo
                                SET username = :username
                                WHERE rowid = :rowid
                                """, {'username': newUsername, 'rowid': choice_id})

                        # email

                        print()
                        newEmail = helpfulFuncs.read_text_no_ws("Enter a new email: ")
                        if newEmail == "-same-" or newEmail == "-SAME-" or newEmail is False:
                            print("Skipped.")
                            pass
                        else:
                            with conn:
                                cursor.execute("""
                                UPDATE userInfo
                                SET email = :email
                                WHERE rowid = :rowid
                                """, {'email': newEmail, 'rowid': choice_id})

                        # password

                        print()
                        newPassword = helpfulFuncs.read_text_no_ws("Enter a new password: ")
                        if newPassword == "-same-" or newPassword == "-SAME-" or newPassword is False:
                            print("Skipped.")
                            pass
                        else:
                            with conn:
                                cursor.execute("""
                                UPDATE userInfo
                                SET password = :password
                                WHERE rowid = :rowid
                                """, {'password': newPassword, 'rowid': choice_id})
                    else:
                        print("*Modify Cancelled*")
                        continue
        elif choice == 2:
            break


def menu_screen():
    """
    Displays menu screen with a choice of numbered options.
    """
    prompt = """
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
    """
    Creates Database.
    """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS userInfo(
    category text COLLATE NOCASE,
    username text,
    email text,
    password text
    )""")


if __name__ == "__main__":
    conn = sqlite3.connect('USER_FILE.db')
    cursor = conn.cursor()
    spinUpDB()
    menu_screen()
