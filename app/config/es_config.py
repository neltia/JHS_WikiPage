from dotenv import load_dotenv
import os
from elasticsearch_dsl import connections
from app.models.dao import BoardIndex, RelatedPostIndex


# es 설정 초기화
def es_init():
    load_dotenv(verbose=True)

    es_client()
    index_mapping()


# 엘라스틱서치 클라이언트 세션 생성
def es_client():
    # ENV
    es_username = os.getenv("ELASTIC_USERNAME", "elastic")
    es_pw = os.getenv("ELASTIC_PASSWORD")
    es_port = os.getenv("ES_PORT")
    ca_file_path = os.getenv("ES_CRT_PATH", "/usr/share/certs/ca/ca.crt")
    # LOG:
    # print(es_username, es_pw, es_port, ca_file_path)

    # connection create
    es = connections.create_connection(
        hosts=[f"https://es01:{es_port}"],
        ca_certs=ca_file_path,
        basic_auth=(es_username, es_pw)
    )

    # 내부 엘라스틱서치 통신 불가 시 Raise
    if not es.ping():
        print("Failed to connect to Elasticsearch.")
        print(es.info())
        exit()

    return es


# index mapping
def index_mapping():
    BoardIndex.init()
    RelatedPostIndex.init()
    return
