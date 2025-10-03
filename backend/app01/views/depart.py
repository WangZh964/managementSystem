"""
部门 视图函数
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import DepartModelForm


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()

    # 分页
    page_object = Pagination(request, queryset)
    
    # 转换查询集为列表
    data_list = []
    for item in page_object.page_queryset:
        data_list.append({
            'id': item.id,
            'title': item.title
        })

    # 返回JSON数据
    return JsonResponse({
        'code': 200,
        'message': '获取部门列表成功',
        'data': data_list,
        'total': queryset.count(),
        'page_string': page_object.html()
    })


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)

    # 用户POST提交数据，数据校验
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '添加部门成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '添加部门失败',
            'data': {
                'errors': errors
            }
        }, status=400)


def depart_delete(request, nid):
    """删除部门"""
    try:
        # 检查部门是否存在
        department = models.Department.objects.filter(id=nid).first()
        if not department:
            return JsonResponse({
                'code': 404,
                'message': '部门不存在'
            }, status=404)
        
        # 删除部门
        models.Department.objects.filter(id=nid).delete()
        return JsonResponse({
            'code': 200,
            'message': '删除部门成功'
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'删除部门失败: {str(e)}'
        }, status=500)


def depart_edit(request, nid):
    """修改部门"""
    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)
    
    try:
        # 根据id去数据库获取要编辑的那一行数据（对象）
        row_object = models.Department.objects.filter(id=nid).first()
        if not row_object:
            return JsonResponse({
                'code': 404,
                'message': '部门不存在'
            }, status=404)
        
        form = DepartModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # 校验成功
            form.save()
            return JsonResponse({
                'code': 200,
                'message': '修改部门成功'
            })
        else:
            # 校验失败，返回错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            return JsonResponse({
            'code': 400,
            'message': '修改部门失败',
            'data': {
                'errors': errors
            }
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'修改部门失败: {str(e)}'
        }, status=500)
