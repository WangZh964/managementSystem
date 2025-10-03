import api from './index'

// 用户登录
export const login = (data: any) => {
  return api.post('/login/', data)
}

// 用户注册
export const register = (data: any) => {
  return api.post('/register/', data)
}

// 用户注销
export const logout = () => {
  return api.post('/logout/')
}

// 获取验证码
export const getCaptcha = () => {
  return api.get('/image/code/', {
    responseType: 'blob'
  })
}

// 获取用户列表
export const getUserListData = (params: any) => {
  return api.get('/user/list/', { params })
}

// 添加用户
export const addUser = (data: any) => {
  return api.post('/user/add/', data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 编辑用户
export const updateUser = (id: number, data: any) => {
  return api.post(`/user/${id}/edit/`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除用户
export const deleteUser = (id: number) => {
  return api.delete(`/user/${id}/delete/`)
}

// 获取部门列表
export const getDepartmentList = () => {
  return api.get('/depart/list/')
}