import requests

url = "https://sinhvien4.tlu.edu.vn:8098/education/oauth/token"
data1 = {
    "client_id": "education_client",
    "grant_type": "password",
    "username": "2251272692",
    "password": "034304009143",
    "client_secret": "password",
}

# Use 'json' instead of 'data' for sending JSON data
response = requests.post(url, json=data1)
print(response.status_code)

url3 = "https://sinhvien2.tlu.edu.vn:9923/education/api/cs_reg_mongo/findByPeriod/71318/36"
h2 = {
    'Host': 'sinhvien2.tlu.edu.vn:9923',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Authorization': 'Bearer 0b3c0a71-0bc4-44c0-87f2-98f955250cbb',
}

res = requests.get(url3, headers=h2)

if res.status_code == 200:
    print(f"Danh sách các môn gồm:")
    data = res.json()['courseRegisterViewObject']
    listsub = data['listSubjectRegistrationDtos']

    for i in listsub:
        sub = i.get('subjectName')
        print(sub)
        time = i.get('courseSubjectDtos', {})

        for table in time:
            timetables = table.get('timetables', {})
            
            for timetable in timetables:
                id = timetable.get('id')
                end_hour = timetable.get('endHour', {}).get('name', '')
                start_hour = timetable.get('startHour', {}).get('name', '')
                print(f"Danh sách ca học tương ứng là: {id} - {start_hour} - {end_hour}")

# Checking if 'res' variable exists before using it
if 'res' in locals() and res.status_code == 200:
    print(f"Nhập ca học bạn muốn đăng ký?")
    x = input()
    ur4 = 'https://sinhvien2.tlu.edu.vn:9923/education/api/cs_reg_mongo/add-register/71318/36'
    h3 = {
        'Host': 'sinhvien2.tlu.edu.vn:9923',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Authorization': 'Bearer 0b3c0a71-0bc4-44c0-87f2-98f955250cbb',
    }

    for i in listsub:
        time = i.get('courseSubjectDtos', {})
        
        for table in time:
            timetables = table.get('timetables', {})
            
            for timetable in timetables:
                id = table.get('id')
                
                if id == x:
                    resp = requests.post(ur4, headers=h3, json=timetable)
                    print(resp.status_code)
