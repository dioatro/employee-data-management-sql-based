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
        obj_cursor.execute("insert into employee values({0},'{1}','{2}',{3},'{4}','{5}',{6})".format(emp_no,name,gender,age,role,dept,salary))
        mydb.commit()
        ch=input("wanna enter more employee's data? (Y/N): ")
        if ch.upper() == 'N': #just trying to be effecient ;)
            mydb.close()
            menu()

def remove_data():
    del_emp=int(input("Enter Employee No. to be removed: "))
    obj_cursor = mydb.cursor()
    obj_cursor.execute("DELETE FROM employee WHERE Emp_no = {0}".format(del_emp))
    mydb.commit()
    if obj_cursor.rowcount == 0:
        print("Employee No. not found!")
        menu()
    else:
        print("Employee removed successfully!")
        menu()

#def config_data():
    

menu()