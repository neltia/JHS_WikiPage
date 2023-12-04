import elasticsearch
from elasticsearch_dsl import Search
from app.models.dao import BoardIndex
from app.utils.dto import BoardDto
from app.utils import common
from datetime import datetime

api = BoardDto.api


class BoardService:
    @staticmethod
    def all_post():
        search = Search(index=BoardIndex())
        res = search.query('match_all').execute()
        post_list = []
        for hit in res.hits:
            post_data = hit.to_dict()
            post_data['id'] = hit.meta.id
            post_list.append(post_data)
        return post_list

    @staticmethod
    def create_post(title, content):
        post = BoardIndex(title=title, content=content)
        post.created_at = datetime.now()
        post.save()

        post_id = post.meta.id
        return post_id

    @staticmethod
    def get_post(post_id):
        try:
            post = BoardIndex.get(id=post_id)
        except elasticsearch.NotFoundError:
            msg = f"post_id: {post_id} doesn't exist"
            res = {"status_code": 404, "result": msg}
            api.abort(404, res)
        post = post.to_dict()
        post = common.conversed_json(post)
        return post

    @staticmethod
    def delete_post(post_id):
        try:
            post = BoardIndex.get(id=post_id)
        except elasticsearch.NotFoundError:
            msg = f"post_id: {post_id} doesn't exist"
            res = {"status_code": 404, "result": msg}
            api.abort(404, res)

        post.delete()
        res = "deleted"
        return res
