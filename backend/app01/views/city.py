"""
城市 视图函数
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from app01 import models
from app01.utils.form import CityModelForm


def city_list(request):
    """城市列表 - 返回JSON格式数据"""
    try:
        queryset = models.City.objects.all()
        # 将查询集转换为列表
        city_list = []
        for city in queryset:
            city_list.append({
                'id': city.id,
                'name': city.name,
                'count': city.count,
                # 获取图片URL，如果有图片的话
                'img': city.img.url if city.img else None
            })
        
        return JsonResponse({
            'code': 200,
            'message': '获取城市列表成功',
            'data': {
                'items': city_list,
                'total': len(city_list)
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取城市列表失败: {str(e)}'
        }, status=500)


@csrf_exempt
def city_add(request):
    """添加城市 - 返回JSON格式数据"""
    if request.method == 'GET':
        return JsonResponse({
            'code': 200,
            'message': '获取添加城市页面成功',
            'data': {}
        })
    
    try:
        # 处理图片URL字符串的情况
        data = {}
        
        # 如果是JSON请求，从request.body获取数据
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
        else:
            # 如果是表单数据，从request.POST获取
            data = request.POST.copy() if request.POST else {}
        
        # 如果img字段是字符串（URL），而不是文件对象
        img_value = data.get('img')
        
        # 如果图片已经通过上传接口保存（是URL字符串），我们直接创建数据库记录
        if img_value and isinstance(img_value, str) and img_value.startswith('/media/'):
            # 直接创建数据库记录，不经过表单验证
            city = models.City(
                name=data.get('name'),
                count=data.get('count'),
                img=img_value.replace('/media/', '')
            )
            city.save()
            
            return JsonResponse({
                'code': 200,
                'message': '添加城市成功',
                'data': {
                    'id': city.id,
                    'name': city.name,
                    'count': city.count,
                    'img': city.img.url if city.img else None
                }
            })
        
        # 如果是文件上传的情况，使用表单验证
        form = CityModelForm(data=data, files=request.FILES)
        if form.is_valid():
            city = form.save()
            
            return JsonResponse({
                'code': 200,
                'message': '添加城市成功',
                'data': {
                    'id': city.id,
                    'name': city.name,
                    'count': city.count,
                    'img': city.img.url if city.img else None
                }
            })
        else:
            # 提取表单错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            # 打印详细的错误信息到控制台，便于调试
            print(f"添加城市表单验证失败 - 错误详情: {errors}")
            print(f"接收到的数据: {data}")
            
            return JsonResponse({
            'code': 400,
            'message': '表单验证失败',
            'data': {
                'errors': errors
            }
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'添加城市失败: {str(e)}'
        }, status=500)


@csrf_exempt
def city_edit(request, nid):
    """编辑城市 - 返回JSON格式数据"""
    row_object = models.City.objects.filter(id=nid).first()
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '城市不存在'
        }, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'code': 200,
            'message': '获取编辑城市页面成功',
            'data': {
                'id': row_object.id,
                'name': row_object.name,
                'count': row_object.count,
                'img': row_object.img.url if row_object.img else None
            }
        })
    
    try:
        # 处理图片URL字符串的情况
        data = request.POST.copy() if request.POST else {}
        
        # 如果是JSON请求，从request.body获取数据
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
        
        # 如果img字段是字符串（URL），而不是文件对象
        img_value = data.get('img')
        
        # 如果图片已经通过上传接口保存（是URL字符串），我们直接更新数据库记录
        if img_value and isinstance(img_value, str) and img_value.startswith('/media/'):
            # 直接更新数据库记录，不经过表单验证
            row_object.name = data.get('name', row_object.name)
            row_object.count = data.get('count', row_object.count)
            row_object.img.name = img_value.replace('/media/', '')
            row_object.save()
            
            return JsonResponse({
                'code': 200,
                'message': '编辑城市成功',
                'data': {
                    'id': row_object.id,
                    'name': row_object.name,
                    'count': row_object.count,
                    'img': row_object.img.url if row_object.img else None
                }
            })
        
        # 如果是文件上传的情况，使用表单验证
        form = CityModelForm(data=data, files=request.FILES, instance=row_object)
        if form.is_valid():
            city = form.save()
            
            return JsonResponse({
                'code': 200,
                'message': '编辑城市成功',
                'data': {
                    'id': city.id,
                    'name': city.name,
                    'count': city.count,
                    'img': city.img.url if city.img else None
                }
            })
        else:
            # 提取表单错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            # 打印详细的错误信息到控制台，便于调试
            print(f"表单验证失败 - 错误详情: {errors}")
            print(f"接收到的数据: {data}")
            
            return JsonResponse({
                'code': 400,
                'message': '表单验证失败',
                'data': {
                    'errors': errors
                }
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'编辑城市失败: {str(e)}'
        }, status=500)


def city_delete(request, nid):
    """删除城市 - 返回JSON格式数据"""
    try:
        row_object = models.City.objects.filter(id=nid).first()
        if not row_object:
            return JsonResponse({
                'code': 404,
                'message': '城市不存在'
            }, status=404)
        
        models.City.objects.filter(id=nid).delete()
        return JsonResponse({
            'code': 200,
            'message': '删除城市成功'
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'删除城市失败: {str(e)}'
        }, status=500)


@csrf_exempt
def city_upload(request):
    """城市图片上传 - 返回JSON格式数据"""
    if request.method != 'POST':
        return JsonResponse({
            'code': 405,
            'message': '方法不允许'
        }, status=405)
    
    try:
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({
                'code': 400,
                'message': '请选择要上传的文件'
            }, status=400)
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if file.content_type not in allowed_types:
            return JsonResponse({
                'code': 400,
                'message': '只支持JPEG、PNG、GIF格式的图片'
            }, status=400)
        
        # 验证文件大小（最大5MB）
        if file.size > 5 * 1024 * 1024:
            return JsonResponse({
                'code': 400,
                'message': '文件大小不能超过5MB'
            }, status=400)
        
        # 创建城市图片目录（如果不存在）
        media_city_dir = os.path.join(settings.MEDIA_ROOT, 'city')
        if not os.path.exists(media_city_dir):
            os.makedirs(media_city_dir)
        
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.name)[1]
        import uuid
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(media_city_dir, unique_filename)
        
        # 保存文件
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # 返回文件URL
        file_url = f"/media/city/{unique_filename}"
        
        return JsonResponse({
            'code': 200,
            'message': '文件上传成功',
            'data': {
                'url': file_url,
                'filename': unique_filename
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'文件上传失败: {str(e)}'
        }, status=500)


