from config import read_yaml
import re


def regex_and_length(**data):
    dob_condition = re.compile(read_yaml.dob_condition_expression)
    errors = []
    if "email" in data.keys():
        if len(data.get("email")) > 150:
            errors.append("email address should containt no more than 150 characters.")
        if not re.search(read_yaml.email_condition, data.get("email")):
            errors.append("Invalid format for email.")
    if "username" in data.keys():
        if not re.search(read_yaml.username_condition, data.get("username")):
            errors.append(
                "Invalid format for username. Only english alphabets, digits, hyphens and underscores are allowed.")
    if "email" in data.keys():
        if len(data.get("email")) > 150:
            errors.append("email address should containt no more than 150 characters.")
    if "firstName" in data.keys():
        if len(data.get("firstName")) > 100:
            errors.append("first name should containt no more than 100 characters.")
        if not re.search(read_yaml.name_condition, data.get("firstName")):
            errors.append("Invalid format for first name. Only english alphabets are allowed.")
    if "lastName" in data.keys():
        if len(data.get("lastName")) > 100:
            errors.append("last name should containt no more than 100 characters.")
        if not re.search(read_yaml.name_condition, data.get("lastName")):
            errors.append("Invalid format for last name. Only english alphabets are allowed.")
    if "dob" in data.keys():
        if not re.search(dob_condition, data.get("dob")):
            errors.append("DOB must have either of the three formats \'dd/mm/yyyy\' \'dd.mm.yyyy\' \'dd-mm-yyyy\'")
    if "gender" in data.keys():
        if not (data.get("gender") == "M" or data.get("gender") == "F" or data.get("gender") == "O"):
            errors.append("Use \'M\' for male, \'F\' for female or \'O\' for others")
    return errors


# def regex_and_length_provider(**data):
#     errors = []
#     # if len(data.get("email")) > 150:
#     #     errors.append("email address should containt no more than 150 characters.")
#     # if data.get("firstName") and len(data.get("firstName")) > 100:
#     #     errors.append("first name should containt no more than 100 characters.")
#     # if data.get("lastName") and len(data.get("lastName")) > 100:
#     #     errors.append("last name should containt no more than 100 characters.")
#     if not re.search(patterns.get("email_condition"), data.get("email")):
#         errors.append("Invalid format for email.")
#     if not re.search(patterns.get("username_condition"), data.get("username")):
#         errors.append(
#             "Invalid format for username. Only english alphabets, digits, hyphens and underscores are allowed.")
#     if data.get("firstName") and not re.search(patterns.get("name_condition"), data.get("firstName")):
#         errors.append("Invalid format for first name. Only english alphabets are allowed.")
#     if data.get("lastName") and not re.search(patterns.get("name_condition"), data.get("lastName")):
#         errors.append("Invalid format for last name. Only english alphabets are allowed.")
#     return errors


def check_values(**data):
    errors = regex_and_length(**data)
    return errors


def check_values_provider(**data):
    errors = regex_and_length_provider(**data)
    return errors
