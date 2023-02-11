from flask import jsonify
from flask_restful import Resource, abort

from api.common import *


class FindCities(Resource):
    @staticmethod
    def get(geo_name_id):
        """
        Метод принимает geo_name_id в видео целочисленного значения.
        Вызывает функцию для поиска географического объекта с geo_name_id.
        Если объект с geo_name_id найден, то отвечает клиенту со статус-кодом 200 ОК и
        передает json файл со всей информацией о географическом объекте.
        В противном случае отвечает со статус-кодом 404 NOT FOUND и json файлом
            {
         "message": "Geographical object doesn't exist.",
         "data": null
        }
        """
        response = {
            "message": None,
            "data": None
        }
        geo_obj = find_geo_obj_by_geo_name_id(geo_name_id)
        if not geo_obj:
            response['message'] = "Geographical object doesn't exist."
            response['http_status_code'] = 404
            abort(**response)

        response['data'] = geo_obj
        return jsonify(**response)
