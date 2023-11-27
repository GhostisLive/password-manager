import os
from cryptography.fernet import Fernet
import mysql.connector as con
import os.path
import os
from dotenv import load_dotenv

load_dotenv()

conn = con.connect(
   host='localhost',
   user=os.environ["DBUSER"],
   passwd=os.environ["DBPASS"],
   database='pass'
)

def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

if not os.path.exists('key.key'):
    write_key()

with conn.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS pass (name VARCHAR(255) NOT NULL, pass VARCHAR(255) NOT NULL)")

if not os.path.exists('mast_password.key'):
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


def view():
    with conn.cursor() as cursor:
       cursor.execute("SELECT * FROM pass")
       results = cursor.fetchall()
       if not len(results):
          print("You do not have any passwords saved!")
          return
       
       for (user, passw) in results:
          password = fer.decrypt(passw.encode()).decode()
          print(f"\nUser: {user}\nPassword: {password}\n")
      

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    with conn.cursor() as cursor:
       vals = (name, fer.encrypt(pwd.encode()).decode())
       cursor.execute("INSERT INTO pass (name, pass) VALUES (%s, %s)", vals)

       conn.commit()


def main():
    while True:
        master_password = input("Enter your master password: ")
        key_user = read_key() + master_password.encode()
        if key_os != key_user:
            print("Your have entered wrong password! TRY AGAIN!")
            continue
      
        print("Do you want to add a new password or view existing one? ")
        choice = input("N -> new password \nV -> view password \nQ -> quit \nEnter your choice: ").upper()

        if choice == 'N':
            add()
        elif choice == 'V':
           view()
        elif choice == 'Q':
           print("Quitting...")
           break
        else:
           print("Choose a valid option.")
           continue

        print("Do u want to continue?")
        exit = input("Yes -> Y \nNo -> N \n").upper()

        if exit == "N":
            print("Quitting...")
            break

main()
