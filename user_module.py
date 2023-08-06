import database_layer as db
import encryption as encrypt_module
import datetime


############################################################User configuration ##################################

def signup(full_name,username,email,password):
    encrypt_pwd= encrypt_module.hash_password(password)
    check_user_name_query="select exists(select username from users where username='"+str(username)+"')"
    check_user_name_result=db.dbTransactionSelect(check_user_name_query)
    if check_user_name_result[0]["exists(select username from users where username='"+str(username)+"')"]!=0:
        return "username already exists"
    check_email_query=" select exists(select email from users where email='"+str(email)+"')"
    check_email_result=db.dbTransactionSelect(check_email_query)
    if check_email_result[0]["exists(select email from users where email='"+str(email)+"')"]!=0:
        return "Email already exists"
    query="insert into users(full_name,username,email, password,updated_at) values('"+str(full_name)+"','"+str(username)+"','"+str(email)+"','"+str(encrypt_pwd)+"','"+str(datetime.datetime.now())+"')"
    result=db.dbTransactionIUD(query)
    return result

def forgetpassword(email,password):
    encrypt_pwd= encrypt_module.hash_password(password)
    check_email_query=" select exists(select email from users where email='"+str(email)+"')"
    check_email_result=db.dbTransactionSelect(check_email_query)
    if check_email_result[0]["exists(select email from users where email='"+str(email)+"')"]!=0:
        query="update users set password='"+str(encrypt_pwd)+"' where email='"+str(email)+"';"
        result=db.dbTransactionIUD(query)
        return result
    return "Email not exists"

def loginUser(username,entered_password):
    check_user_name_query="select exists(select username from users where username='"+str(username)+"')"
    check_user_name_result=db.dbTransactionSelect(check_user_name_query)
    if check_user_name_result[0]["exists(select username from users where username='"+str(username)+"')"]==0:
        return "Username does not exist in our system. Please try again"
    else:
        query_get_pwd="select password from users where username='"+str(username)+"';"
        result_pwd=db.dbTransactionSelect(query_get_pwd)
        check_pwd =encrypt_module.checkPassword(entered_password,str(result_pwd[0]['password']))
        if check_pwd==0:
            return "Wrong password entered"
        if check_pwd==1:
            api_key =encrypt_module.generateUniqueKey()
            user_data_query="select id as user_id,username,email from users where username='"+str(username)+"';"
            result=db.dbTransactionSelect(user_data_query)
        final_result={"api_key":api_key,"user_id":result[0]['user_id'],"username":result[0]['username'],"email":result[0]['email']}
        return final_result
            
######################################################Department configuration #####################################

def createDepartment(department_name,submitted_by):
    query="insert into departments(department_name,submitted_by,updated_at) values('"+str(department_name)+"','"+str(submitted_by)+"','"+str(datetime.datetime.now())+"')"
    result = db.dbTransactionIUD(query)
    return result

def getDepartmentlist(submitted_by):
    query = "SELECT departments.id,departments.department_name,users.full_name as submitted_by,departments.updated_at FROM departments INNER JOIN users ON departments.submitted_by = users.id where submitted_by='"+str(submitted_by)+"';"
    result = db.select_data_rawquery(query) 
    if len(result)==0:
        return  '[]'
    if len(result)>0:
        return result.to_json(orient="records",date_format='iso')

def updateDepartment(department_name,department_id,submitted_by):
    check_department_name_query="select exists(select department_name from departments where department_name='"+str(department_name)+"')"
    check_department_name_result=db.dbTransactionSelect(check_department_name_query)
    if check_department_name_result[0]["exists(select department_name from departments where department_name='"+str(department_name)+"')"]!=0:
        return "Department name alredy exists"
    query = "update departments set department_name='"+str(department_name)+"' where id='"+str(department_id)+"' and submitted_by='"+str(submitted_by)+"';"
    result = db.dbTransactionIUD(query) 
    return result
      
      
###########################################Course configuration #####################################################

def createCourse(course_name,department_id,semester,class_of,lecture_hours,submitted_by):
    query="insert into course(course_name,department_id,semester,class_of,lecture_hours,submitted_by,updated_at) values('"+str(course_name)+"','"+str(department_id)+"','"+str(semester)+"','"+str(class_of)+"','"+str(lecture_hours)+"','"+str(submitted_by)+"','"+str(datetime.datetime.now())+"')"
    result = db.dbTransactionIUD(query)
    return result

def getCourselist(submitted_by):
    query = "SELECT * FROM course where submitted_by='"+str(submitted_by)+"';"
    result = db.select_data_rawquery(query) 
    if len(result)==0:
        return  '[]'
    if len(result)>0:
        return result.to_json(orient="records",date_format='iso')

def updateCourse(course_name,course_id,submitted_by):
    check_department_name_query="select exists(select course_name from course where course_name='"+str(course_name)+"')"
    check_department_name_result=db.dbTransactionSelect(check_department_name_query)
    if check_department_name_result[0]["exists(select course_name from course where course_name='"+str(course_name)+"')"]!=0:
        return "course name alredy exists"
    query = "update course set course_name='"+str(course_name)+"' where id='"+str(course_id)+"' and submitted_by='"+str(submitted_by)+"';"
    result = db.dbTransactionIUD(query) 
    return result

#################################################Student configuration #######################################
    
def createStudent(full_name,department_id,class_of,submitted_by):
    query="insert into students(full_name,department_id,class_of,submitted_by,updated_at) values('"+str(full_name)+"','"+str(department_id)+"','"+str(class_of)+"','"+str(submitted_by)+"','"+str(datetime.datetime.now())+"')"
    result = db.dbTransactionIUD(query)
    return result

def getStudentlist(submitted_by):
    query = "SELECT * FROM students where submitted_by='"+str(submitted_by)+"';"
    result = db.select_data_rawquery(query) 
    if len(result)==0:
        return  '[]'
    if len(result)>0:
        return result.to_json(orient="records",date_format='iso')

def updateStudent(full_name,department_id,class_of,student_id,submitted_by):
    query = "update students set full_name='"+str(full_name)+"',department_id='"+str(department_id)+"',class_of='"+str(class_of)+"' where id='"+str(student_id)+"' and submitted_by='"+str(submitted_by)+"';"
    result = db.dbTransactionIUD(query) 
    return result

############################################################Attendance log#########################################

def createStudentAttandence(student_id,course_id,present,submitted_by):
    query="insert into attendance_log(student_id,course_id,present,submitted_by,updated_at) values('"+str(student_id)+"','"+str(course_id)+"','"+str(present)+"','"+str(submitted_by)+"','"+str(datetime.datetime.now())+"')"
    result = db.dbTransactionIUD(query)
    return result

def getStudentAttandencelist(submitted_by):
    query = "SELECT * FROM attendance_log where submitted_by='"+str(submitted_by)+"';"
    result = db.select_data_rawquery(query) 
    if len(result)==0:
        return  '[]'
    if len(result)>0:
        return result.to_json(orient="records",date_format='iso')
    
def getsingleStudentAttandencelist(student_id,submitted_by):
    query = "SELECT * FROM attendance_log where id='"+str(student_id)+"' and submitted_by='"+str(submitted_by)+"';"
    result = db.select_data_rawquery(query) 
    if len(result)==0:
        return  '[]'
    if len(result)>0:
        return result.to_json(orient="records",date_format='iso')

def updateStudentAttandence(student_id,present,submitted_by,attendance_id):
    query = "update attendance_log set present='"+str(present)+"' where id='"+str(student_id)+"' and submitted_by='"+str(submitted_by)+"' and id='"+str(attendance_id)+"';"
    result = db.dbTransactionIUD(query) 
    return result

