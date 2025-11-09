import mysql.connector as sql 
import os #to run 'setup-sql.sh' 

#conection body
mydb=sql.connect(host="localhost",user="root",password="project",database="Employee_Data_Management")


def menu(): #status - 1[completed] 2[pending] 3[pending] 4[pending] 
    print("Welcome to Employee Data Management software\n")
    print(" 1.Add Employee Data\n","2.Remove Employee Data \n","3.Configure Employee Data \n","4.Veiw Data \n")
    choice = int(input("Select a option(0 to abort, 1-5): "))
    if choice == 1:
        add_data()
    elif choice == 2:
        remove_data()
    elif choice == 3:
        config_data()
    elif choice == 4:
        view_data()


def add_data(): # data=[empno,name,gender,age,role,dept,salary]
    while True:
        emp_no=int(input("Enter Employee's no.: "))
        name=input("Enter Employee's Name: ")
        gender=input("Enter gender(M/F): ")
        age=int(input("Enter Employee's age: "))
        role=input("Enter the Employee's role: ")
        dept=input("Enter Department: ")
        salary=int(input("Enter Emplyee's Salary: "))
        obj_cursor=mydb.cursor()
        obj_cursor.execute('insert into employee values("{emp_no}","{name}","{gender}","{age}","{role}","{dept}","{salary}")')
        ch=input("wanna enter more employee's data? (Y/N): ")
        if ch.upper() == 'N' or ch.upper != 'Y': #just trying to be effecient ;)
            break

def remove_data():
    del_emp=int(input("Enter Employee No. to be removed: "))
    try: #checking if that emp no. exists or not 
        obj_cursor=mydb.cursor()
        obj_cursor.execute('delete from employee where Emp_no = "{del_emp}"')
    except:
        print("Employee No. Not Found!")

def config_data():
    conf_emp=int(input("Enter the Employee No. to be configured: "))
    try: #checking if that emp no. exists or not 
        obj_cursor=mydb.cursor()
        obj_cursor.execute("update")
    except:
        print("Employee No. Not Found!")