"""
用户 视图函数
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import UserModelForm


@csrf_exempt
def user_list(request):
    """用户列表 - 返回JSON格式数据"""
    # 获取所有用户列表 [obj,obj,obj,]
    queryset = models.UserInfo.objects.all()
    
    # 分页
    page_object = Pagination(request, queryset)
    
    # 转换查询集为列表
    data_list = []
    for item in page_object.page_queryset:
        data_list.append({
            'id': item.id,
            'name': item.name,
            'password': item.password,
            'age': item.age,
            'account': float(item.account),  # Decimal转换为float
            'gender': item.gender,
            'depart_id': item.depart_id,
            'depart_title': item.depart.title if item.depart else None,
            'create_time': item.create_time.strftime('%Y-%m-%d') if item.create_time else None
        })

    # 返回JSON数据
    return JsonResponse({
        'code': 200,
        'message': '获取用户列表成功',
        'data': {
            'items': data_list,
            'total': queryset.count()
        }
    })


@csrf_exempt
def user_add(request):
    """添加用户 - 返回JSON格式数据"""
    if request.method == "GET":
        # GET请求返回表单数据
        departments = models.Department.objects.all()
        dept_list = [{'id': dept.id, 'title': dept.title} for dept in departments]
        return JsonResponse({
            'code': 200,
            'message': '获取部门列表成功',
            'data': dept_list
        })

    # 用户POST提交数据，数据校验
    print("=== 用户添加调试信息开始 ===")
    print(f"请求方法: {request.method}")
    print(f"请求头Content-Type: {request.content_type}")
    print(f"POST数据: {dict(request.POST)}")
    print(f"FILES数据: {dict(request.FILES)}")
    
    # 处理前端发送的depart_id转换为depart对象
    post_data = request.POST.copy()
    depart_id = post_data.get('depart_id')
    if depart_id:
        # 将depart_id转换为depart对象
        try:
            depart_object = models.Department.objects.get(id=depart_id)
            post_data['depart'] = depart_object.id  # 设置depart字段为部门对象的ID
            print(f"成功将depart_id {depart_id} 转换为depart对象")
        except models.Department.DoesNotExist:
            print(f"部门ID {depart_id} 不存在")
            return JsonResponse({
                'code': 400,
                'message': '部门不存在',
                'data': {
                    'errors': {'depart': ['选择的部门不存在']}
                }
            })
    
    form = UserModelForm(data=post_data)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        print("表单验证成功，准备保存数据")
        form.save()
        print("用户数据保存成功")
        return JsonResponse({
            'code': 200,
            'message': '添加用户成功'
        })

    # 校验失败，返回错误信息
    print("=== 表单验证失败 ===")
    print(f"表单错误详情: {form.errors}")
    print(f"表单数据: {form.data}")
    print("=== 用户添加调试信息结束 ===")
    
    return JsonResponse({
            'code': 400,
            'message': '添加用户失败',
            'data': {
                'errors': form.errors
            }
        })


@csrf_exempt
def user_edit(request, nid):
    """编辑用户 - 返回JSON格式数据"""
    # 根据id去数据库获取要编辑的那一行数据（对象）
    row_object = models.UserInfo.objects.filter(id=nid).first()
    
    if not row_object:
        return JsonResponse({
            'code': 404,
            'message': '用户不存在'
        })

    if request.method == "GET":
        # GET请求返回用户数据和部门列表
        departments = models.Department.objects.all()
        dept_list = [{'id': dept.id, 'title': dept.title} for dept in departments]
        
        user_data = {
            'id': row_object.id,
            'name': row_object.name,
            'password': row_object.password,
            'age': row_object.age,
            'account': float(row_object.account),
            'gender': row_object.gender,
            'depart_id': row_object.depart_id
        }
        
        return JsonResponse({
            'code': 200,
            'message': '获取用户信息成功',
            'data': {
                'user': user_data,
                'departments': dept_list
            }
        })

    # 添加调试信息
    print("=== 用户编辑调试信息开始 ===")
    print(f"请求方法: {request.method}")
    print(f"请求头Content-Type: {request.content_type}")
    print(f"POST数据: {dict(request.POST)}")
    print(f"FILES数据: {dict(request.FILES)}")
    
    # 处理前端发送的depart_id转换为depart对象
    post_data = request.POST.copy()
    depart_id = post_data.get('depart_id')
    if depart_id:
        # 将depart_id转换为depart对象
        try:
            depart_object = models.Department.objects.get(id=depart_id)
            post_data['depart'] = depart_object.id  # 设置depart字段为部门对象的ID
            print(f"成功将depart_id {depart_id} 转换为depart对象")
        except models.Department.DoesNotExist:
            print(f"部门ID {depart_id} 不存在")
            return JsonResponse({
                'code': 400,
                'message': '部门不存在',
                'data': {
                    'errors': {'depart': ['选择的部门不存在']}
                }
            })
    
    form = UserModelForm(data=post_data, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        print("表单验证成功，准备保存数据")
        form.save()
        print("用户数据保存成功")
        return JsonResponse({
            'code': 200,
            'message': '编辑用户成功'
        })
    
    # 校验失败，返回错误信息
    print("=== 表单验证失败 ===")
    print(f"表单错误详情: {form.errors}")
    print(f"表单数据: {form.data}")
    print("=== 用户编辑调试信息结束 ===")
    
    return JsonResponse({
            'code': 400,
            'message': '编辑用户失败',
            'data': {
                'errors': form.errors
            }
        })


@csrf_exempt
def user_delete(request, nid):
    """删除用户 - 返回JSON格式数据"""
    try:
        models.UserInfo.objects.filter(id=nid).delete()
        return JsonResponse({
            'code': 200,
            'message': '删除用户成功'
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'删除用户失败: {str(e)}'
        })
