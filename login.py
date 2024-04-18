import requests

# Kullanıcı adı ve şifrenizi 
username = "user"
password = "user123"

# Giriş yapma isteği için veri
login_data = {"username": username, "password": password}

# Login endpointine POST isteği 
response = requests.post('http://127.0.0.1:5000/v1/Login/login', json=login_data, headers={"Content-Type": "application/json"})

# Yanıtı kontrol 
if response.status_code == 200:
    # Başarılı giriş durumunda erişim tokenini alın
    access_token = response.json().get('token')
    print("Access Token:", access_token)

    headers = {"Authorization": f"Bearer {access_token}"}
    response_query_tuition = requests.get('http://127.0.0.1:5000/v1/Banking_App/query_tuition?student_no=student_1', headers=headers)

    print(response_query_tuition.status_code)
    print(response_query_tuition.json())

    if response_query_tuition.status_code == 200:
        response_unpaid_tuition = requests.get('http://127.0.0.1:5000/v1/University_Web_Site_Admin/unpaid_tuition_status?term=term_1&page=1', headers=headers)

        print(response_unpaid_tuition.status_code)
        print(response_unpaid_tuition.json())

        add_tuition_data = {
            "student_no": "student_1",
            "term": "2024_Spring",  # Örnek bir dönem
            "tuition_total": 5000  # Örnek bir öğrenim ücreti
        }
        response_add_tuition = requests.post('http://127.0.0.1:5000/v1/University_Web_Site_Admin/add_tuition', json=add_tuition_data, headers=headers)
        print(response_add_tuition.status_code)
        print(response_add_tuition.json())

        pay_tuition_data = {
            "student_no": "student_1",
            "term": "2024_Spring"  # Örnek bir dönem
        }
        response_pay_tuition = requests.post('http://127.0.0.1:5000/v1/Banking_App/pay_tuition', json=pay_tuition_data, headers=headers)
        print(response_pay_tuition.status_code)
        print(response_pay_tuition.json())
else:
    print("Giriş yapılamadı. Hata kodu:", response.status_code)
