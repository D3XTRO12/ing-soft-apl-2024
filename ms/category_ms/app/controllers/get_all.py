from flask import Flask
from flask_restful import Resource
from app.services import category_service


class GetAll(Resource):
    def get(self):
        category_service = category_service()
        category_schema = category_schema()
        try:
            categories = category_service.find_all()
            return {"category": category_schema.dump(categories, many=True)}, 200
        except Exception as e:
            return {"error": f"Error al obtener categorías: {str(e)}"}, 500   

