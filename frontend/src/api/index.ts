import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/', // 使用相对路径，通过Vite代理转发
  timeout: 10000,
  withCredentials: true // 允许携带cookie
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

export default api