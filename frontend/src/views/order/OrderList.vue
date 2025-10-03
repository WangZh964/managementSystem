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
        新建订单
      </el-button>
    </div>

    <!-- 面板 -->
    <el-card class="order-card">
      <template #header>
        <div class="card-header">
          <el-icon><List /></el-icon>
          订单列表
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.oid" placeholder="请输入订单号" clearable />
        </el-form-item>
        <el-form-item label="订单名称">
          <el-input v-model="searchForm.title" placeholder="请输入订单名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待支付" :value="1" />
            <el-option label="已支付" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Table -->
      <el-table :data="orderList" border stripe>
        <el-table-column type="index" label="序号" width="100" align="center" />
        <el-table-column prop="id" label="ID" width="100" align="center" />
        <el-table-column prop="oid" label="订单号" min-width="120" />
        <el-table-column prop="title" label="订单名称" min-width="150" />
        <el-table-column prop="price" label="价格" width="100" align="right">
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'warning' : 'success'">
              {{ scope.row.status === 1 ? '待支付' : '已支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="admin.username" label="管理员" min-width="120" />
        <el-table-column label="创建时间" width="180" align="center">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
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

    <!-- 添加/编辑订单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
      destroy-on-close
    >
      <el-form
        ref="orderFormRef"
        :model="orderForm"
        :rules="orderRules"
        label-width="100px"
      >
        <el-form-item label="订单名称" prop="title">
          <el-input v-model="orderForm.title" placeholder="请输入订单名称" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="orderForm.price" :min="0" :precision="2" :step="0.1" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="orderForm.status">
            <el-radio :label="1">待支付</el-radio>
            <el-radio :label="2">已支付</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="管理员" prop="admin">
          <el-select v-model="orderForm.admin" placeholder="请选择管理员">
            <el-option
              v-for="admin in adminList"
              :key="admin.id"
              :label="admin.username"
              :value="admin.id"
            />
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
import axios from 'axios'
import { useRouter } from 'vue-router'

// 定义订单类型
interface Order {
  id?: number
  oid: string
  title: string
  price: number
  status: number
  admin?: {
    id: number
    username: string
  }
  created_at?: string
}

// 定义管理员类型
interface Admin {
  id: number
  username: string
}

// 路由
const router = useRouter()

// 响应式数据
const orderList = ref<Order[]>([])
const adminList = ref<Admin[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)

// 搜索表单
const searchForm = reactive({
  oid: '',
  title: '',
  status: ''
})

// 表单数据
const orderForm = reactive({
  title: '',
  price: 0,
  status: 1,
  admin: ''
})

// 表单引用
const orderFormRef = ref()

// 表单验证规则
const orderRules = {
  title: [
    { required: true, message: '请输入订单名称', trigger: 'blur' },
    { min: 2, max: 32, message: '订单名称长度在 2 到 32 个字符', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能小于0', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  admin: [
    { required: true, message: '请选择管理员', trigger: 'change' }
  ]
}

// 获取订单列表
const getOrderList = async () => {
  try {
    // 使用Django后端API
    const response = await axios.get('/order/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        oid: searchForm.oid || undefined,
        title: searchForm.title || undefined,
        status: searchForm.status || undefined
      }
    })
    
    // 处理后端返回的数据格式
    if (response.data && response.data.code === 200) {
      orderList.value = response.data.data || []
      total.value = response.data.data.total || 0
    } else {
      ElMessage.error(response.data?.message || '获取订单列表失败')
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败')
  }
}

// 获取管理员列表
const getAdminList = async () => {
  try {
    const response = await axios.get('/user/list/', {
      params: {
        page: 1,
        page_size: 1000,
        is_admin: true
      }
    })
    
    if (response.data && response.data.code === 200) {
      adminList.value = response.data.data.items || []
    } else {
      ElMessage.error(response.data?.message || '获取管理员列表失败')
    }
  } catch (error) {
    console.error('获取管理员列表失败:', error)
    ElMessage.error('获取管理员列表失败')
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
  getOrderList()
}

// 重置搜索
const handleReset = () => {
  searchForm.oid = ''
  searchForm.title = ''
  searchForm.status = ''
  currentPage.value = 1
  getOrderList()
}

// 处理添加订单
const handleAdd = () => {
  dialogTitle.value = '添加订单'
  isEdit.value = false
  currentId.value = null
  orderForm.title = ''
  orderForm.price = 0
  orderForm.status = 1
  orderForm.admin = ''
  dialogVisible.value = true
}

// 处理编辑订单
const handleEdit = (row: Order) => {
  dialogTitle.value = '修改订单'
  isEdit.value = true
  currentId.value = row.id || null
  orderForm.title = row.title
  orderForm.price = row.price
  orderForm.status = row.status
  orderForm.admin = row.admin?.id ? String(row.admin.id) : ''
  dialogVisible.value = true
}

// 处理删除订单
const handleDelete = (row: Order) => {
  ElMessageBox.confirm(`确定要删除订单 "${row.title}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        // 使用Django后端API
        const response = await axios.delete(`/order/delete/?uid=${row.id}`)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('删除成功')
          getOrderList() // 刷新列表
        } else {
          ElMessage.error(response.data?.message || '删除失败')
        }
      } catch (error) {
        console.error('删除订单失败:', error)
        ElMessage.error('删除订单失败')
      }
    })
    .catch(() => {
      // 用户取消删除操作
    })
}

// 提交表单
const submitForm = async () => {
  if (!orderFormRef.value) return
  
  await orderFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        let response
        
        if (isEdit.value && currentId.value) {
          // 编辑订单 - 使用FormData格式
          const formData = new FormData()
          formData.append('uid', currentId.value.toString())
          formData.append('title', orderForm.title)
          formData.append('price', orderForm.price.toString())
          formData.append('status', orderForm.status.toString())
          formData.append('admin', orderForm.admin)
          
          response = await axios.post('/order/edit/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        } else {
          // 添加订单 - 使用FormData格式
          const formData = new FormData()
          formData.append('title', orderForm.title)
          formData.append('price', orderForm.price.toString())
          formData.append('status', orderForm.status.toString())
          formData.append('admin', orderForm.admin)
          
          response = await axios.post('/order/add/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getOrderList() // 刷新列表
        } else {
          // 显示具体错误信息
          const errorMsg = response.data?.message || (isEdit.value ? '修改失败' : '添加失败')
          ElMessage.error(errorMsg)
          
          // 如果有字段错误信息，显示具体字段错误
          if (response.data?.errors) {
            const errors = response.data.data.errors
            for (const field in errors) {
              ElMessage.error(`${field}: ${errors[field]}`)
            }
          }
        }
      } catch (error) {
        console.error(isEdit.value ? '修改订单失败:' : '添加订单失败:', error)
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  orderFormRef.value?.resetFields()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getOrderList()
}

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置为第一页
  getOrderList()
}

// 组件挂载时获取数据
onMounted(() => {
  getOrderList()
  getAdminList()
})

// 返回首页
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './OrderList.css';
</style>