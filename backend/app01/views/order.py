from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootstrapModelForm
from app01 import models
import random
from datetime import datetime
from app01.utils.pagination import Pagination


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    """订单列表 - 返回JSON格式数据"""
    queryset = models.Order.objects.all().order_by('-id')
    
    # 分页
    page_object = Pagination(request, queryset)
    
    # 转换查询集为列表
    data_list = []
    for item in page_object.page_queryset:
        data_list.append({
            'id': item.id,
            'oid': item.oid,
            'title': item.title,
            'price': item.price,
            'status': item.status,
            'admin': {
                'id': item.admin.id,
                'username': item.admin.username
            } if item.admin else None,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(item, 'created_at') and item.created_at else None
        })

    # 返回JSON数据
    return JsonResponse({
        'code': 200,
        'message': '获取订单列表成功',
        'data': data_list,
        'total': queryset.count(),
        'page_string': page_object.html()
    })


@csrf_exempt
def order_add(request):
    """添加订单 - 返回JSON格式数据"""
    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)

    # 用户POST提交数据，数据校验
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：额外添加一些不是用户输入的值
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 固定设置管理员ID - 这里暂时使用默认值1，实际应该从session中获取
        form.instance.admin_id = request.session.get("info", {}).get("id", 1)

        # 如果数据合法，保存到数据库
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '添加订单成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '添加订单失败',
            'data': {
                'errors': errors
            }
        }, status=400)


def order_delete(request):
    """删除订单 - 返回JSON格式数据"""
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({
            'code': 400,
            'message': '缺少订单ID参数'
        }, status=400)

    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({
            'code': 404,
            'message': '订单不存在'
        }, status=404)

    models.Order.objects.filter(id=uid).delete()

    return JsonResponse({
        'code': 200,
        'message': '删除订单成功'
    })


def order_detail(request):
    """根据ID获取订单信息 - 返回JSON格式数据"""
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({
            'code': 400,
            'message': '缺少订单ID参数'
        }, status=400)
        
    row_dict = models.Order.objects.filter(id=uid).values('id', 'oid', 'title', 'price', 'status', 'admin_id').first()
    if not row_dict:
        return JsonResponse({
            'code': 404,
            'message': '订单不存在'
        }, status=404)

    # 获取管理员信息
    admin_info = None
    if row_dict.get('admin_id'):
        admin = models.Admin.objects.filter(id=row_dict['admin_id']).first()
        if admin:
            admin_info = {
                'id': admin.id,
                'username': admin.username
            }

    # 从数据库中获取到一个对象 row_obj
    result = {
        "id": row_dict['id'],
        "oid": row_dict['oid'],
        "title": row_dict['title'],
        "price": row_dict['price'],
        "status": row_dict['status'],
        "admin": admin_info
    }
    
    return JsonResponse({
        'code': 200,
        'message': '获取订单详情成功',
        'data': result
    })


@csrf_exempt
def order_edit(request):
    """编辑订单 - 返回JSON格式数据"""
    if request.method == 'GET':
        # 前端不需要GET请求，直接返回错误
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)
        
    uid = request.POST.get("uid") or request.GET.get("uid")
    if not uid:
        return JsonResponse({
            'code': 400,
            'message': '缺少订单ID参数'
        }, status=400)
        
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '订单不存在'
        }, status=404)

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'code': 200,
            'message': '修改订单成功'
        })
    else:
        # 校验失败，返回错误信息
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        
        return JsonResponse({
            'code': 400,
            'message': '编辑订单失败',
            'data': {
                'errors': errors
            }
        }, status=400)