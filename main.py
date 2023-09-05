from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group
from seed import engine

Session = sessionmaker(bind=engine)
session = Session()


# Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    top_students = session.query(Student).join(Grade).group_by(Student).\
        order_by(func.avg(Grade.value).desc()).limit(5).all()
    return top_students


# Запит 2: Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_name):
    top_student = session.query(Student).join(Grade).join(Subject).\
        filter(Subject.name == subject_name).group_by(Student).\
        order_by(func.avg(Grade.value).desc()).first()
    return top_student


# Запит 3: Знайти середній бал у групах з певного предмета
def select_3(subject_name):
    avg_grades_by_group = session.query(Group, func.avg(Grade.value)).\
        join(Student).join(Grade).join(Subject).\
        filter(Subject.name == subject_name).group_by(Group).all()
    return avg_grades_by_group


# Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    avg_grade_overall = session.query(func.avg(Grade.value)).scalar()
    return avg_grade_overall


# Запит 5: Знайти, які курси читає певний викладач
def select_5(teacher_name):
    teacher_courses = session.query(Subject).join(Teacher).\
        filter(Teacher.name == teacher_name).all()
    return teacher_courses


# Запит 6: Знайти список студентів у певній групі
def select_6(group_name):
    students_in_group = session.query(Student).join(Group).\
        filter(Group.name == group_name).all()
    return students_in_group


# Запит 7: Знайти оцінки студентів в окремій групі з певного предмета
def select_7(group_name, subject_name):
    grades_in_group = session.query(Grade).join(Student).join(Group).join(Subject).\
        filter(Group.name == group_name, Subject.name == subject_name).all()
    return grades_in_group


# Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_name):
    avg_teacher_grades = session.query(func.avg(Grade.value)).join(Subject).\
        join(Teacher).filter(Teacher.name == teacher_name).scalar()
    return avg_teacher_grades


# Запит 9: Знайти список курсів, які відвідує певний студент
def select_9(student_name):
    student_courses = session.query(Subject).join(Grade).\
        join(Student).filter(Student.name == student_name).all()
    return student_courses


# Запит 10: Список курсів, які певному студенту читає певний викладач
def select_10(student_name, teacher_name):
    student_teacher_courses = session.query(Subject).join(Grade).\
        join(Student).join(Teacher).filter(Student.name == student_name, Teacher.name == teacher_name).all()
    return student_teacher_courses


if __name__ == '__main__':
    # Виклик функцій запитів та виведення результатів
    result_1 = select_1()
    print("Запит 1:", result_1)

    result_2 = select_2("Назва певного предмета")
    print("Запит 2:", result_2)

    result_3 = select_3("Назва певного предмета")
    print("Запит 3:", result_3)

    result_4 = select_4()
    print("Запит 4:", result_4)

    result_5 = select_5("Ім'я певного викладача")
    print("Запит 5:", result_5)

    result_6 = select_6("Назва певної групи")
    print("Запит 6:", result_6)

    result_7 = select_7("Назва певної групи", "Назва певного предмета")
    print("Запит 7:", result_7)

    result_8 = select_8("Ім'я певного викладача")
    print("Запит 8:", result_8)

    result_9 = select_9("Ім'я певного студента")
    print("Запит 9:", result_9)

    result_10 = select_10("Ім'я певного студента", "Ім'я певного викладача")
    print("Запит 10:", result_10)
