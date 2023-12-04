from elasticsearch_dsl import Document
from elasticsearch_dsl import Text, Keyword
from elasticsearch_dsl import Date, Boolean, Nested, Float


# Index: 게시판 게시글 목록 조회, 생성, 내용 조회
class BoardIndex(Document):
    class Index:
        name = "board_index"

    title = Text()
    content = Text(analyzer="nori")
    created_at = Date()


# Index: 게시판 게시글 별 40% 이하 빈도 단어 목록, 연관게시글 목록 저장
class RelatedDocument(Document):
    score = Float()
    post_id = Text()


class RelatedPostIndex(Document):
    class Index:
        name = "related_posts"

    word_list = Text()
    related_posts = Nested(RelatedDocument)
