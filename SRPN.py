# Comment detection
is_comment = False

# Random number generations globals
random_lst_length = 31
seed = 1
starting_point = 344
random_lst = [seed] + [0] * (random_lst_length - 1)
repeat_rand_bool = True  # To repeat the first 22 numbers twice
random_counter = starting_point  # It represents the number of index of the random number needed to be generated.

# Stack related globals
MAX_NUM = 2147483647  # 2**31 - 1
MIN_NUM = -2147483648  # -2**31
MAX_NUMBER_STACK_LENGTH = 23  # The stack as max size of 23, for example "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24" would display a "Stack overflow." message
number_stack = []
operation_stack = []
order_to_sort = "^%/*+-"  # This is the order that operations are processed when infix notation

# Error messages
DIVISION_BY_ZERO = "Divide by 0."
EMPTY_STACK = "Stack empty."
NEGATIVE_POWER = "Negative power."
STACK_OVERFLOW = "Stack overflow."
STACK_UNDERFLOW = "Stack underflow."
UNRECOGNISED_OPERATOR = 'Unrecognised operator or operand "{}".'
MOD_0_CRASH = "main.sh: line 5:    20 Floating point exception(core dumped) ./srpn/srpn"
LONG_STRING = "main.sh: line 5:    34 Segmentation fault      (core dumped) ./srpn/srpn"
EXIT_MSG = "exit status {}"


# The random functions below implement the random function in SRPN perfectly.
# The following links are the links I based my code off of (but my code has no imports)
# https://www.mscs.dal.ca/~selinger/random/
# https://gist.github.com/integeruser/4cca768836c68751904fe215c94e914c
def random_overflow_check(num):
    """
    Helper function to check whether a number overflows when generated
    :param num: integer "pseudo-randomly" generated
    :return: integer after it has been corrected from overflow
    """
    return num if MIN_NUM <= num <= MAX_NUM else (num + (MAX_NUM + 1)) % (2 ** 32) - MAX_NUM - 1  # calculates the equivalent of c_uint


def generate_random_num(counter):
    """
    Receives a counter that represents the nth random number in the sequence that needs to be generated (based on the algorithm in the website)
    and returns it
    :param counter: integer representing the nth random number to generate in the "random" sequence
    :return: integer representing the nth random num in the "random" sequence
    """
    return random_overflow_check(random_lst[counter % 31] + random_lst[(counter - 3) % 31])


# These 3 functions require a bit less memory than the github link one. The random_lst length is of length 31 rather than 34 and it also makes the calculations a lot easier.
def random_init():
    """
    Initiates the list of random numbers to start off with.
    :return: None
    """
    for i in range(1, 31):
        random_lst[i] = (16807 * random_lst[i-1]) % MAX_NUM
        if random_lst[i] < 0: random_lst[i] += MAX_NUM
    # Note that I don't have the second for loop that is in the github link as using this implementation of length 31 it is unnecessary
    for i in range(34, starting_point):
        random_lst[i % 31] = generate_random_num(i)


def increment_rand_counter():
    global repeat_rand_bool, random_counter
    # In the SRPN calculator they repeat the first 22 numbers at the beginning again. The repeat_rand_bool replicates that
    if repeat_rand_bool and random_counter == starting_point + 22:
        random_counter = starting_point
        repeat_rand_bool = False
        # Generates the new random number and stores it in random_lst
    if random_counter > starting_point + 22 or repeat_rand_bool is True:
        random_lst[random_counter % 31] = generate_random_num(random_counter)
    random_counter += 1
    return random_lst[(random_counter - 1) % 31]


def random():
    """
    This function returns the next "pseudo-random" number in the list of random numbers
    :return: integer which is an element of the list random_lst
    """
    random_num = increment_rand_counter()
    if random_num < 0: random_num += 2**32  # makes sure the number is positive
    random_num = random_num >> 1  # bit shifts the number by 1 (equivalent to floor division by 2)
    return random_num


def append_to_num_stack(num):
    """
    This functions gets a number and index and tries to append the number to the number_stack.
    If the MAX_NUMBER_STACK_LENGTH is reached then an error is displayed.
    :param num: float, None
    :return: None
    """
    if num is None: return None
    elif len(number_stack) == MAX_NUMBER_STACK_LENGTH:
        print(STACK_OVERFLOW)
        return None
    elif num > MAX_NUM: num = MAX_NUM  # The calculator is saturated, so for any value above the maximum, it turns it to the maximum value. Consider the test "99999999999999 1 -"
    elif num < MIN_NUM: num = MIN_NUM  # The calculator is saturated, so for any value below the minimum, it turns it to the minimum value. Consider the test "-99999999999999 1 +"
    number_stack.append(num)


def display_num_stack():
    """
    Displays content of number_stack, if the stack is empty then it displays MIN_NUM
    :return: None
    """
    if len(number_stack) == 0: print(MIN_NUM)  # This is to cover for the test case when d is pressed at the very beginning
    else:
        for element in number_stack:
            # The display truncates every number. It is easy to see that with the test "1 2 / d 2 * d" to see that the number is changed on display rather than when its stored
            # To prove the number is truncated (rather than floored) consider the test "-11 3 / d" which displays -3 (instead of -4 if it were floored)
            print(int(element))


def peek_num_stack():
    """
    Displays the last element in number_stack, if the stack is empty then it displays "Stack empty."
    :return: None
    """
    if len(number_stack) == 0: print(EMPTY_STACK)  # This is to cover for the test case when = is pressed at the very beginning
    else: print(int(number_stack[-1]))  # As with the display_num_stack function, the number is truncated on display.


def operation_error(num_1, num_2, msg):
    """
    Gets 2 numbers and a message, it appends both numbers to number_stack and prints the message.
    This function is used when extreme cases happen such as division by 0 or exponentiation to negative powers.
    :param num_1: float
    :param num_2: float
    :param msg: string containing error message
    :return: None
    """
    append_to_num_stack(num_1)
    append_to_num_stack(num_2)
    print(msg)


def add(num_1, num_2):
    """
    Gets 2 numbers and returns their sum
    :param num_1: float
    :param num_2: float
    :return: float (the sum of num_1 and num_2)
    """
    return num_1 + num_2


def subtract(num_1, num_2):
    """
    Gets 2 numbers and returns their difference
    :param num_1: float
    :param num_2: float
    :return: float (the difference of num_1 and num_2)
    """
    return num_1 - num_2


def multiply(num_1, num_2):
    """
    Gets 2 numbers and returns their product
    :param num_1: float
    :param num_2: float
    :return: float (the product of num_1 and num_2)
    """
    return num_1 * num_2


def divide(num_1, num_2):
    """
    Gets 2 numbers and returns the value of num_1 divided by num_2 (prints an error message and returns None if num_2 is 0)
    :param num_1: float
    :param num_2: float
    :return: float (the value of num_1 divided by num_2) or None if num_2 is 0
    """
    # This is to cover for the tests when division by 0 is attempted (for example "3 0 / d" yields the error message "Divide by 0." and returns both numbers into the stack)
    if num_2 == 0: return operation_error(num_1, num_2, DIVISION_BY_ZERO)
    return num_1 / num_2


def power(num_1, num_2):
    """
    Gets 2 numbers and returns their exponentiation (prints an error message and returns None if num_2 is negative)
    :param num_1: float
    :param num_2: float
    :return: float (the exponentiation of num_1 and num_2 or MIN_NUM if its negative number to the power of fractional exponent)
    or None if num_2 is negative
    """
    # This is to cover for tests when power of negatives is attempted (for example "1 -1 ^ d" yields the error message "Negative power." and returns both numbers into the stack)
    if num_2 < 0: return operation_error(num_1, num_2, NEGATIVE_POWER)
    # This is to cover for the tests when negatives to fractional powers is attempted (for example -1 1/2 ^ d will display the minimum number)
    # NOTE that this MIN_NUM (in the actual calculator) can not then be used in further calculations
    # (except for mod and exponentiation by 0 which both seem to be special cases that "free" that number) whereas here it can.
    return num_1 ** num_2 if (num_1 >= 0 or num_2 == int(num_2)) else MIN_NUM


def mod(num_1, num_2):
    """
    Gets 2 numbers and returns their modulo (prints an error message and returns None if num_1 is 0)
    NOTE: This function does not deal and ends up crashing when inputting 0 for num_2
    NOTE 2: This function is replicated just like the function in the original SRPN (which is why it looks a bit complex)
    This means that is also accepts (and returns) negative numbers with certain prompts
    :param num_1: float
    :param num_2: float
    :return: integer (the modulo of num_1 and num_2) or None if num_1 is 0
    """
    if num_1 == 0: return operation_error(num_1, num_2, DIVISION_BY_ZERO)  # This is to cover for tests when num_1 = 0, in practice this is possible but in SRPN it is not allowed.
    num_1, num_2 = int(num_1), int(num_2)  # The numbers are truncated. This can be easily demonstrated with the tests "51/10 5/2 %"
    if num_2 == 0:  # Replicating program crash output for example 5 0 %
        print(MOD_0_CRASH)
        exit(EXIT_MSG.format(136))
    result = num_1 % num_2
    if result != 0:  # The following few lines are to cover for tests when either num_1 or num_2 (or both) are negative to make it return the same value as the calculator does
        # Consider the tests "-9 -4 %", "-9 4 %" and "9 -4 %" to understand why
        if num_1 < 0: result -= abs(num_2)
        if num_2 < 0: result += abs(num_2)
    return result


# The two dictionaries store an operation with its corresponding function name. This allows us to call the function when seeing the operation rather than having many if statements.
operation_dict = {"^": power, "%": mod, "/": divide, "*": multiply, "-": subtract, "+": add}
command_operation_dict = {"r": random, "d": display_num_stack, "=": peek_num_stack}


def use_operations_stack():
    """
    Get the last operator in the operation_stack to use and uses the last 2 numbers in number_stack for that operation.
    If there are less than 2 numbers, then an error message is displayed.
    :return: None
    """
    while len(operation_stack) != 0:
        op = operation_stack.pop()
        if len(number_stack) < 2: print(STACK_UNDERFLOW)  # To cover for tests where there is a stack underflow, for example "1 +".
        else:
            # This calls the correct function from the operation_dict and then inputs the 2 numbers into it. Then appends the result to number_stack
            num_2, num_1 = number_stack.pop(), number_stack.pop()
            append_to_num_stack(operation_dict[op](num_1, num_2))


def precedence_checker(operator, precedence):
    """
    Gets an operator and current precedence, checks whether the operator is lower precedence, if it is then the operations in operation_stack are used
    Then it returns new_precedence after appending it to the operation_stack
    :param operator: string representing a mathematical operator
    :param precedence: integer representing current precedence
    :return: integer representing new precedence
    """
    new_precedence = order_to_sort.find(operator)
    if new_precedence > precedence: use_operations_stack()
    operation_stack.append(operator)
    return new_precedence


def is_octal(string):
    """
    Receives a string and calculates whether a number is a valid octal or not.
    Returns True id valid, False if not, returns None if the number is not valid and isn't single digit
    :param string: string representing an integer to be checked
    :return: True if valid, False if not, returns None if the number is not valid and isn't single digit
    """
    if string[0] != "0" and string[:2] != "-0": return False  # If the number starts with 0 then its a positive octal, otherwise its negative octal
    for char in string:
        if char == "8" or char == "9":  # If the number has 8 or 9 in it, then it isn't valid
            if -8 >= int(string) or int(string) >= 8: return None  # If a number isn't a valid octal and isn't single-digit, then SRPN disregards it
            return False
    return True


def evaluate_valid_number(string, octal):
    """
    Turns string into decimal or octal according to the boolean variable octal.
    If it is octal and above 20 digits long it swaps is for -1 if its a positive number and 0 if its a negative number.
    Then it appends it to the stack
    :param string: string representing integer (either in octal or decimal form)
    :param octal: boolean representing whether string is octal or decimal form
    :return: None
    """
    if not octal: num = int(string)
    else:
        if len(string) > 20 and string[0] == "0": num = -1  # This covers tests for anything larger than 07777777777777777777
        elif len(string) > 21 and string[0] == "-": num = 0  # This covers tests for anything smaller than -07777777777777777777
        else: num = int(string, 8)  # This covers for all tests from 0 to 295600127, for some reason it overflows after this and I cannot figure out the pattern
    append_to_num_stack(num)


def process_string(string, is_digit, precedence):
    """
    Gets a string, a boolean of whether the string is a digit or not and the current precedence.
    Then, if it is a number, then it is added to the stack, otherwise it is evaluated. If the string is not recognised, then an error message is outputted
    :param string: string representing either a number or an operator (or unknown)
    :param is_digit: boolean representing if the string is a digit or not
    :param precedence: integer representing current precedence
    :return: integer representing new precedence
    """
    if is_digit:
        octal = is_octal(string)
        # If a number starts with 0 or -0, isn't a valid octal and isn't single-digit, then SRPN disregards it
        if octal is not None: evaluate_valid_number(string, octal)  # Turns the string into an integer (depending on octal if its in base 8 or 10) and appends it to the num_stack
    elif string == "d":
        use_operations_stack()  # d operator forces list operations to be used. E.g. "5 2 4 7 -*d* = " would force the -* to be used (in order_to_sort) before second * is evaluated
        display_num_stack()
    elif string in operation_dict:
        precedence = precedence_checker(string, precedence)
    elif string in command_operation_dict:
        append_to_num_stack(command_operation_dict[string]())
    else:
        print(UNRECOGNISED_OPERATOR.format(string))
    return precedence


def is_neg_num_start(is_number, string, i):
    """
    Checks whether the ith character of string is the start of a negative number
    :param is_number: boolean representing whether the program is in the middle of a number
    :param string: string representing part of the user input to analyse
    :param i: integer representing the index of the character we are interested in checking
    :return: boolean representing whether the ith character of string is the start of a negative number
    """
    return string[i] == "-" and not is_number and i != len(string) - 1 and string[i + 1].isdigit()


def read_valid_string(string):
    """
    Gets a string and evaluates it in a similar way to how the original SRPN does
    :param string: string representing part of the user input to analyse
    :return: None
    """
    op_precedence = len(order_to_sort)  # Setting the op_precedence to the lowest priority, meaning any operation will override it
    is_number = False
    number = ""
    for i in range(len(string)):
        if string[i].isdigit():  # Checks whether the ith character in the string is a digit
            if is_number:
                number += string[i]
            else:
                is_number = True
                number = string[i]
        elif is_neg_num_start(is_number, string, i):  # Checks whether the ith character in the string is the start of a negative number
            is_number = True
            number = string[i]
        else:
            if is_number:  # Evaluates the any number before evaluating the operation
                op_precedence = process_string(number, is_number, op_precedence)
                is_number = False
                number = ""
            op_precedence = process_string(string[i], is_number, op_precedence)
    if is_number: process_string(number, is_number, op_precedence)
    use_operations_stack()  # empties the operation_stack before next user input


def filter_comment(input_lst):
    """
    This function takes an input list and filters comments away from it, thus evaluating only non-comment strings
    :param input_lst: list of strings that make up the user's input
    :return: Boolean representing whether the program is in comment mode or not
    """
    global is_comment
    for string in input_lst:
        if len(string) > 120:  # If the code is over 120 characters then the program crashes.
            print(LONG_STRING)
            exit(EXIT_MSG.format(139))
        if string == "#":
            is_comment = not is_comment
            continue
        elif not is_comment:
            read_valid_string(string)  # If the string is in a comment mode then it is ignored.


def main():
    """
    The main program. Runs in an infinite loop asking the user for inputs to evaluate
    :return: None - Never exists the function unless the program crashes (for example division by 0)
    """
    random_init()
    while True: filter_comment(input().split())


if __name__ == "__main__":
    main()
