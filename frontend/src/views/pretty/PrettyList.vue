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
        <span>靓号管理</span>
      </div>
      <div class="panel-actions">
        <el-button class="home-button" @click="goToHome">
          <el-icon><HomeFilled /></el-icon>
          点击返回首页
        </el-button>
        <el-button type="success" class="add-button" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新建靓号
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="手机号">
          <el-input v-model="searchForm.mobile" placeholder="请输入手机号" clearable />
        </el-form-item>
        <el-form-item label="级别">
          <el-input v-model="searchForm.level" placeholder="请输入级别" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            查找
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
      <el-table :data="prettyList" border style="width: 100%">
        <el-table-column type="index" label="序号" width="80" align="center" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="mobile" label="号码" min-width="120" />
        <el-table-column prop="price" label="价格" width="100" align="right">
          <template #default="{ row }">
            ¥{{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="级别" width="100" align="center">
          <template #default="{ row }">
            {{ getLevelDisplay(row.level) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ getStatusDisplay(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
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
          :page-sizes="[10, 20, 30, 50]"
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
        ref="prettyFormRef"
        :model="prettyForm"
        :rules="prettyRules"
        label-width="100px"
      >
        <el-form-item label="号码" prop="mobile">
          <el-input v-model="prettyForm.mobile" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number
            v-model="prettyForm.price"
            :min="0"
            :precision="2"
            :step="100"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="prettyForm.level" placeholder="请选择级别">
            <el-option label="一级" :value="1" />
            <el-option label="二级" :value="2" />
            <el-option label="三级" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="prettyForm.status">
            <el-radio :label="1">已占用</el-radio>
            <el-radio :label="2">未占用</el-radio>
          </el-radio-group>
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
import { Plus, List, Search, HomeFilled, Refresh } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getPrettyList, createPretty, updatePretty, deletePretty } from '@/api/pretty'

// 定义靓号类型
interface Pretty {
  id?: number
  mobile: string
  price: number
  level: number
  status: number
  created_at?: string
}

// 初始化路由
const router = useRouter()

// 响应式数据
const prettyList = ref<Pretty[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref<number | null>(null)

// 搜索表单
const searchForm = reactive({
  mobile: '',
  level: ''
})

// 表单数据
const prettyForm = reactive({
  mobile: '',
  price: 0,
  level: 1,
  status: 1
})

// 表单引用
const prettyFormRef = ref()

// 表单验证规则
const prettyRules = {
  mobile: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能小于0', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择级别', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 级别字母到数字的映射
const levelMap = {
  'A': 1,
  'B': 2,
  'C': 3,
  'D': 4,
  '1': 1,
  '2': 2,
  '3': 3,
  '4': 4
}

// 获取靓号列表数据
const getPrettyListData = async () => {
  try {
    let levelValue = undefined
    
    if (searchForm.level && searchForm.level.trim() !== '') {
      const levelInput = searchForm.level.trim().toUpperCase()
      // 先尝试字母映射
      if (levelMap[levelInput as keyof typeof levelMap] !== undefined) {
        levelValue = levelMap[levelInput as keyof typeof levelMap]
      } else {
        // 如果字母映射失败，尝试解析数字
        const parsedLevel = parseInt(levelInput)
        if (!isNaN(parsedLevel) && parsedLevel >= 1 && parsedLevel <= 4) {
          levelValue = parsedLevel
        }
      }
    }
    
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      mobile: searchForm.mobile || undefined,
      level: levelValue
    }
    
    const response = await getPrettyList(params)
    
    if (response.data && response.data.code === 200) {
      prettyList.value = response.data.data.items || []
      total.value = response.data.data.total || 0
    } else {
      ElMessage.error(response.data.message || '获取靓号列表失败')
    }
  } catch (error) {
    console.error('获取靓号列表失败:', error)
    ElMessage.error('获取靓号列表失败')
  }
}

// 获取级别显示文本
const getLevelDisplay = (level: number) => {
  const levels = ['', 'A', 'B', 'C', 'D', 'E']
  return levels[level] || '未知'
}

// 获取状态显示文本
const getStatusDisplay = (status: number) => {
  return status === 1 ? '启用' : '禁用'
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
  getPrettyListData()
}

// 重置搜索
const handleReset = () => {
  searchForm.mobile = ''
  searchForm.level = ''
  currentPage.value = 1
  getPrettyListData()
}

// 处理添加靓号
const handleAdd = () => {
  dialogTitle.value = '添加靓号'
  isEdit.value = false
  currentId.value = null
  prettyForm.mobile = ''
  prettyForm.price = 0
  prettyForm.level = 1
  prettyForm.status = 2
  dialogVisible.value = true
}

// 处理编辑靓号
const handleEdit = (row: Pretty) => {
  dialogTitle.value = '修改靓号'
  isEdit.value = true
  currentId.value = row.id || null
  prettyForm.mobile = row.mobile
  prettyForm.price = row.price
  prettyForm.level = row.level
  prettyForm.status = row.status
  dialogVisible.value = true
}

// 处理删除靓号
const handleDelete = (row: Pretty) => {
  ElMessageBox.confirm(`确定要删除靓号 "${row.mobile}" 吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        const response = await deletePretty(row.id!)
        
        if (response.data && response.data.code === 200) {
          ElMessage.success('删除成功')
          getPrettyListData() // 刷新列表
        } else {
          ElMessage.error(response.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除靓号失败:', error)
        ElMessage.error('删除靓号失败')
      }
    })
    .catch(() => {
      // 用户取消删除操作
    })
}

// 提交表单
const submitForm = async () => {
  if (!prettyFormRef.value) return
  
  await prettyFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 创建FormData对象
        const formData = new FormData()
        formData.append('mobile', prettyForm.mobile)
        formData.append('price', prettyForm.price.toString())
        formData.append('level', prettyForm.level.toString())
        formData.append('status', prettyForm.status.toString())
        
        let response
        
        if (isEdit.value && currentId.value) {
          // 编辑靓号
          response = await updatePretty(currentId.value, formData)
        } else {
          // 添加靓号
          response = await createPretty(formData)
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getPrettyListData() // 刷新列表
        } else {
          ElMessage.error(response.data.message || (isEdit.value ? '修改失败' : '添加失败'))
        }
      } catch (error) {
        console.error(isEdit.value ? '修改靓号失败:' : '添加靓号失败:', error)
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  prettyFormRef.value?.resetFields()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  getPrettyListData()
}

// 处理每页条数变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置为第一页
  getPrettyListData()
}

// 组件挂载时获取数据
onMounted(() => {
  getPrettyListData()
})

// 返回首页方法
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './PrettyList.css';
</style>