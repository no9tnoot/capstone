# Sian Wood
# 11/09/2023
# check if user enters valid username and password

login_details = {
  "wdxsia001": "sian",
  "brnpet038": "peter",
  "ryneri002": "molly"
}

def check_login_details(usr, pswd):
    if login_details[usr] == pswd:
        return True 
    return False

def get_eng(level):
    match level:
        case "easy":
            return ("Show all the data in the OFFICES table.")
            # select * from OFFICES
        case "medium":
            return("Find the average BUYPRICE in the PRODUCTS table.")
            # select avg(BUYPRICE) from PRODUCTS
        case "hard":
            return("Show each EMPLOYEENUMBER in the EMPLOYEES table along with the CITY of the associated OFFICECODE.")
            # select EMPLOYEENUMBER, CITY from EMPLOYEES natural join OFFICES

# print(get_eng("easy"))
