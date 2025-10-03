from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def chart_list(request):
    """数据统计页面 - 返回JSON格式数据"""
    return JsonResponse({
        'code': 200,
        'message': '获取数据统计页面成功',
        'data': {}
    })


@csrf_exempt
def chart_bar(request):
    """ 构造柱状图的数据 - 返回JSON格式数据"""
    try:
        # 数据可以去数据库中获取
        legend = ["萧炎", "美杜莎"]

        series_list = [
            {
                "name": '萧炎',
                "type": 'bar',
                "data": [15, 20, 36, 10, 10, 100]
            },
            {
                "name": '美杜莎',
                "type": 'bar',
                "data": [30, 40, 66, 20, 20, 100]
            }
        ]

        x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

        result = {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }

        return JsonResponse({
            'code': 200,
            'message': '获取柱状图数据成功',
            'data': result
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取柱状图数据失败: {str(e)}'
        }, status=500)


@csrf_exempt
def chart_pie(request):
    """ 构造饼图的数据 - 返回JSON格式数据"""
    try:
        db_data_list = [
            {"value": 2048, "name": 'IT部门'},
            {"value": 1735, "name": '运营'},
            {"value": 580, "name": '新媒体'},
        ]

        return JsonResponse({
            'code': 200,
            'message': '获取饼图数据成功',
            'data': db_data_list
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取饼图数据失败: {str(e)}'
        }, status=500)


@csrf_exempt
def chart_line(request):
    """ 构造折线图的数据 - 返回JSON格式数据"""
    try:
        legend = ["河北", "上海"]

        series_list = [
            {
                "name": '河北',
                "type": 'line',
                "stack": 'Total',
                "data": [15, 20, 36, 10, 10, 100]
            },
            {
                "name": '上海',
                "type": 'line',
                "stack": 'Total',
                "data": [30, 40, 66, 20, 20, 100]
            }
        ]

        x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

        result = {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }

        return JsonResponse({
            'code': 200,
            'message': '获取折线图数据成功',
            'data': result
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取折线图数据失败: {str(e)}'
        }, status=500)


def chart_highcharts(request):
    """ highcharts实例 - 返回JSON格式数据"""
    return JsonResponse({
        'code': 200,
        'message': '获取highcharts实例成功',
        'data': {}
    })
