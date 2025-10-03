import api from './index'

// 城市接口定义
export interface City {
  id?: number
  name: string
  count: number
  img: string
}

// 获取城市列表响应接口
export interface CityListResponse {
  code: number
  message: string
  data: {
    items: City[]
    total: number
  }
}

// 添加城市响应接口
export interface AddCityResponse {
  code: number
  message: string
  data: City
}

// 更新城市响应接口
export interface UpdateCityResponse {
  code: number
  message: string
  data: City
}

// 删除城市响应接口
export interface DeleteCityResponse {
  code: number
  message: string
}

// 获取城市列表
export const getCityList = (params?: { page?: number; size?: number; name?: string }) => {
  return api.get('/city/', { params })
}

// 添加城市
export const addCity = (data: any) => {
  return api.post<AddCityResponse>('/city/add/', data, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

// 更新城市
export const updateCity = (id: number, data: any) => {
  return api.post<UpdateCityResponse>(`/city/${id}/edit/`, data, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

// 删除城市
export const deleteCity = (id: number) => {
  return api.delete<DeleteCityResponse>(`/city/${id}/delete/`)
}