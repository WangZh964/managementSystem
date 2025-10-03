import axios from 'axios';

// 获取管理员列表
export const getAdminList = (params: any) => {
  return axios.get('/api/admin/', { params });
};

// 添加管理员
export const addAdmin = (data: any) => {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);
  formData.append('confirm_password', data.confirmPassword);
  if (data.email) {
    formData.append('email', data.email);
  }
  if (data.is_active !== undefined) {
    formData.append('is_active', data.is_active ? '1' : '0');
  }
  
  return axios.post('/api/admin/add/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

// 编辑管理员
export const editAdmin = (id: number, data: any) => {
  const formData = new FormData();
  formData.append('uid', id.toString());
  formData.append('username', data.username);
  if (data.email) {
    formData.append('email', data.email);
  }
  if (data.is_active !== undefined) {
    formData.append('is_active', data.is_active ? '1' : '0');
  }
  
  return axios.post(`/api/admin/${id}/edit/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

// 更新管理员状态
export const updateAdminStatus = (id: number, data: any) => {
  const formData = new FormData();
  formData.append('uid', id.toString());
  formData.append('is_active', data.is_active ? '1' : '0');
  
  return axios.post(`/api/admin/${id}/edit/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

// 删除管理员
export const deleteAdmin = (id: number) => {
  return axios.get(`/api/admin/delete/?uid=${id}`);
};

// 重置管理员密码
export const resetAdminPassword = (id: number, data: any) => {
  const formData = new FormData();
  formData.append('uid', id.toString());
  formData.append('password', data.password);
  formData.append('confirm_password', data.confirmPassword);
  
  return axios.post(`/api/admin/${id}/reset/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};