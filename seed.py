from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from models import Student, Group, Grade, Subject, Teacher
from sqlalchemy.exc import IntegrityError
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
postgres_password = config.get("DB", "password")
postgres_port = config.get("DB", "port")

DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:{postgres_port}/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker

groups = [Group(name=f"Group {i}") for i in range(1, 4)]
session.bulk_save_objects(groups)

subjects = [Subject(name=fake.word()) for _ in range(random.randint(5, 8))]
session.bulk_save_objects(subjects)
session.commit()

teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
session.bulk_save_objects(teachers)
session.commit()

students = []
for _ in range(random.randint(30, 51)):
    student = Student(name=fake.name(), group_id=random.choice(groups).id)
    students.append(student)

session.bulk_save_objects(subjects)
session.commit()

grades = []
for student in students:
    for subject in subjects:
        teacher = random.choice(teachers)
        grade_value = random.randint(1, 101)
        grade = Grade(
            student_id=student.id,
            subject_id=subject.id,
            teacher_id=teacher.id,
            value=grade_value
        )
        grades.append(grade)
try:
    session.bulk_save_objects(grades)
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"IntegrityError: {e}")
