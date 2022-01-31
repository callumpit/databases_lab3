import sqlite3

# Define DBOperation class to manage all data into the database. 
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = "create table if not exists "

  sql_create_table = "create table TableName"

  sql_insert = ""
  sql_select_all = "select * from TableName"
  sql_search = "select * from TableName where EmployeeID = ?"
  sql_update_data = ""
  sql_delete_data = ""
  sql_drop_table = ""
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("DBName.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("DBName.db")
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table)
      self.conn.commit()
      print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      emp = Employee()
      emp.set_employee_id(int(input("Enter Employee ID: ")))
      

      self.cur.execute(self.sql_insert,tuple(str(emp).split("\n")))

      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      results = self.cur.fetchall()

      # think how you could develop this method to show the records

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  def search_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      self.cur.execute(self.sql_search,tuple(str(employeeID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
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
            print("Salary: "+ str(detail))
      else:
        print ("No Record")
            
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  def update_data(self):
    try:
      self.get_connection()

      # Update statement
      
      if result.rowcount != 0:
        print (str(result.rowcount)+ "Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Define Delete_data method to delete data from the table. The user will need to input the employee id to delete the corrosponding record. 
  def delete_data(self):
    try:
      self.get_connection()

      
      if result.rowcount != 0:
        print (str(result.rowcount)+ "Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

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

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
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
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data into EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data (to update a record")
  print (" 6. Delete data (to delete a record")
  print (" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print ("Invalid Choice")



