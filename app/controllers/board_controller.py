from flask_restx import Resource
from app.services.board_service import BoardService
from app.utils.dto import BoardDto


api = BoardDto.api
post_model = BoardDto.post_model


@api.route('/')
@api.response(404, 'Todo not found')
class PostList(Resource):
    ''' Shows a list of all todos, and lets you POST to add new tasks '''
    @api.doc('list_posts')
    def get(self):
        # List all post
        post_list = BoardService.all_post()

        # 검색 결과가 비어있는 경우 404 응답 반환
        if not post_list:
            return {"status_code": 404, "result": "no results found"}, 404

        # 결과가 있을 경우 200 응답 반환
        data = {"status_code": 200, "result": post_list}
        return data


@api.route('/new')
@api.response(201, 'New post created')
class PostCreateResource(Resource):
    @api.doc("create_post")
    @api.expect(post_model, validate=True)
    def post(self):
        req = api.payload
        post_id = BoardService.create_post(
            title=req["title"], content=req["content"]
        )
        data = {"status_code": 201, "result": post_id}
        return data, 201


@api.route('/<post_id>')
@api.response(404, 'post not found')
@api.param('post_id', 'The board post identifier')
class PostResource(Resource):
    '''Show a single post item and lets you delete them'''
    @api.doc("get_post")
    def get(self, post_id):
        post = BoardService.get_post(post_id)
        data = {"status_code": 200, "result": post}
        return data

    @api.doc("delete_post")
    def delete(self, post_id):
        req = BoardService.delete_post(post_id)
        data = {"status_code": 200, "result": req}
        return data