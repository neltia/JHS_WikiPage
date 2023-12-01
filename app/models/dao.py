from elasticsearch_dsl import Document
from elasticsearch_dsl import Date, Text, Boolean, Keyword


class BoardIndex(Document):
    class Index:
        name = "board_index"

    title = Text()
    content = Text(analyzer="nori")
    created_at = Date()
