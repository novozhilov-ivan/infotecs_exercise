from flask import jsonify
from flask_restful import Resource, reqparse, abort

from api.common import *

parser = reqparse.RequestParser()
parser.add_argument(
    'page',
    type=int,
    location='args'
)
parser.add_argument(
    'rows',
    type=int,
    location='args'
)


class PageWithCities(Resource):
    @staticmethod
    def get():
        """
        Метод с помощью reqparse.RequestParser() и parse_args() получает из url два значения "page" и "rows".
        Если аргументы отсутствуют или их значения меньше нуля, то отвечает со статус-кодом 400 BAD REQUEST и
        json файлом
            {
         "message": "Values of pages and rows must be greater than zero.",
         "total": null,
         "data": []
            }
        Если аргументы есть и являются положительными,
        то вызывается функция для нахождения страницы и элементов со страницы.
        Если функция возвращает словарь полем "data", в котором есть данные,
        то отправляется ответ со статус-кодом 200 ОК и json файлом с найденными данными.
        Если поле "data" содержит пустой список, то возвращает ответ со статус-кодом 404 NOT FOUND и json файл
            {
         "message": "Page with given number of elements not found.",
         "total": 366931,
         "data": []
            }
        """
        response = {
            "message": None,
            "total": None,
            "data": []
        }
        args = parser.parse_args()
        page = args['page']
        rows = args['rows']

        if not page or not rows or (page <= 0) or (rows <= 0):
            response["message"] = "Values of pages and rows must be greater than zero."
            response["http_status_code"] = 400
            abort(**response)

        response_info = create_geo_objs_list(args['page'], args['rows'])

        if not response_info["data"]:
            response_info["http_status_code"] = 404
            abort(**response_info)
        return jsonify(response_info)
