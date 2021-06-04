import pydoc
import re


def verifyEmail(userInput):
    pattern = re.compile(r'([a-zA-Z0-9-_.]+@[a-zA-Z0-9-]+\.(com|org|edu|ca))')
    match = pattern.findall(userInput)

    if match:
        # match returns a *list* with a tuple inside.
        match = match[0]
        match = match[0] 
        return match
    else:
        print("That's not an email address.")
        return False


def verifyUsername(userInput, min_char, max_char):
    """
    Counts the number of characters and returns the result.
    Returns False if text is below or above specified limit.
    Raises Exception if max and min are reversed.
    Keyboard interrupts (ctrl + C) are ignored.
    """

    if min_char > max_char:
        raise Exception("Min value is greater than Max value.")
    count = 0

    try:
        while True:
            whitespace_check = white_space_checker(userInput)
            if whitespace_check:
                return False
            else:
                for character in userInput:
                    count += 1

                if count > max_char:
                    print()
                    print(f"Username must be less than {max_char} characters.")
                    return False
                elif count < min_char:
                    print()
                    print(f"Username must be at least {min_char} characters.")
                    return False
                else:
                    return userInput
    except KeyboardInterrupt:
        print("Please don't try to force quit the program")


def verifyWebsite(website):
    pattern = re.compile(r'(https://|www\.){1}(\w+)(\.\w+)')
    matchTuple = pattern.findall(website)

    if matchTuple:
        for i in matchTuple:
            string = ''.join(i)
            return string
    else:
        print("Website entered is not a valid ")
        return False


def read_text(prompt):
    """"
    Returns a string containing input from the user
    Ignores Keyboard interrupts
    """

    while True:
        try:
            result = input(prompt)
            # If we get here, no exception was raised
            break
        except KeyboardInterrupt:
            print("Please don't try to force quit the program.")

    return result


def read_text_no_ws(prompt):
    """"
    Returns a string containing input from the user
    Ignores Keyboard interrupts
    Returns False if string contains ONLY whitespace
    Returns False if no string was entered
    """
    count = 0

    while True:
        try:
            result = input(prompt)
            check = white_space_checker(result)
            if check:
                return False
            else:
                return result
        except KeyboardInterrupt:
            print("Please don't try to force quit the program.")


def white_space_checker(input):
    """"
    Returns False if string contains ONLY whitespace
    Returns False if no string was entered
    """
    count = 0
    for char in input:
        count += 1
    if input.isspace() or count == 0:
        return True
    else:
        return False


def read_float(prompt):
    """
    Displays a prompt and reads in a number.
    Keyboard interrupts are ignored.
    Invalid numbers are rejected.
    Returns a float containing the input of the user.
    """
    while True:
        try:
            number_text = read_text(prompt)
            result = float(number_text)  # Verify that input is float ONLY
            # If we get here the the input is a float.
            # Break out of loop
            break
        except ValueError:
            print("Please enter a valid number.")
            continue
    return result


def read_int(prompt):
    """
    Displays a prompt and reads in a number.
    Keyboard interrupts are ignored.
    Invalid numbers are rejected.
    Returns a integer containing the input of the user.
    """
    while True:
        try:
            number_text = read_text(prompt)
            result = int(number_text)  # Verifies that input is float ONLY
            # If we get here the the input is a float.
            # Break out of loop
            break
        except ValueError:
            print("Please enter a valid number.")
            continue
    return result


def read_float_ranged(prompt, min_value, max_value):
    """
    Displays a prompt and reads in a number.
    min_value gives the minimum value
    max_value gives the max value.
    Raises Exception if max and min are reversed
    Keyboard interrupts (ctrl + C) are ignored
    Returns a float containing the value input from the user.
    """
    if min_value > max_value:
        raise Exception('Min value is greater than Max value')

    while True:
        result = read_float(prompt)
        if result < min_value:
            print()
            print('That number is too low.')
            print(f'Minimum Value is {min_value}')
            continue
            # Repeat the number reading
        elif result > max_value:
            print()
            print('That number is too high.')
            print(f'Maximum Value is {max_value}')
            continue
            # Repeat the number reading
        else:
            break
    # Return result
    return result


def read_int_ranged(prompt, min_value, max_value):
    """
    Displays a prompt and reads in a number.
    min_value gives the minimum value
    max_value gives the max value.
    Raises Exception if max and min are reversed
    Keyboard interrupts (ctrl + C) are ignored
    Returns a float containing the value input from the user.
    """
    if min_value > max_value:
        raise Exception('Min value is greater than Max value')

    while True:
        result = read_int(prompt)
        if result < min_value:
            print()
            print('That number is too low.')
            print(f'Minimum Value is {min_value}')
            continue
            # Repeat the number reading
        elif result > max_value:
            print()
            print('That number is too high.')
            print(f'Maximum Value is {max_value}')
            continue
            # Repeat the number reading
        else:
            break
    # Return result
    return result


def read_words(prompt):
    """"
    Returns a string containing input from the user
    Ignores Keyboard interrupts
    Ignores number values.
    """

    while True:
        try:
            result = str(input(prompt))
            if not result.isalpha():
                print("Only alpha characters accepted.")
                continue
            # If we get here, no exception was raised
            break
        except KeyboardInterrupt:
            print("Please don't try to force quit the program.")

    return result
