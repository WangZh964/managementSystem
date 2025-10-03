"""
管理员 视图
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    """管理员列表 - 返回JSON格式数据"""
    # 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['username__contains'] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    
    # 转换查询集为列表
    data_list = []
    for item in page_object.page_queryset:
        data_list.append({
            'id': item.id,
            'username': item.username,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(item, 'created_at') and item.created_at else None
        })

    # 返回JSON数据
    return JsonResponse({
        'code': 200,
        'message': '获取管理员列表成功',
        'data': {
            'items': data_list,
            'total': queryset.count(),
            'page_string': page_object.html()
        }
    })


@csrf_exempt
def admin_add(request):
    """添加管理员 - 返回JSON格式数据"""
    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '添加管理员成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '添加管理员失败',
            'data': {
                'errors': errors
            }
        }, status=400)


def admin_edit(request, nid):
    """编辑管理员 - 返回JSON格式数据"""
    # 对象 / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '数据不存在'
        }, status=404)

    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '修改管理员成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '编辑管理员失败',
            'data': {
                'errors': errors
            }
        }, status=400)


def admin_delete(request):
    """删除管理员 - 返回JSON格式数据"""
    # 从查询参数中获取uid
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({
            'code': 400,
            'message': '缺少管理员ID参数'
        }, status=400)
    
    # 对象 / None
    row_object = models.Admin.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '数据不存在'
        }, status=404)

    models.Admin.objects.filter(id=uid).delete()
    return JsonResponse({
        'code': 200,
        'message': '删除管理员成功'
    })


@csrf_exempt
def admin_reset(request, nid):
    """重置管理员密码 - 返回JSON格式数据"""
    # 对象 / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '数据不存在'
        }, status=404)

    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '重置密码成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '状态更新失败',
            'data': {
                'errors': errors
            }
        }, status=400)



