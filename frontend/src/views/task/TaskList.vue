<template>
  <div class="container">
    <!-- 浮动形状装饰 -->
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    
    <!-- 面板头部 -->
    <div class="panel-header">
      <div class="panel-title">
        <el-icon><List /></el-icon>
        <span>任务管理</span>
      </div>
      <div class="panel-actions">
        <el-button class="home-button" @click="goToHome">
          <el-icon><HomeFilled /></el-icon>
          点击返回首页
        </el-button>
        <el-button type="primary" class="add-button" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加任务
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="任务名称">
          <el-input v-model="searchForm.name" placeholder="请输入任务名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表格区域 -->
    <el-card class="table-card">
      <el-table :data="taskList" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="title" label="任务名称" min-width="120" />
        <el-table-column prop="detail" label="任务描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="level" label="级别" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)">
              {{ getLevelText(row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status || 1)">
              {{ getStatusText(row.status || 1) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_name" label="负责人" width="120" align="center" />
        <el-table-column prop="created_at" label="创建时间" width="180" align="center">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">修改</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :background="true"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="taskFormRef"
        :model="taskForm"
        :rules="taskRules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="taskForm.level" placeholder="请选择级别" style="width: 100%">
            <el-option label="紧急" :value="1" />
            <el-option label="重要" :value="2" />
            <el-option label="临时" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, List, Search, Refresh, HomeFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getTaskList, addTask, updateTask, deleteTask } from '@/api/task'

// 定义任务类型
interface Task {
  id?: number
  title: string
  detail: string
  level: number
  user_id?: number
  user_name?: string
}

// 初始化路由
const router = useRouter()

// 响应式数据
const taskList = ref<Task[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)

// 搜索表单
const searchForm = reactive({
  name: ''
})

// 表单数据
const taskForm = reactive({
  name: '',
  description: '',
  level: 1
})

// 表单引用
const taskFormRef = ref()

// 表单验证规则
const taskRules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '任务名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' },
    { min: 5, max: 500, message: '任务描述长度在 5 到 500 个字符', trigger: 'blur' }
  ]
}

// 获取任务列表
const getTaskListData = async () => {
  try {
    // 使用API函数
    const response = await getTaskList({
      page: currentPage.value,
      size: pageSize.value
    })
    
    // 处理后端返回的数据格式
    if (response.data && response.data.code === 200) {
      taskList.value = response.data.data.items || []
      total.value = response.data.data.total || 0
    } else {
      ElMessage.error(response.data.message || '获取任务列表失败')
    }
  } catch (error) {
    console.error('获取任务列表失败:', error)
    ElMessage.error('获取任务列表失败')
  }
}

// 获取级别类型
const getLevelType = (level: number) => {
  switch (level) {
    case 1:
      return 'danger'
    case 2:
      return 'warning'
    case 3:
      return 'info'
    default:
      return ''
  }
}

// 获取级别文本
const getLevelText = (level: number) => {
  switch (level) {
    case 1:
      return '紧急'
    case 2:
      return '重要'
    case 3:
      return '临时'
    default:
      return '未知'
  }
}

// 获取状态类型
const getStatusType = (status: number) => {
  switch (status) {
    case 1:
      return 'info'
    case 2:
      return 'warning'
    case 3:
      return 'success'
    default:
      return ''
  }
}

// 获取状态文本
const getStatusText = (status: number) => {
  switch (status) {
    case 1:
      return '未开始'
    case 2:
      return '进行中'
    case 3:
      return '已完成'
    default:
      return '未知'
  }
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1 // 重置为第一页
  getTaskListData()
}

// 重置搜索
const handleReset = () => {
  searchForm.name = ''
  currentPage.value = 1
  getTaskListData()
}

// 处理添加任务
const handleAdd = () => {
  dialogTitle.value = '添加任务'
  isEdit.value = false
  currentId.value = null
  taskForm.name = ''
  taskForm.description = ''
  taskForm.level = 1
  dialogVisible.value = true
}

// 处理编辑任务
const handleEdit = (row: Task) => {
  dialogTitle.value = '修改任务'
  isEdit.value = true
  currentId.value = row.id || null
  taskForm.name = row.title
  taskForm.description = row.detail
  taskForm.level = row.level
  dialogVisible.value = true
}

// 处理删除任务
const handleDelete = (row: Task) => {
  ElMessageBox.confirm(`确定要删除任务 "${row.title}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        // 使用API函数
        const response = await deleteTask(row.id!)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('删除成功')
          getTaskListData() // 刷新列表
        } else {
          ElMessage.error(response.data.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除任务失败:', error)
        ElMessage.error('删除任务失败')
      }
    })
    .catch(() => {
      // 用户取消删除操作
    })
}

// 提交表单
const submitForm = async () => {
  if (!taskFormRef.value) return
  
  await taskFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 创建FormData对象
        const formData = new FormData()
        formData.append('title', taskForm.name)
        formData.append('detail', taskForm.description)
        formData.append('level', taskForm.level.toString())
        
        let response
        
        if (isEdit.value && currentId.value) {
          // 编辑任务
          response = await updateTask(currentId.value, formData)
        } else {
          // 添加任务
          response = await addTask(formData)
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getTaskListData() // 刷新列表
        } else {
          // 如果有表单验证错误信息，显示具体的错误
          if (response.data && response.data.data && (response.data.data as any).errors) {
            const errors = (response.data.data as any).errors
            const errorMessage = Object.values(errors).flat().join('; ')
            ElMessage.error(errorMessage || (isEdit.value ? '修改失败' : '添加失败'))
          } else {
            ElMessage.error(response.data?.message || (isEdit.value ? '修改失败' : '添加失败'))
          }
        }
      } catch (error) {
        console.error(isEdit.value ? '修改任务失败:' : '添加任务失败:', error)
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  taskFormRef.value?.resetFields()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getTaskListData()
}

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置为第一页
  getTaskListData()
}

// 组件挂载时获取数据
onMounted(() => {
  getTaskListData()
})

// 返回首页方法
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './TaskList.css';
</style>