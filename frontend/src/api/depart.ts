import api from './index'

// 部门接口类型定义
export interface Department {
  id?: number
  title: string
}

// 部门响应接口
export interface DepartmentResponse {
  code: number
  message: string
  data: Department[]
  total: number
  page_string?: string
}

// 添加部门请求参数
export interface AddDepartmentRequest {
  title: string
}

// 更新部门请求参数
export interface UpdateDepartmentRequest {
  title: string
}

// 获取部门列表
export const getDepartmentList = () => {
  return api.get('/api/depart/list/')
}

// 添加部门
export const addDepartment = (data: AddDepartmentRequest) => {
  return api.post('/api/depart/add/', data)
}

// 更新部门
export const updateDepartment = (id: number, data: UpdateDepartmentRequest) => {
  return api.post(`/api/depart/${id}/edit/`, data)
}

// 删除部门
export const deleteDepartment = (id: number) => {
  return api.post(`/api/depart/${id}/delete/`)
}