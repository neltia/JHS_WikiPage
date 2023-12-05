from flask_restx import Resource
from app.services.board_service import BoardService
from app.services.related_service import RelatedService
from app.utils.dto import BoardDto


api = BoardDto.api
post_model = BoardDto.post_model


@api.route('/')
@api.response(404, 'Board post list not found')
class PostList(Resource):
    @api.doc('list_posts')
    def get(self):
        '''Shows a list of all posts'''
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
        ''' create new post and return post id '''
        req = api.payload
        post_id = BoardService.create_post(
            title=req["title"], content=req["content"]
        )

        low_freq_words = RelatedService.get_freq_words(post_id)
        related_posts = RelatedService.connect_posts(post_id, low_freq_words)

        data = {"status_code": 201, "result": post_id}
        return data, 201


@api.route('/<post_id>')
@api.response(404, 'post not found')
@api.param('post_id', 'The board post identifier')
class PostResource(Resource):
    @api.doc("get_post")
    def get(self, post_id):
        ''' Show a single post item '''
        # 게시글 내용 조회
        post = BoardService.get_post(post_id)

        # 연관게시글 목록 조회, 기본 연관 score가 높은 순서로 반환
        related_posts = RelatedService.get_posts(post_id)
        post["related_posts"] = related_posts

        # 데이터 반환
        data = {"status_code": 200, "result": post}
        return data
