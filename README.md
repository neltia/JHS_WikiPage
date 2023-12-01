# flask-api-todo
Board API 작성: Flask-RESTX 라이브러리 활용 REST API 작성 과제

## Sytem Arch (test)
### virtualenv
Vagrantfile setup & Virtualbox
- vagrant: 2.4.0
- virtualbox: 6.1
- linux: ubuntu linux 22.04

### Python
lang: Python 3.10.12
lib.ver.
<pre>
python-dotenv==0.21.1
Flask==2.2.2
Werkzeug==2.2.2
flask-restx==1.1.0
elastic-transport==8.10.0
elasticsearch==8.11.0
elasticsearch-dsl==8.11.0
</pre>

## 프로젝트 실행
### .env 환경변수 파일 작성
<pre>
FLASK_APP=manage.py
FLASK_DEBUG=development
ES_API_KEY=...
ES_HOST=
ES_PORT=9200
ES_CRT_PATH=http_ca.crt
</pre>

### 테스트 서버 실행
<pre>
python manage.py
</pre>

### docker-compose 배포
<pre>
docker-compose -d up
</pre>
