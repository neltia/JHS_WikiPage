from flask_restx import Namespace, fields


class BoardDto:
    api = Namespace('board', description='Board API')

    post_model = api.model('post', {
        'id': fields.String(
            readonly=True,
            description='The unique identifier'
        ),
        'title': fields.String(
            required=True,
            description='The board post title'
        ),
        'content': fields.String(
            required=False,
            description='The board post content'
        ),
        'created_at': fields.DateTime(
            readonly=True,
            description='The post created at time'
        )
    })
