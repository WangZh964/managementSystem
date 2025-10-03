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
        <span>管理员账户管理</span>
      </div>
      <div class="panel-actions">
        <el-button class="home-button" @click="goToHome">
          <el-icon><HomeFilled /></el-icon>
          点击返回首页
        </el-button>
        <el-button type="primary" class="add-button" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加管理员
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.is_active" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
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
      <el-table
        v-loading="loading"
        :data="adminList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              :active-value="true"
              :inactive-value="false"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180" align="center">
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

    <!-- 添加/编辑管理员对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        ref="adminFormRef"
        :model="adminForm"
        :rules="adminRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="adminForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="adminForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="adminForm.confirmPassword" type="password" placeholder="请确认密码" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="adminForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch
            v-model="adminForm.is_active"
            :active-value="true"
            :inactive-value="false"
          />
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
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, List, HomeFilled } from '@element-plus/icons-vue'
import { getAdminList, addAdmin, editAdmin, deleteAdmin, updateAdminStatus } from '@/api/admin'
import { useRouter } from 'vue-router'

// 定义接口
interface Admin {
  id?: number
  username: string
  email: string
  is_active: boolean
  created_at?: string
}

// 初始化路由
const router = useRouter()

// 响应式数据
const loading = ref(false)
const dialogVisible = ref(false)
const currentId = ref<number | null>(null)
const adminFormRef = ref()
const adminList = ref<Admin[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单
const searchForm = reactive({
  username: '',
  is_active: ''
})

// 表单数据
const adminForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  is_active: true
})

// 计算属性
const dialogTitle = computed(() => currentId.value ? '修改管理员' : '添加管理员')

// 表单验证规则
const adminRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 32, message: '用户名长度在 3 到 32 个字符', trigger: 'blur' }
  ],
  password: [
    { required: !currentId.value, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度在 6 到 32 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { 
      required: !currentId.value, 
      message: '请确认密码', 
      trigger: 'blur' 
    },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== adminForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  is_active: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 获取管理员列表
const getAdminListData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      q: searchForm.username || undefined,
      is_active: searchForm.is_active !== '' ? searchForm.is_active : undefined
    }
    const response = await getAdminList(params)
    
    if (response.data && response.data.code === 200) {
      adminList.value = response.data.data.items
      total.value = response.data.data.total
    } else {
      ElMessage.error(response.data.message || response.data.msg || '获取管理员列表失败')
    }
  } catch (error) {
    console.error('获取管理员列表失败:', error)
    ElMessage.error('获取管理员列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  getAdminListData()
}

// 重置搜索
const handleReset = () => {
  searchForm.username = ''
  searchForm.is_active = ''
  currentPage.value = 1
  getAdminListData()
}

// 添加管理员
const handleAdd = () => {
  currentId.value = null
  adminForm.username = ''
  adminForm.password = ''
  adminForm.confirmPassword = ''
  adminForm.email = ''
  adminForm.is_active = true
  dialogVisible.value = true
}

// 编辑管理员
const handleEdit = (row: Admin) => {
  currentId.value = row.id || null
  adminForm.username = row.username
  adminForm.password = ''
  adminForm.confirmPassword = ''
  adminForm.email = row.email
  adminForm.is_active = row.is_active
  dialogVisible.value = true
}

// 删除管理员
const handleDelete = (row: Admin) => {
  ElMessageBox.confirm(
    `确定要删除管理员"${row.username}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await deleteAdmin(row.id!)
      
      if (response.data && response.data.code === 200) {
        ElMessage.success('删除成功')
        getAdminListData()
      } else {
        ElMessage.error(response.data.message || response.data.msg || '删除失败')
      }
    } catch (error) {
      console.error('删除管理员失败:', error)
      ElMessage.error('删除失败，请稍后重试')
    }
  }).catch(() => {
    // 用户取消删除操作
  })
}

// 处理状态变更
const handleStatusChange = async (row: Admin) => {
  try {
    const response = await updateAdminStatus(row.id!, {
      is_active: row.is_active 
    })
    
    if (response.data && response.data.code === 200) {
      ElMessage.success('状态更新成功')
    } else {
      // 恢复开关状态
      row.is_active = !row.is_active
      ElMessage.error(response.data.message || response.data.msg || '状态更新失败')
    }
  } catch (error) {
    // 恢复开关状态
    row.is_active = !row.is_active
    console.error('状态更新失败:', error)
    ElMessage.error('状态更新失败，请稍后重试')
  }
}

// 提交表单
const submitForm = async () => {
  if (!adminFormRef.value) return
  
  await adminFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        let response
        
        if (currentId.value) {
          // 编辑管理员
          const updateData = {
            username: adminForm.username,
            email: adminForm.email,
            is_active: adminForm.is_active
          }
          
          // 如果输入了密码，则更新密码
          if (adminForm.password) {
            Object.assign(updateData, { 
              password: adminForm.password,
              confirmPassword: adminForm.password
            })
          }
          
          response = await editAdmin(currentId.value, updateData)
        } else {
          // 添加管理员
          const addData = {
            username: adminForm.username,
            password: adminForm.password,
            confirmPassword: adminForm.confirmPassword,
            email: adminForm.email,
            is_active: adminForm.is_active
          }
          response = await addAdmin(addData)
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(currentId.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getAdminListData()
        } else {
          // 显示具体错误信息
          if (response.data.data?.errors) {
            const errors = response.data.data.errors
            for (const field in errors) {
              ElMessage.error(`${field}: ${errors[field]}`)
            }
          } else {
            ElMessage.error(response.data.message || response.data.msg || '操作失败')
          }
        }
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error('操作失败，请稍后重试')
      }
    }
  })
}

// 对话框关闭
const handleDialogClose = () => {
  if (adminFormRef.value) {
    adminFormRef.value.resetFields()
  }
}

// 分页处理
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getAdminListData()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  getAdminListData()
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString()
}

// 页面加载时获取数据
onMounted(() => {
  getAdminListData()
})

// 返回首页方法
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './AdminList.css';
</style>