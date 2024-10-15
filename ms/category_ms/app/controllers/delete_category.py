from flask import Flask
from flask_restful import Resource, reqparse
from app.services import category_service
from app.schemas import category_schema

class DeleteCategory(Resource):
   def delete_category(category_id):
      category_service = category_service()
      category_schema = category_schema()
      try:
        category = category_service.find_by_id(category_id)
        if category:
            updated_category_data = category_schema.load(reqparse.request.json, partial = True)
            for key, value in updated_category_data.items():
                setattr(category, key, value)
            category_service.update(category)
            return {"category": category_schema.dump(category)}, 200
        else:
            return {"error": "Categoría no encontrada"}, 404
      except Exception as e:
            return {"error": f"Error al actualizar categoría: {str(e)}"}, 500