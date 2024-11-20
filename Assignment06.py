# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   EFox,11/19/2024,Created Script
# ------------------------------------------------------------------------------------------ #
import json


# Data --------------------------------------- #
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a student for a course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

menu_choice: str  # hold the choice made by the user.
students: list[dict[str,str,str]] = []  # a table of student data


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog: (Who, When, What)
    EFox,11/19/2024,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        A function to read the data from a specified JSON file, and into list.

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created Function

        :return: list of JSON file data
        """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages(message = 'File must exist before running this script!', error = e)
        except Exception as e:
            IO.output_error_messages(message = 'There was a non-specific error', error = e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data:list):
        """
        A function to write the data to a specified JSON file from a list

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created Function
        """
        try:
            file = open(file_name,'w')
            json.dump(student_data,file)
            file.close()
        except TypeError as e:
            IO.output_error_messages(message = 'Are the file contents in a valid JSON format?', error= e)
        except Exception as e:
            IO.output_error_messages(message = 'There was a non-specific error', error = e)
        finally:
            if file.closed == False:
                file.close()

        print('The following data was saved to file!')
        IO.output_student_courses(student_data = student_data)


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that regulate data shown
    to and collected from the user

    ChangeLog: (Who,When,What)
    EFox,11/19/2024,Created Class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user

         ChangeLog: (Who, When, What)
         EFox,11/19/2024,Created Function

         :return: None
         """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of choices to the user

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created Function

        :return: None
        """
        print()
        print(MENU)
        print()

    @staticmethod
    def input_menu_choice(menu: str) -> str:
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created function

        :return: string with the user's choice
        """
        menu_choice = input("What would you like to do: ")
        while menu_choice not in ['1','2','3','4']:
            IO.output_error_messages('Please enter a number between 1 and 4.')
            menu_choice = input("What would you like to do: ")
        return menu_choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the student data to the user

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created function

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the first name, last name, and course name from the user

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created Function

        :return: None
        """
        student_first_name: str = ''  # holds the first name of a student entered by the user.
        student_last_name: str = ''  # holds the last name of a student entered by the user.
        course_name: str = ''  # holds the name of a course entered by the user.
        student_data: dict = {}  # one row of student data
        try:
            student_first_name = input("Enter the student's first name: ")
            if IO.has_numeric(student_first_name):
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if IO.has_numeric(student_last_name):
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student_data)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message = 'The value is not valid.', error = e)
        except Exception as e:
            IO.output_error_messages(message = 'Error: There was a problem with your entered data.', error = e)

    @staticmethod
    def has_numeric(input_string: str):
        """ This function loops through each character in a string and returns a boolean value of True
        if any character is numeric

        ChangeLog: (Who, When, What)
        EFox,11/19/2024,Created Function

        :return: Boolean
        """
        for char in input_string:
            if char.isnumeric():
                return True
        return False
# End of class and function definitions


# When the program starts, read the file data into a list of lists (table)
students = FileProcessor.read_data_from_file(file_name = FILE_NAME, student_data = students)

# Present and Process the data
while True:
    # Present the menu of choices
    print(MENU)
    # Store user menu choice
    menu_choice = IO.input_menu_choice(menu = MENU)

    if menu_choice == '1':
        # Input user data
        IO.input_student_data(student_data = students)
        continue

    elif menu_choice == '2':
        # Present the current data
        IO.output_student_courses(student_data = students)
        continue

    elif menu_choice == '3':
        # Save the data to a file
        FileProcessor.write_data_to_file(file_name = FILE_NAME, student_data = students)
        continue

    elif menu_choice == '4':
        # Stop the loop
        break

print("Program Ended")
