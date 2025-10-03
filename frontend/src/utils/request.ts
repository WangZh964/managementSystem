import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:8000', // 后端API的基础URL
  timeout: 5000, // 请求超时时间
  withCredentials: true // 允许携带cookie，用于session认证
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 移除token认证，使用Django的session认证
    // axios会自动处理session cookie，不需要手动添加认证头
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 返回响应数据，而不是整个响应对象
    return response.data
  },
  error => {
    // 对响应错误做点什么
    if (error.response) {
      const { status } = error.response
      
      if (status === 401) {
        // 未授权，清除用户信息并跳转到登录页
        localStorage.removeItem('userInfo')
        ElMessage.error('登录已过期，请重新登录')
        router.push('/login')
      } else if (status === 403) {
        ElMessage.error('权限不足')
      } else if (status === 404) {
        ElMessage.error('请求的资源不存在')
      } else if (status === 500) {
        ElMessage.error('服务器内部错误')
      } else {
        ElMessage.error('网络错误，请稍后重试')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default service