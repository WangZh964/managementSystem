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
        <span>用户管理</span>
      </div>
      <div class="panel-actions">
        <el-button class="home-button" @click="goToHome">
          <el-icon><HomeFilled /></el-icon>
          点击返回首页
        </el-button>
        <el-button type="success" class="add-button" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新建用户
        </el-button>
      </div>
    </div>

    <!-- 面板 -->
    <el-card class="user-card">
      <template #header>
        <div class="card-header">
          <el-icon><List /></el-icon>
          用户列表
        </div>
      </template>

      <!-- Table -->
      <el-table :data="userList" border stripe>
        <el-table-column type="index" label="序号" width="80" align="center" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="姓名" min-width="100" />
        <el-table-column prop="password" label="密码" min-width="100" />
        <el-table-column prop="age" label="年龄" width="80" align="center" />
        <el-table-column prop="account" label="余额" width="100" align="right" />
        <el-table-column label="入职时间" width="120" align="center">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="性别" width="80" align="center">
          <template #default="scope">
            {{ getGenderDisplay(scope.row.gender) }}
          </template>
        </el-table-column>
        <el-table-column prop="depart_title" label="所属部门" min-width="120" />
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

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
      destroy-on-close
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="userForm.age" :min="1" :max="120" />
        </el-form-item>
        <el-form-item label="余额" prop="account">
          <el-input-number v-model="userForm.account" :precision="2" :step="100" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="userForm.gender">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="2">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="所属部门" prop="depart_id">
          <el-select v-model="userForm.depart_id" placeholder="请选择部门">
            <el-option
              v-for="dept in departmentList"
              :key="dept.id"
              :label="dept.title"
              :value="dept.id"
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
import { Plus, List, HomeFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getUserListData, addUser, updateUser, deleteUser, getDepartmentList } from '@/api/user'

// 定义用户类型
interface User {
  id?: number
  name: string
  password: string
  age: number
  account: number
  gender: number
  depart_id?: number
  depart_title?: string
  create_time?: string
}

// 初始化路由
const router = useRouter()

// 定义部门类型
interface Department {
  id: number
  title: string
}

// 响应式数据
const userList = ref<User[]>([])
const departmentList = ref<Department[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)

// 表单数据
const userForm = reactive<User>({
  name: '',
  password: '',
  age: 18,
  account: 0,
  gender: 1,
  depart_id: undefined
})

// 表单引用
const userFormRef = ref()

// 表单验证规则
const userRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 32, message: '长度在 2 到 32 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '长度在 6 到 32 个字符', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' },
    { type: 'number', min: 1, max: 120, message: '年龄必须在1到120之间', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  depart_id: [
    { required: true, message: '请选择所属部门', trigger: 'change' }
  ]
}

// 获取用户列表
const getUserList = async () => {
  try {
    // 使用API函数
    const response = await getUserListData({
      page: currentPage.value,
      size: pageSize.value
    })
    
    // 处理后端返回的数据格式
    if (response.data && response.data.code === 200) {
      userList.value = response.data.data?.items || []
      total.value = response.data.data?.total || 0
    } else {
      ElMessage.error(response.data.data?.message || '获取用户列表失败')
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  }
}

// 获取部门列表
const getDepartmentListData = async () => {
  try {
    const response = await getDepartmentList()
    
    if (response.data && response.data.code === 200) {
      departmentList.value = response.data.data || []
    } else {
      ElMessage.error(response.data.data?.message || '获取部门列表失败')
    }
  } catch (error) {
    console.error('获取部门列表失败:', error)
    ElMessage.error('获取部门列表失败')
  }
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toISOString().split('T')[0]
}

// 获取性别显示
const getGenderDisplay = (gender?: number) => {
  const genderMap = {
    1: '男',
    2: '女'
  }
  return gender ? genderMap[gender as 1 | 2] || gender : gender
}

// 处理添加用户
const handleAdd = () => {
  dialogTitle.value = '添加用户'
  isEdit.value = false
  currentId.value = null
  userForm.name = ''
  userForm.password = ''
  userForm.age = 18
  userForm.account = 0
  userForm.gender = 1
  userForm.depart_id = undefined
  dialogVisible.value = true
}

// 处理编辑用户
const handleEdit = (row: User) => {
  dialogTitle.value = '修改用户'
  isEdit.value = true
  currentId.value = row.id || null
  userForm.name = row.name
  userForm.password = row.password
  userForm.age = row.age
  userForm.account = row.account
  userForm.gender = row.gender
  userForm.depart_id = row.depart_id
  dialogVisible.value = true
}

// 处理删除用户
const handleDelete = (row: User) => {
  ElMessageBox.confirm(`确定要删除用户 "${row.name}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        // 使用API函数
        const response = await deleteUser(row.id!)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('删除成功')
          getUserList() // 刷新列表
        } else {
          ElMessage.error(response.data.data?.message || '删除失败')
        }
      } catch (error) {
        console.error('删除用户失败:', error)
        ElMessage.error('删除用户失败')
      }
    })
    .catch(() => {
      // 用户取消删除操作
    })
}

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return
  
  await userFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 创建FormData对象
        const formData = new FormData()
        formData.append('name', userForm.name)
        formData.append('password', userForm.password)
        formData.append('age', userForm.age.toString())
        formData.append('account', userForm.account.toString())
        formData.append('gender', userForm.gender.toString())
        if (userForm.depart_id !== undefined) {
          formData.append('depart_id', userForm.depart_id.toString())
        }
        
        let response
        
        if (isEdit.value && currentId.value) {
          // 编辑用户
          response = await updateUser(currentId.value, formData)
        } else {
          // 添加用户
          response = await addUser(formData)
        }
        
        console.log('编辑用户完整响应对象:', response)
        console.log('响应状态码:', response.status)
        console.log('响应数据结构:', response.data)
        console.log('响应code值:', response.data?.code)
        console.log('响应message值:', response.data?.message)
        console.log('详细错误信息:', response.data?.data?.errors)
        
        if (response.status === 200 && response.data) {
          // 检查业务状态码
          if (response.data.code === 200) {
            ElMessage.success(isEdit.value ? '编辑成功' : '添加成功')
            dialogVisible.value = false
            getUserList() // 刷新列表
          } else {
            // 如果HTTP状态码是200但业务code不是200，显示后端返回的错误消息
            ElMessage.error(response.data.message || (isEdit.value ? '编辑失败' : '添加失败'))
          }
        } else {
          // HTTP状态码不是200的情况
          ElMessage.error(response.data?.message || (isEdit.value ? '编辑失败' : '添加失败'))
        }
      } catch (error) {
        console.error(isEdit.value ? '修改用户失败:' : '添加用户失败:', error)
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  userFormRef.value?.resetFields()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getUserList()
}

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置为第一页
  getUserList()
}

// 组件挂载时获取数据
onMounted(() => {
  getUserList()
  getDepartmentListData()
})

// 返回首页方法
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './UserList.css';
</style>