University API
University API is a Flask application that provides RESTful APIs for university operations. It can be used to manage various types of data such as student information, courses, enrollments, payments, etc.
To start the application:
python app.py or python3 app.py
and my localhost: http://127.0.0.1:5000/
Authentication:
Authentication is required to use the API. To obtain a token, send a POST request to the /login endpoint:
curl -X POST -H "Content-Type: application/json" -d '{"username":"my-username","password":"my-password"}' http://localhost:5000/v1/login
This will return you an access token which you can use in other endpoints.
My Endpoints:
http://127.0.0.1:5000/v1/University_Web_Site_Admin/add_tuition?student_no=student_1 --> POST method
http://127.0.0.1:5000/v1/University_Web_Site_Admin/unpaid_tuition_status?term=term_1 --> GET method
http://127.0.0.1:5000/v1/Banking_App/pay_tuition?student_no=student_1 --> POST method
http://127.0.0.1:5000/v1/Banking_App/query_tuition?student_no=student_1 --> GET method
http://127.0.0.1:5000/v1/University_Mobile_App/query_tuition?student_no=student_1 --> GET method

My API requirements
 
University Mobile App 	Authentication	Paging
Query Tuition	                NO	       NO
Banking App 		
Query Tuition	                YES	       NO
Pay Tuition	                  NO	       NO
University Web Site - Admin		
Add Tuition	                  YES	       NO
Unpaid Tuition Status	        YES	      YES

