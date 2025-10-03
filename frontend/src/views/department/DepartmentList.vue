<template>
  <div class="container">
    <!-- 浮动形状装饰 -->
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    
    <!-- 返回首页按钮 -->
    <div class="back-to-home">
      <el-button type="primary" @click="goToHome" class="home-button">
        <el-icon><HomeFilled /></el-icon>
        点击返回首页
      </el-button>
    </div>
    
    <!-- 新建按钮 -->
    <div class="add-button">
      <el-button type="success" @click="handleAdd" class="add-btn">
        <el-icon><Plus /></el-icon>
        新建部门
      </el-button>
    </div>

    <!-- 面板 -->
    <el-card class="department-card">
      <template #header>
        <div class="card-header">
          <el-icon><List /></el-icon>
          部门列表
        </div>
      </template>

      <!-- Table -->
      <el-table :data="departmentList" border stripe>
        <el-table-column type="index" label="序号" width="100" align="center" />
        <el-table-column prop="id" label="ID" width="100" align="center" />
        <el-table-column prop="title" label="名称" min-width="200" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        background
      />
    </div>

    <!-- 添加/编辑部门对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
      destroy-on-close
    >
      <el-form
        ref="departmentFormRef"
        :model="departmentForm"
        :rules="departmentRules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="title">
          <el-input v-model="departmentForm.title" placeholder="请输入部门名称" />
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
import { Plus, List, HomeFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

// 定义部门类型
interface Department {
  id?: number
  title: string
}

// 路由
const router = useRouter()

// 响应式数据
const departmentList = ref<Department[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)

// 表单数据
const departmentForm = reactive<Department>({
  title: ''
})

// 表单引用
const departmentFormRef = ref()

// 表单验证规则
const departmentRules = {
  title: [
    { required: true, message: '请输入部门名称', trigger: 'blur' },
    { min: 2, max: 32, message: '长度在 2 到 32 个字符', trigger: 'blur' }
  ]
}

// 获取部门列表
const getDepartmentList = async () => {
  try {
    // 使用Django后端API
    const response = await axios.get('/api/depart/list/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    
    // 处理后端返回的数据格式
    if (response.data && response.data.code === 200) {
      departmentList.value = response.data.data || []
      total.value = response.data.data.total || 0
    } else {
      // 提供更详细的错误信息
      const errorMessage = response.data?.message || '获取部门列表失败'
      console.error('API返回错误:', errorMessage)
      ElMessage.error(errorMessage)
    }
  } catch (error) {
    // 提供更详细的错误信息
    let errorMessage = '获取部门列表失败'
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // 服务器返回了错误状态码
        errorMessage = `服务器错误: ${error.response.status} - ${error.response.data?.message || '未知错误'}`
      } else if (error.request) {
        // 请求已发出但没有收到响应
        errorMessage = '网络错误: 无法连接到服务器'
      } else {
        // 请求设置出错
        errorMessage = `请求错误: ${error.message}`
      }
    } else {
      errorMessage = `未知错误: ${error instanceof Error ? error.message : String(error)}`
    }
    
    console.error('获取部门列表失败:', error)
    ElMessage.error(errorMessage)
  }
}

// 处理添加部门
const handleAdd = () => {
  dialogTitle.value = '添加部门'
  isEdit.value = false
  currentId.value = null
  departmentForm.title = ''
  dialogVisible.value = true
}

// 处理编辑部门
const handleEdit = (row: Department) => {
  dialogTitle.value = '修改部门'
  isEdit.value = true
  currentId.value = row.id || null
  departmentForm.title = row.title
  dialogVisible.value = true
}

// 处理删除部门
const handleDelete = (row: Department) => {
  ElMessageBox.confirm(`确定要删除部门 "${row.title}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        // 使用Django后端API
        const response = await axios.post(`/api/depart/${row.id}/delete/`)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('删除成功')
          getDepartmentList() // 刷新列表
        } else {
          ElMessage.error(response.data?.message || '删除失败')
        }
      } catch (error) {
        console.error('删除部门失败:', error)
        ElMessage.error('删除部门失败')
      }
    })
    .catch(() => {
      // 用户取消删除操作
    })
}

// 提交表单
const submitForm = async () => {
  if (!departmentFormRef.value) return
  
  await departmentFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        let response
        
        if (isEdit.value && currentId.value) {
          // 编辑部门 - 使用表单数据格式
          const formData = new FormData()
          formData.append('title', departmentForm.title)
          response = await axios.post(`/api/depart/${currentId.value}/edit/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        } else {
          // 添加部门 - 使用表单数据格式
          const formData = new FormData()
          formData.append('title', departmentForm.title)
          response = await axios.post('/api/depart/add/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getDepartmentList() // 刷新列表
        } else {
          // 显示更详细的错误信息
          const errorMessage = response.data?.message || (isEdit.value ? '修改失败' : '添加失败')
          if (response.data?.errors) {
            // 如果有字段错误信息，显示具体错误
            const errorDetails = Object.values(response.data.data.errors).join(', ')
            ElMessage.error(`${errorMessage}: ${errorDetails}`)
          } else {
            ElMessage.error(errorMessage)
          }
        }
      } catch (error) {
        console.error(isEdit.value ? '修改部门失败:' : '添加部门失败:', error)
        if (axios.isAxiosError(error) && error.response?.data?.data?.errors) {
          // 显示表单验证错误
          const errorDetails = Object.values(error.response.data.data.errors).join(', ')
          ElMessage.error(`表单验证失败: ${errorDetails}`)
        } else {
          ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
        }
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  departmentFormRef.value?.resetFields()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getDepartmentList()
}

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置为第一页
  getDepartmentList()
}

// 组件挂载时获取数据
onMounted(() => {
  getDepartmentList()
})

// 返回首页
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './DepartmentList.css';
</style>