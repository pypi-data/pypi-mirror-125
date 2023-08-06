__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os

from django.http import HttpResponse
from django.forms.models import model_to_dict
from .models import RouteExec, ComputedField
from .update_models import update_models


def resort_rest_models(all_rest_dict_list):
    for i in all_rest_dict_list:
        print(i)

    return all_rest_dict_list

def write_to_file(to_write_str):

    path1 = os.path.dirname(__file__)
    print('write_to_file-path1:',path1)
    urls_rest_py_file_path = os.path.join(path1,'urls_rest.py')
    print('write_to_file:',urls_rest_py_file_path)
    f_to_w = open(urls_rest_py_file_path,'wb')
    f_to_w.write(to_write_str.encode('utf-8'))
    f_to_w.close()

def list_model_to_dict(all_rest):
    all_rest_dict_list=[]
    for i in all_rest:
        all_rest_dict_list.append(model_to_dict(i))
    return all_rest_dict_list


def none_str(kk):
    return 'None' if kk is None else str(kk)

def generate_rest_code(all_rest_dict_list):
    to_write_str = 'from .models_inspected import *\n'
    to_write_str +='from .my_rest_api import my_rest_viewsetB\n'
    to_write_str += 'from .urls import router\n'

    for i in all_rest_dict_list:
        to_write_str+='####################################\n'
        to_write_str += '#for route'+i['route']+'\n'
        to_write_str += i['import_py_code']+'\n'
        to_write_str += 'routeName="' + i['route']+'"\n'
        to_write_str += """
if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
"""
        to_write_str +='foreign_key_ro = ' +none_str(i['foreign_key_ro'])+'\n'
        to_write_str += 'foreign_key_id = ' + none_str(i['foreign_key_id']) + '\n'
        to_write_str += 'model_obj_list = ' + none_str(i['model_object_list']) + '\n'
        to_write_str += 'filter_fields = None\n' #+ none_str(i['filter_fields']) + '\n'
        to_write_str += 'no_need_login = ' + none_str(i['no_need_login']) + '\n'
        to_write_str += 'search_fieldsA = ' + none_str(i['search_fields']) + '\n'
        to_write_str += 'ordering = ' + none_str(i['ordering']) + '\n'
        to_write_str += 'ordering_fields = ' + none_str(i['ordering_fields']) + '\n'
        to_write_str += 'filter_keys = ' + none_str(i['filter_keys']) + '\n'
        to_write_str += 'foreign_slug_kf = ' + none_str(i['foreign_slug_kf']) + '\n'

        to_write_str += 'if model_obj_list is None:\n    model_obj_list="__all__"\n'

        to_write_str += 'if foreign_key_id is not None:\n    for i in foreign_key_id:\n        foreign_key_id[i]= globals()[foreign_key_id[i][0]]\n'

        to_write_str +=  "choice_problems = my_rest_viewsetB(" + str(i['table_big_name']) + ", tableBName + 'V',"
        to_write_str += """

                                               model_obj_list=model_obj_list, no_need_login=no_need_login,
                                               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
                                               filter_fieldsA=filter_fields,
                                               search_fieldsA=search_fieldsA, orderingA=ordering,
                                               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
                                               foreign_slug_kf=foreign_slug_kf)
                                               \n
                                               """
        to_write_str += '\nrouter.register(routeName, choice_problems) \n'
        to_write_str += '####################################\n'


    return to_write_str
def update_rest(request):
    """
    将各rest的依赖关系顺序整理好
    依次输出代码至 urls_rest
    """
    all_rest = RouteExec.objects.all()
    all_rest_dict_list=list_model_to_dict(all_rest)

    all_rest_dict_list = resort_rest_models(all_rest_dict_list)

    update_models(all_rest_dict_list)

    to_write_str=generate_rest_code(all_rest_dict_list)
    write_to_file(to_write_str)


    return HttpResponse('generate')
