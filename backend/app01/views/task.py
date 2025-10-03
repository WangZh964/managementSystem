import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from app01 import models
from django import forms
from app01.utils.bootstrap import BootstrapModelForm


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'detail', 'level']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为detail字段使用Textarea widget
        self.fields['detail'].widget = forms.Textarea(attrs={'rows': 3})


def task_list(request):
    """ 任务列表 """
    try:
        # 获取分页参数
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        
        # 获取搜索参数
        level = request.GET.get('level')
        
        # 构建查询条件
        queryset = models.Task.objects.all().order_by('-id')
        
        # 添加搜索条件
        if level:
            queryset = queryset.filter(level=level)
        
        # 分页处理
        paginator = Paginator(queryset, size)
        page_obj = paginator.get_page(page)
        
        # 序列化数据
        tasks = []
        for task in page_obj:
            tasks.append({
                'id': task.id,
                'level': task.level,
                'title': task.title,
                'detail': task.detail,
                'user_id': task.user_id,
                'user_name': task.user.username if task.user else '',
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S') if task.created_at else None,
            })
        
        # 返回JSON响应
        return JsonResponse({
            'code': 200,
            'message': '获取任务列表成功',
            'data': {
                'items': tasks,
                'total': paginator.count,
                'page': page,
                'size': size,
                'total_pages': paginator.num_pages
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取任务列表失败: {str(e)}',
            'data': None
        })


@csrf_exempt
@require_http_methods(["POST"])
def task_add(request):
    """添加任务"""
    try:
        # 处理表单数据
        form = TaskModelForm(data=request.POST)
        if form.is_valid():
            # 添加当前用户ID
            task = form.save(commit=False)
            # 假设用户已登录，从session中获取用户ID
            user_id = request.session.get('user_id')
            if user_id:
                task.user_id = user_id
            else:
                # 如果没有用户ID，使用默认用户ID为1
                task.user_id = 1
            task.save()
            
            return JsonResponse({
                'code': 200,
                'message': '添加任务成功',
                'data': {
                    'id': task.id,
                    'level': task.level,
                    'title': task.title,
                    'detail': task.detail,
                    'user_id': task.user_id,
                    'user_name': task.user.username if task.user else '',
                    'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S') if task.created_at else None,
                }
            })
        else:
            # 返回详细的表单验证错误信息
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [str(error) for error in errors]
                
            return JsonResponse({
                'code': 400,
                'message': '表单验证失败',
                'data': {'errors': error_messages}
            })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'添加任务失败: {str(e)}',
            'data': None
        })


@csrf_exempt
@require_http_methods(["POST"])
def task_edit(request, nid):
    """编辑任务"""
    try:
        # 获取任务对象
        task = models.Task.objects.filter(id=nid).first()
        if not task:
            return JsonResponse({
                'code': 404,
                'message': '任务不存在',
                'data': None
            })
        
        # 处理表单数据
        form = TaskModelForm(data=request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save()
            return JsonResponse({
                'code': 200,
                'message': '更新任务成功',
                'data': {
                    'id': updated_task.id,
                    'level': updated_task.level,
                    'title': updated_task.title,
                    'detail': updated_task.detail,
                    'user_id': updated_task.user_id,
                    'user_name': updated_task.user.username if updated_task.user else '',
                    'created_at': updated_task.created_at.strftime('%Y-%m-%d %H:%M:%S') if updated_task.created_at else None,
                }
            })
        else:
            # 返回详细的表单验证错误信息
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [str(error) for error in errors]
                
            return JsonResponse({
                'code': 400,
                'message': '表单验证失败',
                'data': {'errors': error_messages}
            })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'更新任务失败: {str(e)}',
            'data': None
        })


@require_http_methods(["DELETE"])
def task_delete(request, nid):
    """删除任务"""
    try:
        task = models.Task.objects.filter(id=nid).first()
        if not task:
            return JsonResponse({
                'code': 404,
                'message': '任务不存在',
                'data': None
            })
            
        models.Task.objects.filter(id=nid).delete()
        return JsonResponse({
            'code': 200,
            'message': '删除任务成功',
            'data': None
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'删除任务失败: {str(e)}',
            'data': None
        })


def task_detail(request, nid):
    """获取任务详情"""
    try:
        task = models.Task.objects.filter(id=nid).values().first()
        if not task:
            return JsonResponse({
                'code': 404,
                'message': '任务不存在',
                'data': None
            })
        
        # 格式化日期
        if 'created_at' in task and task['created_at']:
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return JsonResponse({
            'code': 200,
            'message': '获取任务详情成功',
            'data': task
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取任务详情失败: {str(e)}',
            'data': None
        })

