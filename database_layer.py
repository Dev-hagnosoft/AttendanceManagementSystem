from sqlalchemy import create_engine, Column, Integer, String, DateTime,ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pandas as pd
import sqlite3

# Step 2: Create declarative base
Base = declarative_base()

# Step 3: Create the database engine
# The database file will be created in the current directory with the name "AttendanceManagementSystem.db"
engine = create_engine('sqlite:///AttendanceManagementSystem.db', echo=True)  # Set echo to True to see SQL commands in the console
conn_string = 'AttendanceManagementSystem.db'



def dbTransactionSelect(query):
    connection = sqlite3.connect(conn_string)
    try:
        select_cursor = connection.cursor()
        select_cursor.execute(query)
        query_result=select_cursor.fetchall()
        connection.commit()
        if len(query_result)>0:
            columns = select_cursor.description 
            result = [{columns[index][0]:column for index, column in enumerate(value)} for value in query_result]
            return result
        if len(query_result)==0:
            return "No data Found"
    except Exception as ex:
        return str(ex)
    finally:
        select_cursor.close()
        connection.close()


def dbTransactionIUD(query):
    connection = sqlite3.connect(conn_string)
    try:
        iud_cursor = connection.cursor()
        iud_cursor.execute(query)
        connection.commit()
        return "Success"
    except Exception as ex:
        return str(ex)
    finally:
        iud_cursor.close()
        connection.close()

def select_data_rawquery(query):
    try:
        conn= engine.connect()
        df = pd.read_sql(query, conn)
        return df
    except Exception as ex:
        return "error"


# Step 4: Define your models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # type = Column(String(50), nullable=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    # submitted_by = Column(Integer, ForeignKey('users.id'))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   
    
class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(50), nullable=False)
    department_id = Column(Integer, nullable=False)
    semester = Column(String(100), nullable=False)
    class_of = Column(String(50), nullable=False)
    lecture_hours = Column(String(100), nullable=False)
    submitted_by = Column(Integer, ForeignKey('course.id'))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    
class AttendanceLog(Base):
    __tablename__ = 'attendance_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    present=Column(Boolean)
    submitted_by = Column(Integer, ForeignKey('attendance_log.id'))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(50), nullable=False)
    submitted_by = Column(Integer, ForeignKey('course.id'))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    department_id = Column(Integer, nullable=False)
    class_of = Column(String(50), nullable=False)
    submitted_by = Column(Integer, ForeignKey('students.id'))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    

# Step 5: Create the tables in the database
Base.metadata.create_all(engine)

