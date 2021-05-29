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

def displayInfo(values):
    """
    Takes a tuple from a select query as input and prints out each value.
    """
    sleep_value = 0.3
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

def displayUser():
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
        displayInfo(values)
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

def displayRowid(rowid):
    """
    Takes a rowid as input and prints that rows information.
    Returns a list containing the row information as well
    """
    sleep_value = 0
    info = []
    cursor.execute("""
    SELECT rowid, * FROM userInfo
    WHERE rowid = :rowid""",
    {'rowid': rowid})
    values = cursor.fetchone()
    for item in values:
        info.append(item)

    time.sleep(sleep_value)
    print(f"Category: {values[1]}")
    time.sleep(sleep_value)
    print(f"Username: {values[2]}")
    time.sleep(sleep_value)
    print(f"Email: {values[3]}")
    time.sleep(sleep_value)
    print(f"Password: {values[4]}")
    print()

    return info



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
> """).upper()

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
        displayCategories()
        choice = helpfulFuncs.read_int_ranged("""
Would you like to display all user categories or search for a certain user if you already know the category?

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
                confirm_choice = helpfulFuncs.read_text(f"""
Are you sure you want to MODIFY all of USER {choice_id}'s information?
                        Y/N
> """).upper()
                if confirm_choice == "Y":
                    print(f"Existing info for user {choice_id}: ")
                    print()
                    values = displayRowid(choice_id)

                    category = values[1]
                    username = values[2]
                    email = values[3]
                    password = values[4]
                    print('Type "-SAME-" in any field to keep existing info the same.')
                    print()

                    # category

                    newCategory = helpfulFuncs.read_text_no_ws("Enter a new category: ")
                    if newCategory == "-same-" or newCategory == "-SAME-" or newCategory == False:
                        print("Skipped.")
                        pass
                    else:
                        cursor.execute("""
                        UPDATE userInfo
                        SET category = :category
                        WHERE rowid = :rowid 
                        """,
                        {'category': newCategory,'rowid': choice_id})
                    print()

                    # username

                    newUsername = helpfulFuncs.read_text_no_ws("Enter a new username: ")
                    if newUsername == "-same-" or newUsername == "-SAME-" or newUsername == False:
                        print("Skipped.")
                        pass
                    else:
                        cursor.execute("""
                        UPDATE userInfo
                        SET username = :username
                        WHERE rowid = :rowid
                        """,
                        {'username': newUsername, 'rowid': choice_id})

                    # email

                    print()
                    newEmail= helpfulFuncs.read_text_no_ws("Enter a new email: ")
                    if newEmail == "-same-" or newEmail == "-SAME-" or newEmail == False:
                        print("Skipped.")
                        pass
                    else:
                        cursor.execute("""
                         UPDATE userInfo
                         SET email = :email
                         WHERE rowid = :rowid
                         """,
                        {'email': newEmail, 'rowid': choice_id})

                    # password

                    print()
                    newPassword = helpfulFuncs.read_text_no_ws("Enter a new password: ")
                    if newPassword == "-same-" or newPassword == "-SAME-" or newPassword == False:
                        print("Skipped.")
                        pass
                    else:
                        cursor.execute("""
                         UPDATE userInfo
                         SET password = :password
                         WHERE rowid = :rowid
                         """,
                       {'password': newPassword, 'rowid': choice_id})
                else:
                    print("*Modify Cancelled*")
                    break
        elif choice == 2:
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
