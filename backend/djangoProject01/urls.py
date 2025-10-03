from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from app01.views import depart, user, pretty, admin, account, city, avatar, task, order, chart

urlpatterns = [
    # 默认访问用户列表页面
    path('', user.user_list),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/<int:nid>/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 靓号管理
    path('pretty/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # 管理员管理
    path('admin/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 注册
    path('register/', account.register),

    

    # 上传图片
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 城市列表
    path('city/', city.city_list),
    path('city/add/', city.city_add),
    path('city/<int:nid>/edit/', city.city_edit),
    path('city/<int:nid>/delete/', city.city_delete),
    path('city/upload/', city.city_upload),

    # 头像
    path('avatar/edit/', avatar.avatar_edit),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),
    path('task/<int:nid>/edit/', task.task_edit),
    path('task/<int:nid>/delete/', task.task_delete),
    path('task/<int:nid>/detail/', task.task_detail),

    # 订单管理
    path('order/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.chart_highcharts),


]
