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
<pre>
docker-compose -d up
</pre>
