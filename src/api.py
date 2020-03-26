from flask import request
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException

from src.models import Keyword


class NotFound(HTTPException):
    code = 404
    data = {}


class KeywordsApi(Api):
    
    def init_app(self, app):
        super(KeywordsApi, self).init_app(app)
        app.after_request(self.add_cors_headers)

    def add_cors_headers(self, response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response


class KeywordsResource(Resource):
    default_length = 100

    def get(self, keyword_id=None):
        if keyword_id:
            return self.get_one(keyword_id)
        return self.get_list()

    def get_one(self, keyword_id):
        keyword = Keyword.query.get(keyword_id)
        return keyword.as_dict()

    def get_list(self):
        query = self.paginate(Keyword.query)
        keywords = [row.as_dict() for row in query]
        return keywords

    def paginate(self, query):
        offset = int(request.args.get('start', 0))
        limit = int(request.args.get('length', self.default_length))
        if offset < 0 or limit < 0:
            raise NotFound()
        entries = query.limit(limit).offset(offset).all()
        if not entries:
            raise NotFound()

        return entries


api = KeywordsApi()
api.add_resource(KeywordsResource, '/keyword/<int:keyword_id>', '/keywords')
