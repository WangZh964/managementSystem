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
    
    <!-- 面板头部 -->
    <div class="panel-header">
      <div class="panel-title">
        <el-icon><List /></el-icon>
        <span>城市管理</span>
      </div>
      <div class="panel-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加城市
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="城市名称">
          <el-input v-model="searchForm.name" placeholder="请输入城市名称" clearable />
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
      <el-table :data="cityList" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column label="Logo" width="120" align="center">
          <template #default="scope">
            <el-image 
              :src="scope.row.img" 
              :preview-src-list="[scope.row.img]"
              fit="cover"
              style="width: 80px; height: 80px"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="120" />
        <el-table-column prop="count" label="人口" width="120" align="center" />
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
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
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        ref="cityFormRef"
        :model="cityForm"
        :rules="cityRules"
        label-width="100px"
        enctype="multipart/form-data"
      >
        <el-form-item label="城市名称" prop="name">
          <el-input v-model="cityForm.name" placeholder="请输入城市名称" />
        </el-form-item>
        <el-form-item label="人口数量" prop="count">
          <el-input-number v-model="cityForm.count" :min="0" placeholder="请输入人口数量" />
        </el-form-item>
        <el-form-item label="城市Logo" prop="img">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :http-request="handleUpload"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="cityForm.img" :src="cityForm.img" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
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
import { Plus, List, Picture, Search, Refresh, HomeFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getCityList, addCity, updateCity, deleteCity } from '@/api/city'
import axios from 'axios'

// 定义接口
interface City {
  id?: number
  name: string
  count: number
  img: string
  created_at?: string
}

// 路由
const router = useRouter()

// 响应式数据
const cityList = ref<City[]>([])
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
const cityForm = reactive<City>({
  name: '',
  count: 0,
  img: ''
})

// 表单引用
const cityFormRef = ref()

// 表单验证规则
const cityRules = {
  name: [
    { required: true, message: '请输入城市名称', trigger: 'blur' },
    { min: 2, max: 32, message: '长度在 2 到 32 个字符', trigger: 'blur' }
  ],
  count: [
    { required: true, message: '请输入人口数量', trigger: 'blur' },
    { type: 'number', min: 0, message: '人口数量不能小于0', trigger: 'blur' }
  ],
  img: [
    { required: true, message: '请上传城市Logo', trigger: 'change' }
  ]
}

// 获取城市列表
const getCityListData = async () => {
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      name: searchForm.name || undefined
    }
    const response = await getCityList(params)
    if (response.data && response.data.code === 200) {
      cityList.value = response.data.data.items
      total.value = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取城市列表失败')
    }
  } catch (error) {
    ElMessage.error('获取城市列表失败')
    console.error('获取城市列表失败:', error)
  }
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  getCityListData()
}

// 处理重置
const handleReset = () => {
  searchForm.name = ''
  currentPage.value = 1
  getCityListData()
}

// 处理添加
const handleAdd = () => {
  dialogTitle.value = '添加城市'
  isEdit.value = false
  dialogVisible.value = true
}

// 处理编辑
const handleEdit = (row: City) => {
  dialogTitle.value = '修改城市'
  isEdit.value = true
  currentId.value = row.id || null
  Object.assign(cityForm, row)
  dialogVisible.value = true
}

// 处理删除
const handleDelete = (row: City) => {
  ElMessageBox.confirm(
    `确定要删除城市 "${row.name}" 吗?`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await deleteCity(row.id!)
      if (response.data && response.data.code === 200) {
        ElMessage.success('删除成功')
        getCityListData()
      } else {
        ElMessage.error(response.data.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除失败:', error)
    }
  }).catch(() => {
    // 用户取消删除操作
  })
}

// 提交表单
const submitForm = async () => {
  if (!cityFormRef.value) return
  
  await cityFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        let response
        // 创建普通对象而不是FormData，因为图片已经通过单独接口上传
        const requestData = {
          name: cityForm.name,
          count: cityForm.count,
          img: cityForm.img // 这里发送的是图片URL字符串
        }
        
        if (isEdit.value) {
          // 编辑
          response = await updateCity(currentId.value!, requestData)
        } else {
          // 添加
          response = await addCity(requestData)
        }
        
        if (response.data && response.data.code === 200) {
          ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
          dialogVisible.value = false
          getCityListData()
        } else {
          ElMessage.error(response.data.message || (isEdit.value ? '修改失败' : '添加失败'))
        }
      } catch (error) {
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
        console.error(isEdit.value ? '修改失败:' : '添加失败:', error)
      }
    }
  })
}

// 处理对话框关闭
const handleDialogClose = () => {
  if (cityFormRef.value) {
    cityFormRef.value.resetFields()
  }
  Object.assign(cityForm, {
    name: '',
    count: 0,
    img: ''
  })
  isEdit.value = false
  currentId.value = null
}

// 处理分页大小变化
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getCityListData()
}

// 处理当前页变化
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getCityListData()
}

// 处理头像上传
const handleUpload = async (options: any) => {
  try {
    const formData = new FormData()
    formData.append('file', options.file)
    
    // 使用axios直接发送上传请求
    const response = await axios.post('/city/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data && response.data.code === 200) {
      cityForm.img = response.data.data.url
      ElMessage.success('图片上传成功')
      options.onSuccess(response)
    } else {
      ElMessage.error(response.data.message || '图片上传失败')
      options.onError(new Error('图片上传失败'))
    }
  } catch (error) {
    console.error('图片上传失败:', error)
    ElMessage.error('图片上传失败')
    options.onError(error)
  }
}

// 处理头像上传前验证
const beforeAvatarUpload = (rawFile: any) => {
  const isJPG = rawFile.type === 'image/jpeg' || rawFile.type === 'image/png'
  const isLt2M = rawFile.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

// 组件挂载时获取数据
onMounted(() => {
  getCityListData()
})

// 返回首页
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './CityList.css';
</style>