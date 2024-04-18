from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restx import Api, Resource, Namespace
from flasgger import Swagger
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'  # SQLite veritabanı dosyası
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)
api = Api(app, version='1.0', title='University API', description='APIs for University Operations', prefix='/v1')
swagger = Swagger(app)  # Swagger instance

db = SQLAlchemy(app)  # SQLAlchemy instance

# University Mobile App Namespace
university_mobile_app_ns = Namespace('University_Mobile_App', description='Endpoints for University Mobile App')
api.add_namespace(university_mobile_app_ns)

# Banking App Namespace
banking_app_ns = Namespace('Banking_App', description='Endpoints for Banking App')
api.add_namespace(banking_app_ns)

# University Web Site - Admin Namespace
admin_ns = Namespace('University_Web_Site_Admin', description='Endpoints for University Web Site - Admin')
api.add_namespace(admin_ns)

# Login Namespace
login_ns = Namespace('Login', description='Endpoints for Login')
api.add_namespace(login_ns)


# Öğrenci (Student) Modeli
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)


# Ders (Course) Modeli
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)


# Kayıt (Enrollment) Modeli
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)


# Ödeme (Payment) Modeli
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)


# Öğrenci (Student) Schema
class StudentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    date_of_birth = fields.Date()


# Ders (Course) Schema
class CourseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    credit_hours = fields.Int()
    department = fields.Str()


# Kayıt (Enrollment) Schema
class EnrollmentSchema(Schema):
    id = fields.Int()
    student_id = fields.Int()
    course_id = fields.Int()
    enrollment_date = fields.Date()


# Ödeme (Payment) Schema
class PaymentSchema(Schema):
    id = fields.Int()
    student_id = fields.Int()
    amount = fields.Float()
    payment_date = fields.Date()


tuition_data = {
    "student_1": {"tuition_total": 5000, "balance": 2000},
    "student_2": {"tuition_total": 6000, "balance": 6000},
}

unpaid_tuition = {
    "term_1": ["student_1", "student_2"],
    "term_2": ["student_3", "student_4"],
}

# Giriş endpointi
@login_ns.route('/login')
class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        
        if username == 'user' and password == 'user123':
            access_token = create_access_token(identity=username)
            return {"token": access_token}, 200
        else:
            return jsonify({"msg": "Invalid username or password"}), 401


# Öğrenim ücreti sorgulama
@university_mobile_app_ns.route('/query_tuition')
class QueryTuition(Resource):
    def get(self):
        student_no = request.args.get('student_no')
        if student_no in tuition_data:
            return {
                "tuition_total": tuition_data[student_no]["tuition_total"],
                "balance": tuition_data[student_no]["balance"]
            }
        else:
            return {"error": "Student not found"}, 404


# Öğrenim ücreti sorgulama (Bankacılık Uygulaması)
@banking_app_ns.route('/query_tuition')
class QueryTuition(Resource):
    @jwt_required()
    def get(self):
        student_no = request.args.get('student_no')
        if student_no in tuition_data:
            return {
                "tuition_total": tuition_data[student_no]["tuition_total"],
                "balance": tuition_data[student_no]["balance"]
            }
        else:
            return {"error": "Student not found"}, 404


# Öğrenim ücreti ödeme
@banking_app_ns.route('/pay_tuition')
class PayTuition(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        student_no = data.get('student_no')
        term = data.get('term')
        # Ödeme işlemi (örnek işlem)
        return {"payment_status": "Successful"}, 200


# Öğrenim ücreti ekleme
@admin_ns.route('/add_tuition')
class AddTuition(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        student_no = data.get('student_no')
        term = data.get('term')
        tuition_total = data.get('tuition_total')  # 'tuition_total' anahtarını doğru şekilde alın
        # Öğrencinin dönem için öğrenim ücretini ekleyin (örnek işlem)
        tuition_data[student_no] = {"tuition_total": tuition_total, "balance": 0}  # 'tuition_total' kullanımı düzeltildi
        return {"transaction_status": "Success"}, 200


# Ödenmemiş öğrenim ücreti durumu
@admin_ns.route('/unpaid_tuition_status')
class UnpaidTuitionStatus(Resource):
    @jwt_required()
    @admin_ns.doc(params={'page': 'Page number'})
    def get(self):
        term = request.args.get('term')
        page = int(request.args.get('page', 1))
        if term in unpaid_tuition:
            # Gerekiyorsa sayfalama yapın
            unpaid_students = unpaid_tuition[term][(page-1)*10:page*10]  # Sayfa başına 10 öğe varsayımı
            return {"unpaid_students": unpaid_students}
        else:
            return {"error": "Term not found"}, 404


"""# Öğrenciyi kaydetme
@university_mobile_app_ns.route('/enroll_student')
class EnrollStudent(Resource):
    def post(self):
        data = request.get_json()
        student_no = data.get('student_no')
        course_code = data.get('course_code')
        # Kayıt işlemi (örnek işlem)
        return {"enrollment_status": "Successful"}, 200


# Dersi bırakma
@university_mobile_app_ns.route('/drop_course')
class DropCourse(Resource):
    def post(self):
        data = request.get_json()
        student_no = data.get('student_no')
        course_code = data.get('course_code')
        # Ders bırakma işlemi (örnek işlem)
        return {"drop_status": "Successful"}, 200"""


if __name__ == '__main__':
    app.run(debug=True)
