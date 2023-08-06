# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import io
from .models import RouteExec, ComputedField
import json
from django.http import HttpResponse


def update_table_id(depth=0):
    """
    更新表的id。
    根据各表的依赖关系，更新id
    """
    if depth > 20:
        print('update_table_id loop infinite')
        return 0

    table_exist = 1
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM route_exec;")
            row = cursor.fetchone()
    except Exception as e:
        print('no route_exec exist? just return')
        table_exist = 0

    if table_exist == 0:
        return

    # filter(re_type='table').
    tables = RouteExec.objects.all().order_by('id')

    # 保存所有的表： ['Danwei', 'Gongyingshang', 'Fenlei', 'Cpfenlei', 'Zhiwei']
    has_tables = []
    # {'Danwei':4, } Danwei表的id需要在4前面（id=4的表，需要Danwei表做外键）
    table_to_up = {}
    for i in tables:
        curr_table = i.route.replace('/', '')
        if curr_table in has_tables:
            # 如果重复，则后一个不再统计
            print('WARN: table duplicated in RouteExec', curr_table)
            continue
        has_tables.append(curr_table)
        params_updata(i)
        if i.params is not None:
            params = parse_params(i.params)
            if 'foreign_key_id' not in params:
                continue

            for fk in params['foreign_key_id']:
                table_foreign_l = params['foreign_key_id'][fk]
                table_foreign = table_foreign_l[0]
                if table_foreign not in has_tables:
                    if table_foreign not in table_to_up:
                        table_to_up[table_foreign] = i.id
                    elif table_to_up[table_foreign] > i.id:
                        table_to_up[table_foreign] = i.id

    # print('has_tables', has_tables)
    # print('table_to_up', table_to_up)

    for i in list(table_to_up.keys()):
        if i not in has_tables:
            # print('no table found. will not change order', i)
            del table_to_up[i]

    # 表是需要转移
    if len(table_to_up) == 0:
        return 0

    # print('table resotr:', table_to_up)
    for table_name in table_to_up:
        table_to_id = table_to_up[table_name]
        tables_gte = RouteExec.objects.filter(id__gte=table_to_id).all().order_by('-id')
        for i in tables_gte:
            iid = i.id
            i.id = iid + 1
            i.save()
            i.id = iid
            i.delete()
        tb_target = RouteExec.objects.get(route='/' + table_name)
        tb_target.id = table_to_id
        tb_target.save()

        # update_table_id(depth+1)

    return 0


def parse_params(params_str):
    ret_dict = {}
    if params_str is None:
        return ret_dict
    if len(params_str) == 0:
        return ret_dict

    if isinstance(params_str, dict):
        return params_str
    try:
        ret_dict = json.loads(params_str)
    except Exception as e:
        print(e)
        print('param parse error')
        print(params_str)

    return ret_dict


def foreign_key_gen(table_name, related_name, del_type='CASCADE'):
    """
    del_type: CASCADE SET_NULL DO_NOTHING

    """

    return "models.ForeignKey(to=" + table_name + ", db_constraint=False, on_delete=models."+del_type+", blank=True, null=True, related_name='" + related_name + "')"

def str_to_obj(obj):
    if obj is None:
        return obj
    return json.loads(obj)


def params_foreign_key_id_update(one_r):
    if one_r['foreign_key_id'] is None:
        return one_r
    if one_r['foreign_key_id'] == '':
        return one_r
    fk = str_to_obj(one_r['foreign_key_id'])
    need_save = 0
    for i in fk:
        if isinstance(fk[i], str):
            fk[i] = [fk[i], 'CASCADE']
            need_save = 1

    if need_save:
        one_r['foreign_key_id'] = json.dumps(fk, indent=2)

    return one_r

def params_updata(one_r: dict):
    one_r = params_foreign_key_id_update(one_r)

    params = {
        'foreign_key_id': str_to_obj(one_r['foreign_key_id']),
        'foreign_key_ro': str_to_obj(one_r['foreign_key_ro']),
        'foreign_slug_kf': str_to_obj(one_r['foreign_slug_kf']),
        'ordering_fields': str_to_obj(one_r['ordering_fields']),
        'ordering': str_to_obj(one_r['ordering']),
        'no_need_login': one_r['no_need_login'],
        'search_fields': str_to_obj(one_r['search_fields']),
        'filter_keys': str_to_obj(one_r['filter_keys']),
        'model_object_list': str_to_obj(one_r['model_object_list'])
    }

    for i in list(params.keys()):
        if params[i] is None:
            del params[i]
    one_r['params'] = json.dumps(params)
    return one_r



def rewrite_model_inspected_when_production():
    from django.conf import settings

    if settings.IN_PRODUCTION!=True:
        return

    BASE_DIR = settings.BASE_DIR
    file_name = str(BASE_DIR) + r'/AmisBack/models_inspected.py'
    f = open(file_name, 'r')
    old_file_cont = f.read()
    f.close()
    f2 = io.StringIO()

    alread_done = 0
    # 当前model名
    curr_class_name = ''

    for one_line in old_file_cont.split('\n'):
        if len(one_line.strip()) == 0:
            # 空行
            f2.write(one_line + "\n")
            continue
        one_line_start_space = len(one_line) - len(one_line.lstrip())
        one_line_striped = one_line.strip()
        if one_line_striped[0] == '#':
            # 注释
            f2.write(one_line + "\n")
            continue
        spt = one_line_striped.split(' ')
        if len(spt) == 0:
            # 没有空格，不认识的行??
            f2.write(one_line + "\n")
            continue
        if (one_line_start_space==0) and (spt[0] == 'class'):
            # 获取类名
            curr_class_name = spt[1].split('(')[0]
            f2.write(one_line + "\n")
            continue
        elif spt[0] == 'class':
            f2.write(one_line + "\n")
            continue

        curr_field_name = spt[0]
        if curr_field_name!='managed':
            #不是需要的字段，直接复制
            f2.write(one_line + "\n")
            continue

        #此处处理managed. 由False改为True
        if len(spt)!=3:
            print('unknown line:', spt)
            continue

        if spt[2]=='True':
            print('already done. skip')
            alread_done = 1
            continue
        f2.write(' ' * one_line_start_space + "managed = True\n")

    if alread_done==0:
        cont  = f2.getvalue()
        f=open(file_name, 'w')
        f.write(cont)
        f.close()


def update_models(all_rest_dict_list):
    """
    更新模型文件
    1 读取routeexec种的表名，使用命令inspected生成默认表结构
    2 替换foreign_key 字段
    3 去掉id字段。id如果存在，会导致django程序错误。针对部分表导出后有id的问题
    """
    from django.core.management import call_command
    from django.conf import settings
    import os

    path1 = os.path.dirname(__file__)
    file_name = os.path.join(path1,'models_inspected.py')

    print(file_name)

    #保存inspectdb数据到stringio.
    f = io.StringIO()

    f.write("from django.contrib.auth.models import User\n")
    #f.write("from AmisNavigationBar.models import AmisNavigation\n")

    table_list = []
    for i in all_rest_dict_list:
        if i['inspected_from_db'] !=1:
            continue
        table_list.append(i['table_name'])
    if len(table_list) > 0:
        call_command("inspectdb", table_list, stdout=f)
    else:
        f.write('#no table exist in route_exec\n')
    # 所有数据读出到字符串变量：models_new
    models_new = f.getvalue()
    f.close()


    # 此变量用户下面的model外键更改
    # key:className
    # value:{ foreign_key_id中的key _id : foreign_key_id_value  }
    foreign_key_dict2 = {}
    for one_r in all_rest_dict_list:
        # if one_r.re_type == 'table':
        one_r = params_updata(one_r)
        params = parse_params(one_r['params'])
        if one_r['inspected_from_db'] != 1:
            continue
        if 'foreign_key_id' in params:
            foreign_key_dict2[one_r['table_big_name']] = {}
            for k in params['foreign_key_id']:
                foreign_key_dict2[one_r['table_big_name']][k + '_id'] = params['foreign_key_id'][k]

    print('update_models foreign_key_dict2:', foreign_key_dict2)

    # 当前model名
    curr_class_name = ''
    f2 = open(file_name, 'w+')
    for one_line in models_new.split('\n'):
        #每行分析处理
        if len(one_line.strip()) == 0:
            # 空行
            f2.write(one_line + "\n")
            continue
        one_line_start_space = len(one_line) - len(one_line.lstrip())
        one_line_striped = one_line.strip()
        if one_line_striped[0] == '#':
            # 注释
            f2.write(one_line + "\n")
            continue

        spt = one_line_striped.split(' ')
        if len(spt) == 0:
            # 没有空格，不认识的行??
            f2.write(one_line + "\n")
            continue

        if (one_line_start_space==0) and (spt[0] == 'class'):
            # 获取类名
            curr_class_name = spt[1].split('(')[0]
            f2.write(one_line + "\n")
            continue

        elif spt[0] == 'class':
            #内部类，在内部类之前，先放入计算属性值
            re1 = RouteExec.objects.filter(table_big_name=curr_class_name, inspected_from_db=1).all()
            if len(re1)<1:
                print('skip this table',curr_class_name, len(re1))
            cf = ComputedField.objects.filter(route_exec=re1[0]).all()
            for cfi in cf:
                f2.write(' ' * one_line_start_space+cfi.func_text.replace('\r\n','\n'))
                f2.write(' ' * one_line_start_space+"\n")

            f2.write(one_line + "\n")
            continue

        curr_field_name = spt[0]
        if curr_field_name=='id':
            #id自动去除，避免djanog错误
            f2.write(' ' * one_line_start_space )
            f2.write('#' + one_line)
            f2.write('\n')
            continue


        # managed处理
        if curr_field_name == 'managed' and len(spt) == 3 and spt[2] != 'True':
            # 不是需要的字段，直接复制
            f2.write(' ' * one_line_start_space + "managed = True\n")
            continue

        if curr_class_name not in foreign_key_dict2:
            # 当前class没有外键
            f2.write(one_line + "\n")
            continue

        # 当前class的所有外键
        foreign_key_dict = foreign_key_dict2[curr_class_name]

        # 当前字段是外键
        if curr_field_name in foreign_key_dict:
            # 此行要替换为外键代码

            f2.write(' ' * one_line_start_space)
            f2.write(curr_field_name.replace('_id', ''))
            f2.write(' = ')
            print(curr_class_name, curr_field_name, foreign_key_dict[curr_field_name][0])
            if foreign_key_dict[curr_field_name][0] == curr_class_name:
                itable_name = '"self"'
            else:
                itable_name = foreign_key_dict[curr_field_name][0]

            irelated_name = curr_class_name +'_'+ curr_field_name.replace('_id', '')
            print('irelated_name', irelated_name)
            idel_typ = foreign_key_dict[curr_field_name][1]
            f2.write(foreign_key_gen(itable_name, irelated_name, idel_typ))
            f2.write('\n')
            continue


        f2.write(one_line + "\n")
        continue

    # model写完。此处添加receiver
    path1 = os.path.dirname(__file__)
    file_name_receiver = os.path.join(path1,'models_receiver.py')
    f_recv = open(file_name_receiver, 'r')
    f2.write(f_recv.read())

    f2.close()

    return 'ok'
