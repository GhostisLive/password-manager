import os
os.system('cls') or None
from cryptography.fernet import Fernet
import os.path
import os

def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb')as key_file:
        key_file.write(key)

exists =  os.path.exists('key.key')
if not exists:
    write_key()



exist = os.path.exists('mast_password.key')       #checking if mast_password.key exists
if exist == True:
    pass
else:
    while True:
     mast_pwd = input("Enter new password: ")
     mast_pwd1 = input("Enter the password again: ")
     if mast_pwd == mast_pwd1:
      with open('mast_password.key','a') as f:
        f.write(mast_pwd)
        break
         
     else:
       print("Your password don't match!")
       continue
    
    
def master_key():
    file1 = open("mast_password.key", "rb") 
    m_key = file1.read()
    file1.close()
    return m_key

def read_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key 


master_pwd = master_key()
key_os = read_key() + master_pwd
fer= Fernet(key_os)

'''def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb')as key_file:
        key_file.write(key)'''

def view():
    with open('password.txt','r') as f:
        for line in f.readlines():
            data= line.rstrip("|")
            user, passw = data.rsplit("|",1)
            password = fer.decrypt(passw.encode())
            password1 = password.decode()
            print(f"User: {user} \nPassword: {password1}")

            
            

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    with open('password.txt','a') as f:
        f.write(name + " | " + fer.encrypt(pwd.encode()).decode() + "\n")


    
    

while True:
    master_password = input("Enter your master password: ")
    key_user = read_key() + master_password.encode()
    if key_os == key_user:
     print("Do you want to add a new password or view existing one? ")
     choice = input("N -> new password \nV -> view password \nQ -> quit \nEnter your choice: ")
     choice = choice.upper()
     if choice == 'N':
        add()
     elif choice =='V':
        if os.path.exists('password.txt') == True:
            view()
        else:
            print("You do not have any password saved!")
     elif choice =='Q':
        print("Quitting...")
        break
     else:
        print("Choose a valid option!")
        continue
    else:
        print("Your have entered wrong password! TRY AGAIN!")     
        continue
    print("Do u want to continue?")
    exit = input("Yes -> Y \nNo -> N \n")
    exit = exit.upper()

    if exit == "N":
        print("Quitting...")
        break
    else:
        continue

