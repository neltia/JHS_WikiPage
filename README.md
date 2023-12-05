# flask-api
Board API 작성: Flask-RESTX 라이브러리 활용 REST API 작성 과제

## 구현 내용
- 게시판: 게시글의 ID, 제목, 본문, 생성날짜
- 게시글: 게시글 생성 시 연관게시글을 찾아 연결
- 연관게시글:
    - 게시글의 내용을 단어별로 공백기준으로 나눠 각 단어가 다른 게시글에서 얼마나 많이 나타나는가
    - 자주 사용하는 단어를 배제하기 위해 전체게시글 중 60% 이상 빈도 단어는 연관게시글 파악 시 배제
    - 게시글 40% 이하 빈도 단어가 해당 게시글에 많이 나타날수록 연관성이 높은 게시글

1. 게시글 작성
    - 제목, 본문을 입력 받아 게시글 생성
    - 게시글 생성 시 연관게시글 찾아 연결
2. 게시글 목록
    - 게시글 제목과 날짜 정보 반환
3. 게시글 내용 조회
    - 날짜, 제목, 내용, 연관 게시글 반환

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
gunicorn==21.2.0
</pre>

## 프로젝트 실행
### .env 환경변수 파일 작성
<pre>
# WAS config
FLASK_APP=manage.py
FLASK_DEBUG=development
ES_CRT_PATH=/usr/share/certs/ca/ca.crt

# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=

# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=

# Version of Elastic products
STACK_VERSION=8.11.1

# Set the cluster name
CLUSTER_NAME=docker-cluster

# Set to 'basic' or 'trial' to automatically start the 30-day trial
LICENSE=basic

# Port to expose Elasticsearch HTTP API to the host
ES_PORT=9200

# Port to expose Kibana to the host
KIBANA_PORT=5601

# Increase or decrease based on the available host memory (in bytes)
MEM_LIMIT=1073741824

# Project namespace (defaults to the current folder name if not set)
# COMPOSE_PROJECT_NAME=myproject
</pre>

### docker-compose
- new service build
<pre>
docker-compose -d up --build
</pre>
- service down
<pre>
docker-compose down
</pre>
- service restart
<pre>
docker-compose -d up
</pre>
