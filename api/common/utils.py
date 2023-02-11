import pytz
from datetime import datetime


def file_info_list() -> list[str]:
    """
    Распаковывает файл с данными о географических объектах.
    Возвращает данные файла в виде списка со всеми строками.
    :return:
    """
    with open('api/RU/RU.txt', 'r') as file:
        return file.readlines()


def set_value_and_type(value: str, value_type):
    """
    Функция принимает строку и тип данных, в который необходимо ее преобразовать.
    Возвращает преобразованное значение.
    Если в значении пустая строка, то возвращает None, либо пустой список.
    :param value:
    :param value_type:
    :return:
    """
    if value_type == list:
        alternate_names_list = []
        alternate_names_list.extend(value.split(',')) if value else []
        return alternate_names_list
    return value_type(value) if value else None


def preparing_dict_data_types_to_json(geo_obj: str):
    """
    Функция принимает строку с данными о географическом объекте;
    Строка разбивается на более подстроки с данными, через каждую табуляцию. Полученные подстроки добавляются в список.
    Подготавливает словарь, наполняет его значениями, в соответствии с установленными типами данных
    для каждого значения.

    Возвращает словарь с данными о географическом объекте, подготовленный для преобразования в json.
    :param geo_obj:
    :return:
    """
    geo_obj = geo_obj.replace('\n', '').split('\t')
    dict_to_json = {
        "geo_name_id": int,
        "name": str,
        "ascii_name": str,
        "alternate_names": list,
        "latitude": float,
        "longitude": float,
        "feature_class": str,
        "feature_code": str,
        "country_code": str,
        "cc2": str,
        "admin1_code": str,
        "admin2_code": str,
        "admin3_code": str,
        "admin4_code": str,
        "population": int,
        "elevation": int,
        "dem": int,
        "timezone": str,
        "modification_date": str
    }
    for index, item in enumerate(dict_to_json.items()):
        dict_to_json[item[0]] = set_value_and_type(
            geo_obj[index],
            item[1]
        )
    return dict_to_json


def find_geo_obj_by_geo_name_id(geo_name_id: int):
    """
    Функция принимает geo_name_id. Ищет в данных из файла информацию о географическом объекте по geo_name_id.
    Если полученный geo_name_id присутствует в файле, то вызывает функцию для подготовки данных в нужный формат и
    возвращает полученный результат.
    Иначе возвращает False
    :param geo_name_id:
    :return:
    """
    geo_obj_infos = file_info_list()
    for geo_obj_info in geo_obj_infos:
        geo_obj_geo_name_id = int(geo_obj_info.split('\t')[0])
        if geo_obj_geo_name_id == geo_name_id:
            return preparing_dict_data_types_to_json(geo_obj_info)
    return False


def create_geo_objs_list(page: int, rows: int):
    """
    Функция принимает страницу и количество элементов на странице в виде двух целых чисел.
    Рассчитываются индексы элементов для строк из файла,
    согласно номеру полученной страницы и количеству элементов на странице.
    Рассчитывается количество географических объектов в файле.
    При успешном итерировании по заданному промежутку индексов,
    найденные данные подготавливаются и добавляются в список.
    При ошибке итерирования формируется сообщение об ошибке.
    В конечном итоге функция возвращает словарь
    с сообщением если возникла ошибка, с количеством географических объектов и список словарей,
    которые содержат данные о найденных объектах.
    :param page:
    :param rows:
    :return:
    """
    first_page_element = page * rows - rows
    last_page_element = page * rows
    geo_obj_infos = file_info_list()
    geo_obj_list = []
    total = len(geo_obj_infos)
    message = None
    try:
        for i in range(first_page_element, last_page_element):
            geo_obj = preparing_dict_data_types_to_json(geo_obj_infos[i])
            geo_obj_list.append(geo_obj)
    except IndexError:
        if not geo_obj_list:
            message = "Page with given number of elements not found."
    finally:
        response = {
            "message": message,
            "total": total,
            "data": geo_obj_list
        }
        return response


def find_biggest_or_first_city(same_name_cities: list):
    """
    Функция принимает список с информацией о географических объектах.
    Если список пуст, то функция возвращает None.
    Если список не пуст, то среди всех географических объектов в списке выбирается один,
    который имеет наибольшее значение в коллекции с ключом "population".
    Если у всех географических объектов значения в коллекциях с ключом "population" равные,
    то функция возвращает первый географический объект из полученного списка.
    :param same_name_cities:
    :return:
    """
    if not same_name_cities:
        return None
    biggest_city_population = -1
    biggest_city_index = 0
    for index, city in enumerate(same_name_cities):
        if city['population'] and city['population'] > biggest_city_population:
            biggest_city_population = city['population']
            biggest_city_index = index
    return same_name_cities[biggest_city_index]


def find_two_ru_cities(first_city: str, second_city: str):
    """
    Функция принимает названия двух городов на русском языке, в виде двух строк и ищет два географических объекта,
    у которых в поле "alternate_names" есть, полученные, названия двух городов на русском языке.
    Вызывается функция чтения данных из файла. Список с данными сохраняется в переменную.
    Полученные строки конвертируются в строки с нижним регистром всех букв.
    Создаются два пустых списка для географических объектов, альтернативные названия на русском языке,
    которых совпадает с полученными на входе названиями городов.

    Далее происходит поиск названий городов на русском языке среди всех географических объектов.
    Если географический объект имеет данные в поле "alternate_names",
    то строка из этого поля конвертируются в нижний регистр и
    строка разбивается на список со строками по разделителю - ",".
    Если названия первого или второго города находятся в списке с альтернативными названиями географического объекта,
    то все данные о географическом объекте добавляются в первый или второй пустой список соответственно.
    Для каждого списка с географическими объектами вызывается функция
    для нахождения объекта с самым большим количеством населения,
    либо выбирается первый объект из списка, если количество населения во географических объектах совпадает.

    Функция возвращает список с найденными и отфильтрованными географическими объектами.
    :param first_city:
    :param second_city:
    :return:
    """
    geo_objs_info = file_info_list()
    first_city = first_city.lower()
    second_city = second_city.lower()
    list_for_first_cities = []
    list_for_second_cities = []
    for geo_obj in geo_objs_info:
        geo_obj_alt_names = geo_obj.split('\t')[3]
        if geo_obj_alt_names:
            geo_obj_alt_names = geo_obj_alt_names.lower().split(',')
            if first_city in geo_obj_alt_names:
                list_for_first_cities.append(preparing_dict_data_types_to_json(geo_obj))
            elif second_city in geo_obj_alt_names:
                list_for_second_cities.append(preparing_dict_data_types_to_json(geo_obj))
    return [
        find_biggest_or_first_city(list_for_first_cities),
        find_biggest_or_first_city(list_for_second_cities)
    ]


def compare_timezones(cities: list):
    """
    Функция сравнивает две временные зоны.
    Если временные зоны равные, то разница в часах ноль.
    Иначе создается некоторая дата и время.
    Затем создаются две переменные с датой и временем, локализованные под первую и вторую временные зоны соответственно.
    Далее находится разница во времени между двумя датами, из большего всегда вычитается меньшее и
    рассчитывается разница во времени в часах.
    Функция возвращает информацию: одинаковая временная зона или нет,
    а также разницу во времени между двумя временными зонами в часах.
    :param cities:
    :return:
    """
    first_city_tz = pytz.timezone(cities[0]['timezone'])
    second_city_tz = pytz.timezone(cities[1]['timezone'])
    if first_city_tz == second_city_tz:
        same_timezones = True
        difference_in_time = 0
    else:
        same_timezones = False
        some_date = datetime(2010, 4, 20, 23, 30, 0)
        date_in_first_timezone = first_city_tz.localize(some_date)
        date_in_second_timezone = second_city_tz.localize(some_date)

        if date_in_first_timezone > date_in_second_timezone:
            difference_in_time = (date_in_first_timezone - date_in_second_timezone).seconds / 60 / 60
        else:
            difference_in_time = (date_in_second_timezone - date_in_first_timezone).seconds / 60 / 60
    return same_timezones, difference_in_time


def compare_latitude(cities: list):
    """
    Функция получает информацию о двух географических объектах и вычисляет какой из них находится севернее.
    Сравнивает их данные из полей 'latitude' и возвращает то название географического объекта,
    у которого это значение больше.
    Возвращает данные из поля 'name'.
    :param cities:
    :return:
    """
    if cities[0]['latitude'] > cities[1]['latitude']:
        return cities[0]['name']
    return cities[1]['name']


def part_city_name_search(part_name: str):
    """
    Функция принимает часть названия географического объекта в виде строки и
    ищет среди всех географических объектов из файла названия, которые начинаются с полученной строки.

    Вызывается функция чтения данных из файла. Список с данными сохраняется в переменную.
    Строка с частью названия конвертируется в строку с буквами в нижнем регистре.
    Создается пустое множество для сбора названий географических объектов, которые содержат в своем названии,
    полученную на вход, строку.
    Выполняется поиск части названия в названии географического объекта, среди все объектов из файла.
    Если часть названия содержится в названии объекта, то происходит более точная проверка.
    Строка с полным названием объекта разбивается на два списка со строками.
    Один список наполняется строками разбитыми по символам - " ", другой по "-".
    Затем если хотя бы один элемент из двух списков начинается со строки, которую функция получила,
    то найденное оригинальное название географического объекта добавляется в множество с найденными названиями.

    Возвращает список с найденными городами.
    :param part_name:
    :return:
    """
    geo_objs_info = file_info_list()
    part_name = part_name.lower()
    set_with_finding_cities = set()
    for geo_obj in geo_objs_info:
        geo_obj_name = geo_obj.split('\t')[1]
        geo_obj_name_lower_case = geo_obj_name.lower()
        if part_name in geo_obj_name_lower_case:
            geo_obj_name_without_spaces = geo_obj_name_lower_case.split(' ')
            geo_obj_name_without_hyphen = geo_obj_name_lower_case.split('-')
            part_name_is_listed = any(
                list(map(lambda name: name.startswith(part_name), geo_obj_name_without_spaces))
            ) or any(
                list(map(lambda name: name.startswith(part_name), geo_obj_name_without_hyphen))
            )
            if part_name_is_listed:
                set_with_finding_cities.add(geo_obj_name)

    return list(set_with_finding_cities)
