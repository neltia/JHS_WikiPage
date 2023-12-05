import elasticsearch
from elasticsearch_dsl import Search
from app.models.dao import BoardIndex
from app.utils.dto import BoardDto
from app.utils import common
from datetime import datetime

api = BoardDto.api


class BoardService:
    '''전체 게시글 조회'''
    @staticmethod
    def all_post():
        # 전체 게시글 목록에서 title과 created_at 필드만 조회
        search = Search(index="board_index").source(["title", "created_at"])
        res = search.query('match_all').extra(size=1000).execute()
        post_list = [hit.to_dict() for hit in res.hits]
        return post_list

    '''게시글 생성'''
    @staticmethod
    def create_post(title, content):
        # 게시글 생성, 추후 예외 발생에 대한 처리 추가 필요
        post = BoardIndex(title=title, content=content)
        post.created_at = datetime.now()
        post.save()

        # 정상 결과 실행 시 게시글 고유 ID 반환
        post_id = post.meta.id
        return post_id

    '''게시글 조회'''
    @staticmethod
    def get_post(post_id):
        # ID를 가지고 게시글 조회, 찾을 수 없을 시 404 abort 발생
        try:
            post = BoardIndex.get(id=post_id)
        except elasticsearch.NotFoundError:
            msg = f"post_id: {post_id} doesn't exist"
            res = {"status_code": 404, "result": msg}
            api.abort(404, res)

        # 날짜 데이터를 문자열로 적절히 처리하여 반환
        post = post.to_dict()
        post = common.conversed_json(post)
        return post
