"""
靓号 视图函数
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import PrettyModelForm


def pretty_list(request):
    """靓号列表 - 返回JSON格式数据"""
    try:
        # 搜索
        mobile = request.GET.get("mobile", '')
        level = request.GET.get("level", '')
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 10))
        
        date_dict = {}
        if mobile:
            date_dict["mobile__contains"] = mobile
        if level:
            date_dict['level'] = level

        queryset = models.PrettyNum.objects.filter(**date_dict).order_by("-level")
        
        # 计算总数
        total = queryset.count()
        
        # 分页
        start = (page - 1) * size
        end = start + size
        queryset = queryset[start:end]
        
        # 将查询集转换为列表
        pretty_list = []
        for pretty in queryset:
            pretty_list.append({
                'id': pretty.id,
                'mobile': pretty.mobile,
                'price': pretty.price,
                'level': pretty.level,
                'status': pretty.status,
                'level_text': pretty.get_level_display(),
                'status_text': pretty.get_status_display()
            })
        
        return JsonResponse({
            'code': 200,
            'message': '获取靓号列表成功',
            'data': {
                'items': pretty_list,
                'total': total
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取靓号列表失败: {str(e)}'
        }, status=500)


@csrf_exempt
def pretty_add(request):
    """添加靓号 - 返回JSON格式数据"""
    if request.method == 'GET':
        return JsonResponse({
            'code': 200,
            'message': '获取添加靓号页面成功',
            'data': {}
        })
    
    try:
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            pretty = form.save()
            return JsonResponse({
                'code': 200,
                'message': '添加靓号成功',
                'data': {
                    'id': pretty.id,
                    'mobile': pretty.mobile,
                    'price': pretty.price,
                    'level': pretty.level,
                    'status': pretty.status,
                    'level_text': pretty.get_level_display(),
                    'status_text': pretty.get_status_display()
                }
            })
        else:
            # 提取表单错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            return JsonResponse({
                'code': 400,
                'message': '添加靓号失败',
                'data': {
                    'errors': errors
                }
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'添加靓号失败: {str(e)}'
        }, status=500)


@csrf_exempt
def pretty_edit(request, nid):
    """修改靓号 - 返回JSON格式数据"""
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '靓号不存在'
        }, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'code': 200,
            'message': '获取修改靓号页面成功',
            'data': {
                'id': row_object.id,
                'mobile': row_object.mobile,
                'price': row_object.price,
                'level': row_object.level,
                'status': row_object.status,
                'level_text': row_object.get_level_display(),
                'status_text': row_object.get_status_display()
            }
        })
    
    try:
        form = PrettyModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            pretty = form.save()
            return JsonResponse({
                'code': 200,
                'message': '修改靓号成功',
                'data': {
                    'id': pretty.id,
                    'mobile': pretty.mobile,
                    'price': pretty.price,
                    'level': pretty.level,
                    'status': pretty.status,
                    'level_text': pretty.get_level_display(),
                    'status_text': pretty.get_status_display()
                }
            })
        else:
            # 提取表单错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            return JsonResponse({
                'code': 400,
                'message': '编辑靓号失败',
                'data': {
                    'errors': errors
                }
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'修改靓号失败: {str(e)}'
        }, status=500)


def pretty_delete(request, nid):
    """删除靓号 - 返回JSON格式数据"""
    try:
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        if not row_object:
            return JsonResponse({
                'code': 404,
                'message': '靓号不存在'
            }, status=404)
        
        models.PrettyNum.objects.filter(id=nid).delete()
        return JsonResponse({
            'code': 200,
            'message': '删除靓号成功'
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'删除靓号失败: {str(e)}'
        }, status=500)
