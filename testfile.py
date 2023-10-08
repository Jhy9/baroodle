import users
import courses
import students

def create_test():
    users.register("Money man","money123", "Teacher")
    users.register("Ghost", "salasana1", "Teacher")
    users.register("Ny12", "pws", "Student")
    users.register("Dave", "1234", "Student")
    users.register("FBI","undercover","Student")
    courses.create(1,"Making money 101","200% Works")
    courses.create(1,"Getting away with scams","Expert level")
    courses.create(2,"Jump scares","AAAAAAAAAA")

def add_attendances():
    students.attend_course(3,3)
    students.attend_course(3,4)
    students.attend_course(2,3)
    students.attend_course(2,5)
    students.attend_course(3,5)
    students.attend_course(1,5)