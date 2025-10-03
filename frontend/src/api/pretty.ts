import api from './index'

// 靓号接口
export interface Pretty {
  id?: number;
  mobile: string;
  price: number;
  level: number;
  status: number;
}

// 靓号列表响应接口
export interface PrettyListResponse {
  code: number;
  message: string;
  data: {
    items: Pretty[];
    total: number;
  };
}

// 添加靓号响应接口
export interface AddPrettyResponse {
  code: number;
  message: string;
  data: Pretty;
}

// 更新靓号响应接口
export interface UpdatePrettyResponse {
  code: number;
  message: string;
  data: Pretty;
}

// 删除靓号响应接口
export interface DeletePrettyResponse {
  code: number;
  message: string;
  data: any;
}

// 获取靓号列表
export const getPrettyList = (params: { mobile?: string; page?: number; size?: number }) => {
  return api.get<PrettyListResponse>('/pretty/', { params })
}

// 新建靓号
export const createPretty = (data: FormData) => {
  return api.post<AddPrettyResponse>('/pretty/add/', data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 编辑靓号
export const updatePretty = (id: number, data: FormData) => {
  return api.post<UpdatePrettyResponse>(`/pretty/${id}/edit/`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除靓号
export const deletePretty = (id: number) => {
  return api.delete<DeletePrettyResponse>(`/pretty/${id}/delete/`)
}