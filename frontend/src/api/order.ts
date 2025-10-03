import api from './index'

// 订单接口类型定义
export interface Order {
  id: number
  oid: string
  title: string
  price: number
  status: number
  admin: {
    id: number
    username: string
  } | null
  created_at: string | null
}

export interface AddOrderRequest {
  title: string
  price: number
  status: number
  admin: number
}

export interface UpdateOrderRequest {
  title: string
  price: number
  status: number
  admin: number
}

export interface OrderListResponse {
  code: number
  message: string
  data: Order[]
  total: number
  page_string: string
}

// 获取订单列表
export function getOrderList(params: {
  page?: number
  page_size?: number
  oid?: string
  title?: string
  status?: number
}) {
  return api.get('/order/', { params })
}

// 添加订单
export function addOrder(data: AddOrderRequest) {
  // 使用FormData格式发送数据
  const formData = new FormData()
  Object.keys(data).forEach(key => {
    formData.append(key, data[key as keyof AddOrderRequest].toString())
  })
  
  return api.post('/order/add/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 更新订单
export function updateOrder(id: number, data: UpdateOrderRequest) {
  // 使用FormData格式发送数据
  const formData = new FormData()
  formData.append('uid', id.toString())
  Object.keys(data).forEach(key => {
    formData.append(key, data[key as keyof UpdateOrderRequest].toString())
  })
  
  return api.post('/order/edit/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除订单
export function deleteOrder(id: number) {
  return api.delete(`/order/delete/?uid=${id}`)
}

// 获取订单详情
export function getOrderDetail(id: number) {
  return api.get(`/order/detail/?uid=${id}`)
}