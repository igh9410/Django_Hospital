# Django_Hospital

Hostpital and patients management API written in Django REST

## 실행 방법

로컬 환경:  
Postgres가 5432번 포트에서

- POSTGRES_DB=postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=testpassword
- POSTGRES_HOST=postgres
- POSTGRES_PORT=5432  
  실행중이어야 합니다.

git clone 이후 루트 디렉토리에서

pip install poetry -> poetry install ->  
poetry run python manage.py makemigrations  
poetry run python manage.py migrate  
poetry run python mnage.py runserver

도커 환경:  
pip install poetry ->  
docker compose up -d --build ->  
poetry run python manage.py makemigrations  
poetry run python manage.py migrate

## API endpoints

### API Documentations

Swagger: http://localhost:8000/swagger  
Redoc: http://localhost:8000/redoc

Endpoints:

의사검색  
a. 문자열 검색: GET http://localhost:8000/api/doctors/search-by-string/?string={}

- 문자열을 입력했을때 조건에 맞는 의사리스트 반환

b. 날짜별 검색: GET http://localhost:8000/api/doctors/search-by-datetime/?datetime={}

- 특정 날짜와 시간 입력하여 해당 시간에 영업중인 의사 반환.
- datetime 패러미터는 2023-12-14 01:00:00 과 같은 형식이어야 문제없이 작동

진료요청  
POST /api/appointments/  
HTTP Body (JSON):  
{
"patient_id": "patient_id(UUID)",
"doctor_id": "doctor_id(UUID)",
"preferred_datetime": "datetime (2023-12-14 01:00:00)"
}

RETURN  
{
"id": "4e61d524-9a5d-11ee-b1e6-571972f7616e",
"patient_name": "박환자",
"doctor_name": "김의사",
"preferred_datetime": "2023-12-18T10:00:00+09:00",
"request_expiration_datetime": "2023-12-14T18:06:43.268579+09:00"
}

진료요청 검색
GET /api/appointments/{doctor_id}  
ex) GET http://localhost:8000/api/appointments/?doctor_id=97c8f1f1-4b5f-4b65-9c0f-9a5c39443ee8

RETURN  
[
{
"id": "4e61d524-9a5d-11ee-b1e6-571972f7616e",
"patient_name": "박환자",
"doctor_name": "김의사",
"preferred_datetime": "2023-12-18T10:00:00+09:00",
"request_expiration_datetime": "2023-12-14T18:06:43.268579+09:00"
}
]

진료요청 수락
PATCH /api/appointments/{appointment_request_id}/accept/  
ex) http://localhost:8000/api/appointments/11ceeafc-9a5d-11ee-b1e6-571972f7616e/accept/

RETURN
{
"id": "11ceeafc-9a5d-11ee-b1e6-571972f7616e",
"patient_name": "김환자",
"preferred_datetime": "2023-12-18T10:00:00+09:00",
"request_expiration_datetime": "2023-12-14T18:05:01.641910+09:00"
}
