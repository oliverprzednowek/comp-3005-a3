import psycopg2 as ps
from tabulate import tabulate
import datetime

class Db:
# Db class runs all the functions that interact with the database
# to encapsulate this functionality
    def __init__(self):
        # initializing db object
        try:
            self.conn = ps.connect(database="COMP-3005-A3",
                                    user="postgres",
                                    password="8439",
                                    host="localhost")
            print("Database connected successfully")
        except:
            print("Database not connected successfully")
    
    def getAllStudents(self):
        # function to print all students in db
        with self.conn.cursor() as curs:
            try:
                curs.execute("SELECT * FROM students")
                data = curs.fetchall()
                headers = ["student_id", "first_name", "last_name", "email", "enrollment_date"]
                print(tabulate(data, headers=headers)) # prints a neat table using tabulate

            except (Exception, ps.DatabaseError) as error:
                print(error)

    def addStudent(self, first_name: str, last_name: str, email: str, enrollment_date: datetime):
        # this function adds a student to the database
        query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES(%s, %s, %s, %s)"
        data = (first_name, last_name, email, str(enrollment_date))

        with self.conn.cursor() as curs:
            try:
                curs.execute(query, data)
                self.conn.commit()

            except (Exception, ps.DatabaseError) as error:
                print(error)
    

    def updateStudentEmail(self, student_id: int, new_email: str):
        # this function updates a student's email address
        query = """ UPDATE students
        SET email = %s
        WHERE student_id = %s"""

        data = (new_email, student_id)

        with self.conn.cursor() as curs:
            try:
                curs.execute(query, data)
                self.conn.commit()
            except (Exception, ps.DatabaseError) as error:
                print(error)
    
    def deleteStudent(self, id):
        # this function deletes a student from the database
        query = """DELETE FROM students
        WHERE student_id = %s"""
        data = (id,)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query, data)
                self.conn.commit()
            except (Exception, ps.DatabaseError) as error:
                print(error)
    


    
def getStudentInfo() -> list | None:
    # function to get data about a student when adding a student to the database
    print("Please enter the following information:")
    fname = input("first name: ")
    lname = input("last name: ")
    email = input("email: ")
    try:
        year = int(input("enrollment year: "))
        month = int(input("enrollment month: "))
        day = int(input("enrollment day: "))
    except ValueError:
        print("Whoops, one of the numbers you entered isn't valid")
        return None
    date = datetime.datetime(year, month, day)
    return [fname, lname, email, date]


def getStudentId():
    # function to get the student id and ensure it is valid
    try:
        id = int(input("please enter student ID: "))
    except ValueError:
        print("Whoops, one of the numbers you entered isn't valid")
        return None
    return id
 
def getStudentIdEmail() -> list | None:
    # function to get student id and email
    print("Please enter the following information:")
    id = getStudentId()
    if not id: return None
    email = input("please enter student email: ")
    return [id, email]


def menu(db: Db):
    # menu function which runs the main code
    while (True):
        print("1 -> get all students")
        print("2 -> add a student")
        print("3 -> update a student's email")
        print("4 -> delete a student")
        print("q -> exit the program")
        choice = input("Pick an option: ")
        match choice:
            case '1':
                db.getAllStudents()
            case '2':
                studentInfo = getStudentInfo()
                if not studentInfo: continue
                db.addStudent(*studentInfo)
            case '3':
                idEmail = getStudentIdEmail()
                if not idEmail: continue
                db.updateStudentEmail(*idEmail)
            case '4':
                id = getStudentId()
                if not id: continue
                db.deleteStudent(id)    
            case 'q':
                break
            case _:
                print("invalid option")
                

def main():
    db = Db()
    menu(db)


if __name__ == "__main__":
    main()
