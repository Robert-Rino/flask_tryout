# -*- coding: utf-8 -*-
from flask import Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.article import Article

class ArticleResource(Resource):
    @jwt_required
    def post(self, *args):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        data = parser.parse_args()

        article = Article(title=data['title'], user_id=user_id)

        try:
            article.save_to_db()
        except:
            return {'message':'An error occured when inserting data'}, 500
        return article.json(), 201

    @jwt_required
    def put(self, article_id: int, *args):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('context', type=str, required=True)
        data = parser.parse_args()

        if not (article := Article.find_one(id=article_id, user_id=user_id)):
            return 404

        article.context = data['context']
        article.save_to_db()
        return {
            'title': article.title,
            'context': article.context,
        }, 200


        try:
            article.save_to_db()
        except:
            return {'message':'An error occured when inserting data'}, 500
        return article.json(), 201


    def get(self, article_id: int, *args):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)

        article = Article.find_one(id=article_id)

        if article:
            return article.json(), 200
        return {'message': 'store not found'}, 404

    @jwt_required
    def delete(self, article_id: int, *args):
        user_id = get_jwt_identity()
        article = Article.find_one(id=article_id, user_id=user_id)
        if not article:
            return Response(status=403)

        article.delete_from_db()
        return {'message': 'Store deleted'}



# class StoreList(Resource):
#     def get(self):
#         stores = Store.query.all()
#         result = [store.json() for store in stores]
#         return {'stores':result}
