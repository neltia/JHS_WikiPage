import elasticsearch
from app.config.es_config import es_client
from elasticsearch_dsl import Search, Q
from app.models.dao import BoardIndex, RelatedPostIndex, RelatedDocument
from app.utils.dto import BoardDto

es = es_client()
api = BoardDto.api


class RelatedService:
    '''ES의 Term Vectors API 활용 빈도 정보 계산'''
    @staticmethod
    def get_freq_words(post_id: str) -> list:
        # Term Vectors에서 빈도 정보 추출
        term_vectors = es.termvectors(index="board_index", id=post_id, fields=['content'], term_statistics=True)
        term_freq_info = term_vectors['term_vectors']['content']['terms']

        # 전체 문서 수, 빈도가 40% 이하인 단어 리스트
        total_docs = term_vectors['term_vectors']['content']['field_statistics']['doc_count']
        low_freq_words = [term  for term, info in term_freq_info.items() if info['term_freq'] / total_docs <= 0.4]

        # 결과 반환
        # LOG:
        # high_freq_words = [term for term, info in term_freq_info.items() if info['term_freq'] / total_docs > 0.4]
        # print("High-frequency words (> 40%):", high_freq_words)
        # print("Low-frequency words (<= 40%):", low_freq_words)
        return low_freq_words


    '''freq words 기준, 연관게시글 연결'''
    @staticmethod
    def connect_posts(post_id: str, word_list: list) -> list:
        # match 쿼리 수행을 위해 문자열 결합
        word_list_cnt = len(word_list)
        word_string = " ".join(word_list)

        # Query: word_list 필드 검색, 겹친 단어가 많을수록 score 값이 높음
        # 요청 경우가 새 도큐먼트 생성 시이긴 하지만,
        # - 만약을 위해 주어진 post_id는 검색에서 제외
        s = Search(index="related_posts")
        query = Q('bool',
            must=[
                Q('match', word_list=word_string)
            ],
            must_not=[
                Q('term', _id=post_id)
            ]
        )

        # 쿼리 수행
        # - size는 게시글의 최대 수를 임의로 산정
        # - min_score는 1로 설정, 테스트 결과 1 이하의 경우 단어가 하나만 겹치는 경우로 산정
        s = s.query(query).extra(size=1000, min_score=1)
        response = s.execute()
        # 결과 데이터 반환
        related_post_list = list()
        for hit in response:
            # - 스코어 값이 1 이상이더라도,
            # - 단어가 하나만 겹치는, 혹은 겹치지 않는 문서가 검색되는 경우를 위한 분기
            related_words = hit.to_dict()["word_list"].split()
            duplicated_words = list(set(word_list).intersection(related_words))
            # LOG:
            # print(duplicated_words)
            if len(duplicated_words) <= 1:
                continue

            # - 연관게시글 목록 추가
            related_document = RelatedDocument(score=hit.meta.score, post_id=hit.meta.id)
            related_post_list.append(related_document)

        # 연관게시글이 없을 경우: 필드 누락 방지를 위한 빈 도큐먼트 삽입
        if len(related_post_list) == 0:
            related_document = RelatedDocument(score=None, post_id=None)
            related_post_list.append(related_document)

        # 인덱스 데이터 저장
        obj = RelatedPostIndex(
            meta={'id': post_id}, word_list=word_string,
            related_posts=related_post_list
        )
        obj.save()
        return related_post_list

    '''저장된 연관 게시글 조회'''
    @staticmethod
    def get_posts(post_id: str) -> list:
        search = Search(index="related_posts").filter("term", _id=post_id)
        response = search.execute()
        res = response.to_dict()["hits"]["hits"]
        if len(res) == 0:
            msg = f"post_id: {post_id} doesn't exist"
            res = {"status_code": 404, "result": msg}
            api.abort(404, res)

        doc = res[0]
        related_posts = doc["_source"]["related_posts"]
        related_posts = [item["post_id"] for item in related_posts if "post_id" in item]
        return related_posts
