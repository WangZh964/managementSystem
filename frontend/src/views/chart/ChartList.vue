<template>
  <div class="chart-container">
    <!-- 浮动形状装饰 -->
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    
    <!-- 面板头部 -->
    <div class="panel-header">
      <div class="panel-title">
        <el-icon><List /></el-icon>
        <span>图表统计</span>
      </div>
      <div class="panel-actions">
        <el-button class="home-button" @click="goToHome">
          <el-icon><HomeFilled /></el-icon>
          点击返回首页
        </el-button>
      </div>
    </div>
    
    <!-- 折线图 -->
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>折线图</span>
        </div>
      </template>
      <div class="chart" ref="lineChartRef" style="width: 100%; height: 300px"></div>
    </el-card>

    <el-row :gutter="20" class="chart-row">
      <!-- 柱状图 -->
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>柱状图</span>
            </div>
          </template>
          <div class="chart" ref="barChartRef" style="width: 100%; height: 400px"></div>
        </el-card>
      </el-col>

      <!-- 饼图 -->
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>饼图</span>
            </div>
          </template>
          <div class="chart" ref="pieChartRef" style="width: 100%; height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { List, HomeFilled } from '@element-plus/icons-vue'
import { getLineChartData, getBarChartData, getPieChartData } from '../../api/chart'
import { useRouter } from 'vue-router'

// 初始化路由
const router = useRouter()

// 图表引用
const lineChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()

// 图表实例
let lineChart: echarts.ECharts | null = null
let barChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null

// 初始化折线图
const initLineChart = () => {
  if (!lineChartRef.value) {
    console.error('折线图容器未找到')
    return
  }
  
  // 确保容器有尺寸
  if (lineChartRef.value.offsetWidth === 0 || lineChartRef.value.offsetHeight === 0) {
    console.log('折线图容器尺寸为0，等待DOM渲染完成')
    setTimeout(() => {
      initLineChart()
    }, 100)
    return
  }
  
  console.log('初始化折线图，容器尺寸:', lineChartRef.value.offsetWidth, 'x', lineChartRef.value.offsetHeight)
  lineChart = echarts.init(lineChartRef.value)
  
  // 设置默认空图表
  const defaultOption = {
    title: {
      text: '分公司业绩图',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: [],
      bottom: 0,
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: []
  }
  
  lineChart.setOption(defaultOption)
  
  // 获取数据
  getLineChartData().then(res => {
    console.log('折线图响应数据:', res)
    if (res.code === 200 && res.data) {
      const chartOption = {
        ...defaultOption,
        legend: {
          ...defaultOption.legend,
          data: res.data.legend || []
        },
        xAxis: {
          ...defaultOption.xAxis,
          data: res.data.x_axis || []
        },
        series: res.data.series_list || []
      }
      
      lineChart?.setOption(chartOption, true) // true表示不合并，完全替换
      console.log('折线图数据设置成功')
    } else {
      console.error('获取折线图数据失败:', res.message || '未知错误')
    }
  }).catch(error => {
    console.error('获取折线图数据异常:', error)
  })
}

// 初始化柱状图
const initBarChart = () => {
  if (!barChartRef.value) {
    console.error('柱状图容器未找到')
    return
  }
  
  // 确保容器有尺寸
  if (barChartRef.value.offsetWidth === 0 || barChartRef.value.offsetHeight === 0) {
    console.log('柱状图容器尺寸为0，等待DOM渲染完成')
    setTimeout(() => {
      initBarChart()
    }, 100)
    return
  }
  
  console.log('初始化柱状图，容器尺寸:', barChartRef.value.offsetWidth, 'x', barChartRef.value.offsetHeight)
  barChart = echarts.init(barChartRef.value)
  
  // 设置默认空图表
  const defaultOption = {
    title: {
      text: '员工业绩汇总阅读信息',
      subtext: "河北分公司",
      textAlign: "auto",
      left: "center",
    },
    tooltip: {},
    legend: {
      data: [],
      bottom: 0,
    },
    xAxis: {
      data: []
    },
    yAxis: {},
    series: []
  }
  
  barChart.setOption(defaultOption)
  
  // 获取数据
  getBarChartData().then(res => {
    console.log('柱状图响应数据:', res)
    if (res.code === 200 && res.data) {
      const chartOption = {
        ...defaultOption,
        legend: {
          ...defaultOption.legend,
          data: res.data.legend || []
        },
        xAxis: {
          ...defaultOption.xAxis,
          data: res.data.x_axis || []
        },
        series: res.data.series_list || []
      }
      
      barChart?.setOption(chartOption, true) // true表示不合并，完全替换
      console.log('柱状图数据设置成功')
    } else {
      console.error('获取柱状图数据失败:', res.message || '未知错误')
    }
  }).catch(error => {
    console.error('获取柱状图数据异常:', error)
  })
}

// 初始化饼图
const initPieChart = () => {
  if (!pieChartRef.value) {
    console.error('饼图容器未找到')
    return
  }
  
  // 确保容器有尺寸
  if (pieChartRef.value.offsetWidth === 0 || pieChartRef.value.offsetHeight === 0) {
    console.log('饼图容器尺寸为0，等待DOM渲染完成')
    setTimeout(() => {
      initPieChart()
    }, 100)
    return
  }
  
  console.log('初始化饼图，容器尺寸:', pieChartRef.value.offsetWidth, 'x', pieChartRef.value.offsetHeight)
  pieChart = echarts.init(pieChartRef.value)
  
  // 设置默认空图表
  const defaultOption = {
    title: {
      text: '用户来源',
      subtext: 'Fake Data',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: '50%',
        data: [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  pieChart.setOption(defaultOption)
  
  // 获取数据
  getPieChartData().then(res => {
    console.log('饼图响应数据:', res)
    if (res.code === 200 && res.data) {
      const chartOption = {
        ...defaultOption,
        series: [
          {
            ...defaultOption.series[0],
            data: res.data || []
          }
        ]
      }
      
      pieChart?.setOption(chartOption, true) // true表示不合并，完全替换
      console.log('饼图数据设置成功')
    } else {
      console.error('获取饼图数据失败:', res.message || '未知错误')
    }
  }).catch(error => {
    console.error('获取饼图数据异常:', error)
  })
}

// 窗口大小改变时，重新调整图表大小
const handleResize = () => {
  lineChart?.resize()
  barChart?.resize()
  pieChart?.resize()
}

onMounted(() => {
  initLineChart()
  initBarChart()
  initPieChart()
  
  // 添加窗口大小改变事件监听
  window.addEventListener('resize', handleResize)
})

// 返回首页方法
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
@import './ChartList.css';
</style>