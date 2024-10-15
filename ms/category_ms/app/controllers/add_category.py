from flask import Flask
from flask_restful import Resource, reqparse
from app.services import category_service
from app.schemas import category_schema

class AddCategory(Resource):
    def post_category():
        category_service = category_service()
        category_schema = category_schema()
        try:
            category_data = category_schema.load(reqparse.request.json)
            category = category_service.create(category_data)
            return {"category": category_schema.dump(category)}, 200
        except Exception as e:
            return {"error": f"Error al agregar categoría: {str(e)}"}, 500

def delete_category(category_id):
    try:
        category_service = get_category_service()
        category = category_service.find_by_id(category_id)
        return get_category_response(category_service.delete(category_id))
    except Exception as e:
        return handle_exception(e, "Error al eliminar categoría")