import mysql.connector as sql 

#conection body
mydb=sql.connect(host="localhost",user="root",password="",database="Employee_Data_Management")


def menu(): #status - 1[completed] 2[completed] 3[completed] 4[completed] 5[completed]
    print("Welcome to Employee Data Management software\n")
    print(" 1.Add Employee Data\n","2.Remove Employee Data \n","3.Configure Employee Data \n","4.Veiw Data \n","5.Exit \n")
    choice = int(input("Select a option(0 to abort, 1-5): "))
    if choice == 1:
        add_data()
    elif choice == 2:
        remove_data()
    elif choice == 3:
        config_data()
    elif choice == 4:
        view_data()
    elif choice == 5:
        obj_cursor.close()
        print("Exiting... \n See You Next Time!")
    else:
        print("Wrong Input!")
        menu()


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
            menu()

def remove_data(): #single employee at a time
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

def config_data(): #limited feilds to reduce lines of code and time
    upg_emp=int(input("Enter Employee No. to be configured: "))
    upg_item=input("Fields that can be updated:\n Age (A)\n Role (R)\n Department (D)\n Salary (S)\n Enter the Field: ") 
    obj_cursor = mydb.cursor()
    if upg_item.upper() == 'A':
        age=int(input("Enter the Age: "))
        obj_cursor.execute("update employee set Age={0} where Emp_no = {1}".format(age,upg_emp))
        mydb.commit()
        menu()

    elif upg_item.upper() == 'R':
        role=input("Enter the role: ")
        obj_cursor.execute("update employee set Role='{0}' where Emp_no = {1}".format(role,upg_emp))
        mydb.commit()
        menu()

    elif upg_item.upper() == 'D':
        dept=input("Enter the Department: ")
        obj_cursor.execute("update employee set Dept='{0}' where Emp_no = {1}".format(dept,upg_emp))
        mydb.commit()
        menu()

    elif upg_item.upper() == 'S':
        salary=input("Enter the Salary: ")
        obj_cursor.execute("update employee set Salary={0} where Emp_no = {1}".format(salary,upg_emp))
        mydb.commit()
        menu()

    else:
        print("Feild Not Found!")
        menu()
        

def view_data(): #making it simple
    choice = input("Do want view the whole table(T) or single row(R)?: ")
    if choice.upper() == 'T':
        obj_cursor=mydb.cursor()
        obj_cursor.execute("select * from employee")
        display = obj_cursor.fetchall()
        for row in display:
            print(row)
        menu()
    elif choice.upper() == "R":
        emp_no=int(input("Enter Employee No.: "))
        obj_cursor=mydb.cursor()
        obj_cursor.execute("select * from employee where Emp_no = {0}".format(emp_no))
        display = obj_cursor.fetchone()
        if display: # checks if found
            print(display)
            menu()
        else:
            print("Employee not found!")
            menu()
    else:
        print("Wrong Input!")
        menu()

menu()

#A school project
#By Ak,Praveen,Dharun,Kevin