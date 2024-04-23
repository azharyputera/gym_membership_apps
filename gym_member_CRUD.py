from tabulate import tabulate
import getpass
import re
import datetime

users = {
    'admin': {'password': 'admin123', 'type': 'admin', 'visit_limit': None,'specialpass':'azhary123'},
    'andrian': {'password': 'gym123', 'type': 'member', 'visit_limit': 20,'member_valid':datetime.date(2024,6,20)},
    'valdi': {'password': 'gym123', 'type': 'regular', 'visit_limit': 5,'member_valid': None},
    'budianto': {'password': 'gym123', 'type': 'regular', 'visit_limit': 12,'member_valid':None},
    'fadhil': {'password': 'gym123', 'type': 'regular', 'visit_limit': 8,'member_valid':None},
}

list_package =[
    {
        'namapaket':'Package 1',
        'addvisit': 5,
        'harga':100000
    },
     {
        'namapaket':'Package 2',
        'addvisit': 10,
        'harga':175000
    },
     {
        'namapaket':'Package 3',
        'addvisit': 20,
        'harga':325000
    }
]
logged_in_users={}

def start ():  
    while True:
        print("""Welcome to SixPack Gym Apps
          
        1. Login
        2. Close Apps
          """)
        ToLogin = input('Enter your choice:')
        if ToLogin == '1':
            login()
        elif ToLogin == '2':
            quit_app()
        else: print('invalid input')
    
            

def login():
    print('\nLogin to SixPacks Membership Apps')
    username = input('Username:')
    password = getpass.getpass('Password:')
    
    if username in users:
        if users[username]['password'] == password:
            print(f'Login Succesfull, Welcome {username}')
            logged_in_users[username]={'has_visited':False}
            if users[username]['type'] == 'admin':
                admin_menu()
            else:
                main_menu(username)
        else: 
            print('Incorrect password')
            login()
    else:
        print('Username not found')
        login()

def admin_menu():
    while True:
        print("""\nAdmin Menu
        1. Display Visitors data
        2. Add visitors
        3. Delete Visitor
        4. Update Data
        5. Sort Data
        6. Log Out""")
        choice = input('Enter your choice:')
        
        if choice == '1':
            display_visitors()
            display_full_data()
        elif choice == '2':
            add_visitor()
        elif choice == '3':
            delete_visitors()
        elif choice == '4':
            update_visitor()
        elif choice == '5':
            sorted_visitors =sort_visitors(users)
            display_sorted_visitors(sorted_visitors)
        elif choice == '6':
            start()
            break
        else:
            print("Invalid choice.")

def main_menu(username):
    while True:
        print("""\n Main Menu
        1. Check My Data
        2. Purchase Visit Package
        3. Upgrade my membership
        4. Enter Gym
        5. Log out""")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            check_visitor_data(username)
        elif choice == '2':
            purchase_visit_package(username)
        elif choice == '3':
            upgrade_membership(username)
        elif choice == '4':
            enter_gym(username)
        elif choice == '5':
            logout(username)
            break
        else:
            print("\nInvalid choice.")

def display_visitors():
    print('\n List Visitor')
    header = ['index','Name','Membership Type','Visit Limit','Member Expiration Day']
    table = [[index,username,users[username]['type'],users[username]['visit_limit'],users[username]['member_valid']] for index,username in enumerate(users)if users[username]['type'] != 'admin']
    print(tabulate(table,headers=header,tablefmt="grid",showindex=False))
    
def display_full_data():
    full_data = input('\nDisplay full data as admin: (Y to continue) :')
    if full_data.upper() == 'Y':
        specialpass = getpass.getpass('Enter the password:')
        if users['admin']['specialpass'] == specialpass:
            print('\n List Visitor')
            header = ['Index','Account Name','Passwword','Membership Type','Visit Limit']
            table = [[index,username,users[username]['password'],users[username]['type'],users[username]['visit_limit']] for index,username in enumerate(users)if users[username]['type'] != 'admin']
            print(tabulate(table,headers=header,tablefmt="grid",showindex=False))
        else: 
            print('Incorrect password, go back to Admin Menu')
            return
    else:
        print('\n Go back to Admin Menu')
        return
    
    
       
def add_visitor():
    print("\nAdd New Visitor")
    while True:
        tambahtamu = input("Enter new visitor's username(x to quit): ").strip().lower()
        if tambahtamu.lower() == 'x':
            return
        
        if len(tambahtamu) < 5 or not re.match("^[a-zA-Z0-9]*$", tambahtamu):
            print('Invalid username, Must be at least 5 character and contain only letter/numbers')     
        elif tambahtamu.lower() in users:
            print("Error: Username already exists.")
        else: 
            break

    passwordtamu = input("Enter password for new visitor: ").strip()
    while len(passwordtamu) < 5 or not re.match("^[a-zA-Z0-9]*$", passwordtamu):
        print("Password must be longer than 5 characters and cannot contain simbols")
        passwordtamu = input("Enter password for new visitor: ")
    
    print('\nSixpact Gym member got 10% off!!')
    typetamu = input("Enter membership type (member/regular): ")
    while typetamu not in ['member', 'regular']:
        print("Invalid type. Please choose 'member' or 'regular'.")
        typetamu = input("Enter membership type (member/regular): ")
    

    print('Visitors data will be added, your current visit limit = 0')
    buyornot = input('Do you want to purchase visit point (Y/N) :')
    if buyornot.upper() == 'Y':
        display_package_menu()
        try:
            indexinput = int(input("Choose package u want to purchase: "))
            if 0<=indexinput<(len(list_package)+1):
                index_beli = indexinput -1
            
            harga = list_package[index_beli]['harga']
            if typetamu == 'member':
                totalharga = harga*0.9
            else: totalharga=harga
            print(f"\nTotal Harga: Rp{totalharga}")
            amount_paid = int(input("Enter payment amount: "))
            while True:
                if amount_paid < totalharga:
                    print("The amount of money you paid is not enough . Trasaction Cancelled.")
                    visitlimit=0
                else:
                    change = amount_paid - totalharga
                    visitlimit= list_package[index_beli]['addvisit']
                    print(f"Purchase successful.{list_package[index_beli]['addvisit']}  visits have been added to your account.")
                    print(f"Transaction Complete: your change isRp{change:.2f}")
                break
            else: 
                print('Invalid input, go back to Main menu')
        except ValueError:
            print('Please enter correct input')
    else : visitlimit = 0
    
    if typetamu == 'member':
        today = datetime.date.today()
        memberdate = today + datetime.timedelta(days=365)
    else: memberdate=None
    
    users[tambahtamu] = {
        'password': passwordtamu,
        'type': typetamu,
        'visit_limit': visitlimit,
        'member_valid':memberdate
    }
    print(f"Visitor {tambahtamu} added successfully.")

def delete_visitors():
    display_visitors()
    while True:
        index_input = input('Please enter the index of visitor to delete:')
        if index_input.isdigit():
            indexdelete = int(index_input)
            if 0 <= indexdelete < len(users):
                usernameremoved = list(users.keys())[indexdelete]
                del users[usernameremoved]
                print('Visitor deleted successfully')
                break
            else:
                print('Index out of range, please enter a valid index.')
        else:
            print('Invalid input. Please enter a valid integer index.')
            
def update_visitor():
    display_visitors()
    index_update_input= input('\nSelect Index of Visitors to update :')
    if index_update_input.isdigit():
        index_update= int(index_update_input)
        if 0 <= index_update <len(users):
            usernameupdate = list(users.keys())[index_update]
            data_update = input('Select Data to Update (username,password,type,visitlimit):')
            while data_update.lower() not in ['username', 'password','type','visitlimit']:
                print("Invalid type. Please choose 'username'or 'password' or'visit_limit'.")
                data_update = input("Select data to update (username,password,type,visitlimit) : ")
            
            if data_update.lower() == 'username':
                while True:
                    databaru = input('\nEnter new username :').lower().strip()
                
                    if len(databaru) < 5 or not re.match("^[a-zA-Z0-9]*$", databaru):
                        print('Invalid username, Must be at least 5 character and contain only letter/numbers')     
                    else: 
                        users[databaru] = users.pop(usernameupdate)
                        print ('Update Success !')
                        display_visitors()
                        break
                
            elif data_update.lower() == 'password':
                
                databaru = input('\nEnter new password :').strip()
                while len(databaru) < 5 or not re.match("^[a-zA-Z0-9]*$", databaru):
                    print("Password must be longer than 5 characters and cannot contain simbols")
                    databaru = input('\nEnter new password :')
                    
                users[usernameupdate]['password'] = databaru
                print ('Update Success !')
                display_visitors()
                
            elif data_update.lower() == 'type':
                databaru = input('\nUpdate membership type (member/regular) :')
                while databaru not in ['member', 'regular']:
                    print("Invalid type. Please choose 'member' or 'regular'.")
                    databaru = input("Update membership type (member/regular): ")
                users[usernameupdate]['type'] = databaru
                if databaru == 'member':
                    today = datetime.date.today()
                    memberdate = today + datetime.timedelta(days=365)
                else: memberdate = None
                users[usernameupdate]['member_valid'] = memberdate
                print ('Update Success !')
                display_visitors()
                
            else:
                databaru = input('\nEnter the visit limit :')
                while not databaru.isdigit():
                    print('invalid input, please enter a number')
                    databaru = input('\nMasukkan Visit Limit baru :')
                users[usernameupdate]['visit_limit'] = int(databaru)
                print ('Update Success !')
                display_visitors()
                
        else : print('index out of range, please enter a valid index')
    
    else: print('Invalid input, please enter a number')
        
def sort_visitors(users):
    filtered_users = {k: v for k, v in users.items() if v['type'] != 'admin'}
    sorted_visitors = sorted(filtered_users.items(), key=lambda x: (x[1]['type'], x[0]))
    return sorted_visitors

def display_sorted_visitors(sorted_visitors):
    print('\n List of Visitors:')
    header = ['Index', 'Name', 'Membership Type', 'Visit Limit','Member Exp Date']
    table = [[index+1, username, visitor['type'], visitor['visit_limit'],visitor['member_valid']] for index, (username, visitor) in enumerate(sorted_visitors)]
    print(tabulate(table, headers=header, tablefmt="grid", showindex=False))

        
def check_visitor_data(username):
    print(f"You have {users[username]['visit_limit']} visits left.")
    tipemember = users[username]['type']
    print(f'Your membership type is {tipemember}')
    if tipemember == 'member':
        membership_end = users[username]['member_valid']
        print(f'Your membership valid until {membership_end.strftime("%Y-%m-%d")}')
    
  
def display_package_menu():
    print("\nPackage Menu")
    header =['Index','Package Name','Visit Point','Price(Rp)']
    table= [[index+1,list_package['namapaket'],list_package['addvisit'],list_package['harga']]for index, list_package in enumerate(list_package)]
    print(tabulate(table,headers=header,tablefmt="grid"))


def purchase_visit_package(username):
    display_package_menu()
    try:
        indexinput = int(input("\nChoose the package u want to purchase: "))
        if 0<=indexinput<(len(list_package)+1):
            index_beli = indexinput -1
            
            harga = list_package[index_beli]['harga']
            if users[username]['type'] == 'member':
                totalharga = harga*0.9
            else: totalharga=harga
            print(f"\nTotal Harga: Rp{totalharga}")
            amount_paid = int(input("Enter your payment amount: "))
            while True:
                if amount_paid < totalharga:
                    print("The amount you paid is not enough, Transaction cancelled.")
                else:
                    change = amount_paid - totalharga
                    users[username]['visit_limit'] += list_package[index_beli]['addvisit']
                    print(f"Purchase successful.{list_package[index_beli]['addvisit']}  visits have been added to your account.")
                    print(f"Transaction Complete. Your change is: Rp{change:.2f}")
                break
        else: 
            print('Invalid input, go back to Main menu')
    except ValueError:
        print('Please enter correct input')
    

def upgrade_membership(username):
    try:
        if username in users and users[username]['type'] == 'regular':
            print('Membership got 10% discount for 1 year!!')
            hargaupgrade = 150000
            print(f"\nTotal Price: Rp150.000/Year")
            amount_paid = int(input("Enter your payment amount: "))
            while True:
                if amount_paid < hargaupgrade:
                    print("The amount you paid is not enough, Transaction cancelled.")
                else:
                    change = amount_paid - hargaupgrade
                    users[username]['type'] = 'member'
                    today = datetime.date.today()
                    memberdate = today + datetime.timedelta(days=365)
                    users[username]['member_valid'] = memberdate
                    print(f"{username} has been successfully upgraded to a member.")
                    print(f"Transaction Complete, Your change is : Rp{change:.2f}")
                break   
        else: 
            print(f"{username} is already a member.")
    except ValueError:
        print('Input ERROR,Please enter correct input')

def enter_gym(username):
    if username not in logged_in_users:
        print("Please login first.")
        return
    if logged_in_users[username]["has_visited"]:
        print("You have already visited the gym during this session.")
        return
    if users[username]["visit_limit"] is None or users[username]["visit_limit"] > 0:
        if users[username]["visit_limit"] is not None:
            users[username]["visit_limit"] -= 1
        logged_in_users[username]["has_visited"] = True
        print("Welcome to the gym!")
    else:
        print("You have exceeded your visit limit.") 
   
def logout(username):
    if username in logged_in_users:
        del logged_in_users[username]
        print("Logged out successfully.")
    else:
        print("You are not logged in.")     
        
def quit_app():
    print("Thank you for using SixPack Gym Membership App. Goodbye!")
    exit()

if __name__ == "__main__":
    start()