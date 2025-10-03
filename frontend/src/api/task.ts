import api from './index'

// 任务接口类型定义
export interface Task {
  id?: number
  title: string
  detail: string
  level: number
  user_id: number
  user_name?: string
  created_at?: string
}

// 任务列表响应接口
export interface TaskListResponse {
  items: never[]
  total: number
  code: number
  message: string
  data: {
    items: Task[];
    total: number;
    page: number;
    size: number;
    total_pages: number;
  };
}

// 添加任务响应接口
export interface AddTaskResponse {
  code: number;
  message: string;
  data: Task;
}

// 更新任务响应接口
export interface UpdateTaskResponse {
  code: number;
  message: string;
  data: Task;
}

// 删除任务响应接口
export interface DeleteTaskResponse {
  code: number;
  message: string;
  data: any;
}

// 任务详情响应接口
export interface TaskDetailResponse {
  code: number;
  message: string;
  data: Task;
}

// 获取任务列表
export const getTaskList = (params: {
  page?: number;
  size?: number;
  level?: number;
}) => {
  return api.get<TaskListResponse>('/task/list/', { params })
}

// 添加任务
export const addTask = (data: FormData) => {
  return api.post<AddTaskResponse>('/task/add/', data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 更新任务
export const updateTask = (id: number, data: FormData) => {
  return api.post<UpdateTaskResponse>(`/task/${id}/edit/`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除任务
export const deleteTask = (id: number) => {
  return api.delete<DeleteTaskResponse>(`/task/${id}/delete/`)
}

// 获取任务详情
export const getTaskDetail = (id: number) => {
  return api.get<TaskDetailResponse>(`/task/${id}/detail/`)
}