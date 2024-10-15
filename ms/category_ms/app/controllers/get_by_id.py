from flask import Flask
from flask_restful import Resource
from app.services import category_service
from app.schemas import category_schema

class GetById(Resource):
    def get(self, category_id):
        category_service = category_service()
        category_schema = category_schema()

        try:
            category = category_service()
            if category:
                return {"category": category_schema.dump(category)}, 200
        except Exception as e:
            return {"error": f"Error al obtener categoría por ID: {str(e)}"}, 500
