import elasticsearch
from app.config.es_config import es_client
from elasticsearch_dsl import Search, Q
from app.models.dao import BoardIndex, RelatedPostIndex
from app.utils.dto import BoardDto

es = es_client()


class RelatedService:
    '''ES의 Term Vectors API 활용 빈도 정보 계산'''
    @staticmethod
    def get_freq_words(post_id):
        # Term Vectors에서 빈도 정보 추출
        term_vectors = es.termvectors(index="board_index", id=post_id, fields=['content'], term_statistics=True)
        term_freq_info = term_vectors['term_vectors']['content']['terms']

        # 전체 문서 수, 빈도가 40% 이하인 단어 리스트
        total_docs = term_vectors['term_vectors']['content']['field_statistics']['doc_count']
        low_freq_words = [term  for term, info in term_freq_info.items() if info['term_freq'] / total_docs <= 0.4]

        # 결과 반환
        # LOG: print("Low-frequency words (<= 40%):", low_freq_words)
        return low_freq_words


    '''freq words 기준, 연관게시글 연결'''
    @staticmethod
    def related_posts(post_id, word_list):
        # match 쿼리 수행을 위해 문자열 결합
        word_list_cnt = len(word_list)
        if isinstance(word_list, list):
            word_string = " ".join(word_list)

        # Query: word_list 필드 검색, 겹친 단어가 많을수록 score 값이 높음
        # 요청 경우가 새 도큐먼트 생성 시이긴 하지만,
        # - 만약을 위해 주어진 post_id는 검색에서 제외
        s = Search(index=RelatedPostIndex())
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
        s = s.query(query).extra(size=10, min_score=1)
        response = s.execute()
        # 결과 데이터 반환
        related_post_list = list()
        for hit in response:
            # - 스코어 값이 1 이상이더라도,
            # - 단어가 하나만 겹치는 문서가 검색되는 경우를 위한 분기
            related_words = hit.to_dict()["word_list"]
            related_words_cnt = len(related_words)
            merge_list = word_list + related_words
            merge_cnt = word_list_cnt + related_words_cnt
            if merge_cnt - list(set(merge_list)) == 1:
                continue

            # - 연관게시글 목록 추가
            related_post = {"score": hit.meta.score, "post_id": hit.meta.id}
            related_post_list.append(related_post)

        # 인덱스 데이터 저장
        obj = RelatedPostIndex(meta={'id': post_id}, word_list=word_string)
        obj.related_posts = related_post_list
        obj.save()
        return related_post_list
