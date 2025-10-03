import request from '../utils/request'

// 折线图数据接口
export interface LineChartData {
  legend: string[]
  series_list: any[]
  x_axis: string[]
}

// 柱状图数据接口
export interface BarChartData {
  legend: string[]
  series_list: any[]
  x_axis: string[]
}

// 饼图数据接口
export interface PieChartData {
  value: number
  name: string
}

// 通用响应接口
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 获取折线图数据
export function getLineChartData(): Promise<ApiResponse<LineChartData>> {
  return request({
    url: '/chart/line/',
    method: 'get'
  })
}

// 获取柱状图数据
export function getBarChartData(): Promise<ApiResponse<BarChartData>> {
  return request({
    url: '/chart/bar/',
    method: 'get'
  })
}

// 获取饼图数据
export function getPieChartData(): Promise<ApiResponse<PieChartData[]>> {
  return request({
    url: '/chart/pie/',
    method: 'get'
  })
}

// 获取highcharts实例数据
export function getHighchartsData(): Promise<ApiResponse<any>> {
  return request({
    url: '/chart/highcharts/',
    method: 'get'
  })
}

// 获取图表列表数据
export function getChartListData(): Promise<ApiResponse<any>> {
  return request({
    url: '/chart/',
    method: 'get'
  })
}