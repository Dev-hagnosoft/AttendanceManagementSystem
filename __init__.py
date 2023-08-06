from flask import Flask,request,jsonify,session
import user_module as userboarding
import database_layer as db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta


app=Flask(__name__)
app.config["JWT_SECRET_KEY"] = "z7mv6ps81hjd145fcbdcyw8jfv8f2m0h14w679he14345"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=8)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'Developed by Dev anand'


@app.route('/')
def index():
    return "Attandence Management System Aplication is running"


@app.route("/jwtrefresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    api_key = request.headers["api-key"]
    if api_key!= session["api_key"]:
        return  jsonify({"message": "Unauthorized Access" }),401
    else:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token,refresh_token=refresh_token),200


@app.route('/signup',methods=["POST"])
def signup():
    try:
        param_json= request.get_json()
        full_name = param_json['full_name']
        user_name = param_json['username']
        email = param_json['email']
        password = param_json['password']
        registerUser=userboarding.signup(full_name,user_name,email,password)
        if registerUser=="Success":
            return jsonify({"message": "User registered successfully" }),200
        else:
            return jsonify({"message": registerUser }),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/login", methods=["POST"])
def login():
    try:
        param_json= request.get_json()
        username = str(param_json['username'])
        password =  str(param_json['password'])
        check_login=userboarding.loginUser(username,password)
        if check_login=="Wrong password entered" or check_login=="Username does not exist in our system. Please try again":
            return jsonify({"message": check_login }),452
        access_token = create_access_token(identity=username)
        refresh_token=create_refresh_token(identity=username)
        session['access_token']=access_token
        session['refresh_token']=refresh_token
        session['api_key']=check_login['api_key']
        return jsonify(access_token=access_token, refresh_token=refresh_token,data=check_login,message="Logged in successfully"),200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/resetpassword", methods=["POST"])
def resetpassword():
    try:
        param_json= request.get_json()
        email=param_json["email"]
        password=param_json["password"]
        if password=="":
            return jsonify({"message": "Password can't be Empty" }),452
        resetresult = userboarding.forgetpassword(email,password)
        if  resetresult=="Success":
                return  jsonify({"message": "Password reset successfully" }),200
        else:
                return  jsonify({"message": "email not exists" }),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500
    

########################################################Department configuration ###################################

@app.route("/addDepartment", methods=["POST"])
@jwt_required()
def createDepartment():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            department_name=param_json["department_name"]
            submitted_by=param_json['submitted_by']
            result = userboarding.createDepartment(department_name,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Department added successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/getDepartmentlist", methods=["GET"])
@jwt_required()
def getDepartmentlist():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            submitted_by=request.args.get('submitted_by')
            result=userboarding.getDepartmentlist(submitted_by)
            return  result,200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500


@app.route("/updateDepartment", methods=["POST"])
@jwt_required()
def updateDepartment():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            department_name=param_json["department_name"]
            department_id=param_json["department_id"]
            submitted_by=param_json["submitted_by"]
            result = userboarding.updateDepartment(department_name,department_id,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Department updated successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

############################################Course configuration ######################################################

@app.route("/addCourse", methods=["POST"])
@jwt_required()
def createCourse():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            course_name=param_json["course_name"]
            department_id=param_json['department_id']
            semester=param_json["semester"]
            class_of=param_json['class']
            lecture_hours=param_json["lecture_hours"]
            submitted_by=param_json['submitted_by']
            result = userboarding.createCourse(course_name,department_id,semester,class_of,lecture_hours,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Course added successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/getCourselist", methods=["GET"])
@jwt_required()
def getCourselist():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            submitted_by=request.args.get('submitted_by')
            result=userboarding.getCourselist(submitted_by)
            return  result,200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500


@app.route("/updateCourse", methods=["POST"])
@jwt_required()
def updateCourse():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            course_name=param_json["course_name"]
            course_id=param_json["course_id"]
            submitted_by=param_json["submitted_by"]
            result = userboarding.updateCourse(course_name,course_id,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Course updated successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

################################################## Student configuration ############################################

@app.route("/addStudent", methods=["POST"])
@jwt_required()
def createStudent():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            full_name=param_json["full_name"]
            department_id=param_json['department_id']
            class_of=param_json['class']
            submitted_by=param_json['submitted_by']
            result = userboarding.createStudent(full_name,department_id,class_of,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Student added successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/getStudentlist", methods=["GET"])
@jwt_required()
def getStudentlist():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            submitted_by=request.args.get('submitted_by')
            result=userboarding.getStudentlist(submitted_by)
            return  result,200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500


@app.route("/updateStudentdetails", methods=["POST"])
@jwt_required()
def updateStudent():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            full_name=param_json["full_name"]
            department_id=param_json["department_id"]
            class_of=param_json["class"]
            student_id=param_json["student_id"]
            submitted_by=param_json["submitted_by"]
            result = userboarding.updateStudent(full_name,department_id,class_of,student_id,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Student details updated successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

######################################################### Attandence Log #################################################

@app.route("/markAttandence", methods=["POST"])
@jwt_required()
def createStudentAttandence():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            student_id=param_json["course_name"]
            course_id=param_json['department_id']
            present=param_json["present"]
            submitted_by=param_json['submitted_by']
            result = userboarding.createStudentAttandence(student_id,course_id,present,submitted_by)
            if result =="Success":
                return  jsonify({"message": "Attendance done" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/getStudentAttandencelist", methods=["GET"])
@jwt_required()
def getStudentAttandencelist():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            submitted_by=request.args.get('submitted_by')
            result=userboarding.getStudentAttandencelist(submitted_by)
            return  result,200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/getsingleStudentAttandencelist", methods=["GET"])
@jwt_required()
def getsingleStudentAttandencelist():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            student_id=request.args.get('student_id')
            submitted_by=request.args.get('submitted_by')
            result=userboarding.getsingleStudentAttandencelist(student_id,submitted_by)
            return  result,200
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

@app.route("/updateStudentAttandence", methods=["POST"])
@jwt_required()
def updateStudentAttandence():
    try:
        api_key = request.headers["api-key"]
        if api_key!= session["api_key"]:
            return  jsonify({"message": "Unauthorized Access" }),401
        else:
            param_json= request.get_json()
            student_id=param_json["student_id"]
            present=param_json["present"]
            submitted_by=param_json["course_name"]
            attendance_id=param_json["attendance_id"]
            result = userboarding.updateStudentAttandence(student_id,present,submitted_by,attendance_id)
            if result =="Success":
                return  jsonify({"message": "Attendance updated successfully" }),200
            else:
                return  jsonify({"message":result}),452
    except Exception as ex:
        return jsonify({"error":str(ex)}),500

if __name__ == '__main__':
    app.run()