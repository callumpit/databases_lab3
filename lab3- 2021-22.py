import sqlite3

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
    # Set of sqlite queries stored as class variables for use in methods.
    sql_create_table = "create table if not exists {} (employeeID INTEGER UNSIGNED NOT NULL, title VARCHAR(20), forename VARCHAR(20), surname VARCHAR(20), email VARCHAR(20), salary FLOAT)"
    sql_insert = "insert into {} (employeeID, title, forename, surname, email, salary) values (?,?,?,?,?,?)"
    sql_select_all = "select * from {} order by {}"
    sql_search = "select * from {} where employeeID=?"
    sql_update_data = "update {} set {}=? where employeeID=?"
    sql_delete_data = "delete from {} where employeeID=?"
    sql_drop_table = "drop table {}"

    def __init__(self):
        """
        Here the constructor creates the database if it doesn't already exist.
        """
        try:
            self.conn = sqlite3.connect("EmployeeTables.db")
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_connection(self):
        """
        This function connects to the database enabling functions to interact with it.
        """
        self.conn = sqlite3.connect("EmployeeTables.db")
        self.cur = self.conn.cursor()

    def check_exists(self, table_name):
        """
        This function takes a table name string as an argument and checks if it exists in the database.
        If it does, the function returns True, if not it returns False.
        """
        try:
            self.get_connection()
            check = self.cur.execute(
                "select count(*) from sqlite_master where type = 'table' and name = '{}'".format(table_name))
            if self.cur.fetchone()[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def create_table(self, table_name):
        """
        Here we can create employee tables of different names e.g. techEmployees, teachingEmployees.
        Takes desired table name string as an argument, if the table name does not already exist in
        the database, a table of this name is created. If a table of given name does already exist in the 
        database a warning message is printed. No return.
        """
        try:
            # check is given table exists in database
            if self.check_exists(table_name) == True:
                print("This table is already created")
            else:
                self.get_connection()
                # create the table
                self.cur.execute(
                    self.sql_create_table.format(table_name))
                self.conn.commit()
                print("Table \"{}\" created successfully".format(table_name))
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def list_tables(self):
        """
        This function returns a list of all table names in the database and prints them out.
        """
        try:
            self.get_connection()
            self.cur.execute(
                "select name from sqlite_master where type='table';")
            # print out table names
            tables = self.cur.fetchall()
            List = []
            for table in tables:
                List.append(table[0])
                print(table[0])
            return List

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def delete_table(self, table_name):
        """
        This function takes a table name string as an argument and upon confirmation, deletes it from the database. No return.
        """
        try:
            # check given table exists
            if self.check_exists(table_name) == True:
                self.get_connection()
                userSure = None
                while userSure != "y" and userSure != "n":
                    # confirm user wants to delete the given table in case of mistake.
                    userSure = str(input(
                        "Are you sure you want to delete the table: {} ? y/n: ".format(table_name)))
                if userSure == "y":
                    self.cur.execute(
                        self.sql_drop_table.format(table_name))
                    self.conn.commit()
                    print("{} deleted from database".format(table_name))

            else:
                print("Table does not exist")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def insert_data(self, table_name):
        """
        This function takes a table name string as an argument and, if it exists, inserts information for a 
        new employee into the table. Information is given by user input. No return.
        """
        try:
            # check given table exists
            if self.check_exists(table_name) == True:
                self.get_connection()

                # check which entries user wishes to update and get user input for the
                # required changes
                emp = Employee()
                emp.set_employee_id(int(input("Enter Employee ID: ")))
                emp.set_employee_title(
                    str(input("Enter Employee Title: ")))
                emp.set_forename(str(input("Enter Employee Forename: ")))
                emp.set_surname(str(input("Enter Employee Surname: ")))
                emp.set_email(str(input("Enter Employee Email: ")))
                emp.set_salary(str(input("Enter Employee Salary: ")))
                print(tuple(str(emp).split("\n")))

                self.cur.execute(self.sql_insert.format(
                    table_name), tuple(str(emp).split("\n")))

                self.conn.commit()
                print("Inserted data successfully")

            else:
                print("Table does not exist")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all(self, table_name):
        """
        This function takes a table name string as an argument as, if the table exists in the database, prints all
        data from the table. No return.
        """
        try:
            # check given table exists
            if self.check_exists(table_name) == True:
                self.get_connection()
                order = str(
                    input("Enter ordering format (e.g. employeeID, forename, surname, salary): "))
                self.cur.execute(self.sql_select_all.format(table_name, order))
                # display all data in table
                results = self.cur.fetchall()
                for row in results:
                    print(row)

            else:
                print("Table does not exist")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_data(self, table_name, employeeID=None):
        """
        This function takes a table name string as an argument as well as an optional
        Employee ID int. If optional argument is not given it will ask for the employee id
        number via user input. The given table will be searched for the given employee id number 
        and the corresponding data is printed out. If the given id number cannot be found in the
        given table or the given table cannot be found in the database, the function will return
        False. Otherwise there is no return.
        """
        try:
            if self.check_exists(table_name) == True:
                self.get_connection()
                # Supply employee id if not given in argument
                if employeeID == None:
                    employeeID = int(input("Enter Employee ID: "))
                self.cur.execute(self.sql_search.format(
                    table_name), (employeeID,))
                result = self.cur.fetchone()
                if type(result) == type(tuple()):
                  # display employee information
                    for index, detail in enumerate(result):
                        if index == 0:
                            print("Employee ID: " + str(detail))
                        elif index == 1:
                            print("Employee Title: " + detail)
                        elif index == 2:
                            print("Employee Name: " + detail)
                        elif index == 3:
                            print("Employee Surname: " + detail)
                        elif index == 4:
                            print("Employee Email: " + detail)
                        else:
                            print("Salary: " + str(detail))

                else:
                    print("No Record Found in Database")
                    return False

            else:
                print("Table does not exist")
                return False

        except Exception as e:
            print(e)
            return False

        finally:
            self.conn.close()

    def update_data(self, table_name):
        """
        This function takes a table name string as its argument and, if the table exists in the database, will
        ask for the user to input an employee id to search for in the table. If the employee id is found in the
        table, each column of the table for that row can be either updated or left the same by a series of user
        inputs. No return.
        """
        try:
            if self.check_exists(table_name) == True:
                empID = int(
                    input("Enter Employee ID of record to be updated: "))
                print("\n")

                # display record user wishes to update
                print("RECORD TO UPDATE: ")
                update = self.search_data(table_name, empID)
                if update != False:
                    print("\n")

                    # Update Employee ID
                    self.get_connection()
                    changeID = None
                    while changeID != "y" and changeID != "n":
                        changeID = str(input("Change Employee ID? y/n: "))
                    if changeID == "y":
                        newID = int(input("Change Employee ID to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "employeeID"), (newID, empID))
                        self.conn.commit()
                        print("Employee ID Updated")

                    # Update Employee title
                    changetitle = None
                    while changetitle != "y" and changetitle != "n":
                        changetitle = str(
                            input("Change Employee title? y/n: "))
                    if changetitle == "y":
                        newtitle = str(input("Change Employee title to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "title"), (newtitle, empID))
                        self.conn.commit()
                        print("Employee title Updated")

                    # Update Employee first name
                    changefname = None
                    while changefname != "y" and changefname != "n":
                        changefname = str(
                            input("Change Employee forename? y/n: "))
                    if changefname == "y":
                        newforename = str(
                            input("Change Employee forename to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "forename"), (newforename, empID))
                        self.conn.commit()
                        print("Employee forename Updated")

                    # Update employee surname
                    changesname = None
                    while changesname != "y" and changesname != "n":
                        changesname = str(
                            input("Change Employee surname? y/n: "))
                    if changesname == "y":
                        newsurname = str(input("Change Employee surname to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "surname"), (newsurname, empID))
                        self.conn.commit()
                        print("Employee surname Updated")

                    # Update Employee email
                    changeemail = None
                    while changeemail != "y" and changeemail != "n":
                        changeemail = str(
                            input("Change Employee email? y/n: "))
                    if changeemail == "y":
                        newemail = str(input("Change Employee email to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "email"), (newemail, empID))
                        self.conn.commit()
                        print("Employee email Updated")

                    # Update Employee salary
                    changesalary = None
                    while changesalary != "y" and changesalary != "n":
                        changesalary = str(
                            input("Change Employee salary? y/n: "))
                    if changesalary == "y":
                        newsalary = float(input("Change Employee salary to: "))
                        self.cur.execute(self.sql_update_data.format(table_name,
                                                                     "salary"), (newsalary, empID))
                        self.conn.commit()
                        print("Employee salary Updated")

                else:
                    print("Table does not exist")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def delete_data(self, table_name):
        """
        This function takes a table name string as an input and, if the table exists in the database,
        will ask the user to input an employee id number. If this number is found in the table, upon 
        confirmation, the corresponding record is deleted from the table. No return.
        """
        try:
            if self.check_exists(table_name) == True:
                empID = int(
                    input("Enter Employee ID of record to be deleted: "))
                print("\n")
                # Display record about to be deleted
                print("RECORD TO DELETED: ")
                delete = self.search_data(table_name, empID)
                if delete != False:
                  # Confirm user wants to delete record incase of mistake
                    check = str(
                        input("Are you sure you want to delete this record? y/n: "))
                    if check == "y":
                        self.get_connection()
                        self.cur.execute(
                            self.sql_delete_data.format(table_name), (empID,))
                        self.conn.commit()

            else:
                print("Table does not exist")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def show_all_data(self):
        """
        This function displays all tables in the database allowing the user to order each one
        as they wish. No Return.
        """
        try:
            tables = self.list_tables()
            for i in tables:
                print("Table Name: {}".format(i))
                self.select_all(i)
                print("\n")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()


class Employee:
    def __init__(self):
        self.employeeID = 0
        self.empTitle = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    def set_employee_id(self, employeeID):
        self.employeeID = employeeID

    def set_employee_title(self, empTitle):
        self.empTitle = empTitle

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

    def get_employee_id(self):
        return self.employeeId

    def get_employee_title(self):
        return self.empTitle

    def get_forename(self):
        return self.forename

    def get_surname(self):
        return self.surname

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def __str__(self):
        return str(self.employeeID)+"\n"+self.empTitle+"\n" + self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# The main function will parse arguments.
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.

# while True:
# if __name__ == '__main__':
while True:
    print("\n Menu:")
    print("**********")
    print(" 1. Create New Employee table")
    print(" 2. Insert data into an Employee table")
    print(" 3. Display all data from an Employee table")
    print(" 4. Search for an employee in a table")
    print(" 5. Update a record in an Employee table")
    print(" 6. Delete a record in an Employee table")
    print(" 7. Delete a table from database")
    print(" 8. List all tables in database")
    print(" 9. Show all table data")
    print(" 10. Exit\n")

    __choose_menu = None
    # Ensure entry is a valid option
    while type(__choose_menu) != int:
        try:
            choice = int(input("Enter your choice: "))
            if choice >= 1 and choice <= 10:
                __choose_menu = choice
            else:
                # Give error message for invalid entries
                print("Invalid Entry, Please Try Again!!")
        except ValueError:
            print("Invalid Entry, Please Try Again!!")
    # create instance of dp_ops class
    db_ops = DBOperations()

    # create new employee table
    if __choose_menu == 1:
        table_name = str(
            input("Enter the name of the table you wish to create: "))
        db_ops.create_table(table_name)

    # insert data into employee table
    elif __choose_menu == 2:
        insert_into = str(
            input("Enter name of the table you wish to insert data into: "))
        print("\n")
        db_ops.insert_data(insert_into)

    # display all data from an employee table
    elif __choose_menu == 3:
        print("\n")
        display = str(
            input("Enter name of the table whose data you wish to display: "))
        print("\n")
        db_ops.select_all(display)

    # search for an employee in a table
    elif __choose_menu == 4:
        search = str(input("Enter name of the table you wish to search: "))
        db_ops.search_data(search)

    # update an employee record in a table
    elif __choose_menu == 5:
        record = str(
            input("Enter name of the table where record exists: "))
        db_ops.update_data(record)

    # delete an employee record in a table
    elif __choose_menu == 6:
        record = str(
            input("Enter name of the table where record exists: "))
        db_ops.delete_data(record)

    # delete a table from the database
    elif __choose_menu == 7:
        delete = input("Enter name of table you wish to delete: ")
        db_ops.delete_table(delete)

    # list all tables in the database
    elif __choose_menu == 8:
        print("table names in database: ")
        print("\n")
        db_ops.list_tables()

    # Display all database tables
    elif __choose_menu == 9:
        print("tables in database: ")
        print("\n")
        db_ops.show_all_data()

    # quit programme
    elif __choose_menu == 10:
        exit(0)

    else:
        print("Invalid Choice")
