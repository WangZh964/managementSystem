import { ref, watch } from 'vue'

// 主题类型定义
export type ThemeType = 'light' | 'dark' | 'auto'

// 主题管理器类
class ThemeManager {
  private currentTheme = ref<ThemeType>('light')
  
  constructor() {
    this.loadThemeFromStorage()
    this.applyTheme(this.currentTheme.value)
    this.setupSystemThemeListener()
  }
  
  // 从本地存储加载主题
  private loadThemeFromStorage() {
    const savedTheme = localStorage.getItem('theme') as ThemeType
    if (savedTheme) {
      this.currentTheme.value = savedTheme
    } else {
      // 如果没有保存的主题，检测系统偏好
      this.currentTheme.value = this.detectSystemTheme()
    }
  }
  
  // 检测系统主题偏好
  private detectSystemTheme(): ThemeType {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
    return 'light'
  }
  
  // 设置系统主题变化监听
  private setupSystemThemeListener() {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      // 使用更兼容的事件监听方式
      const handleSystemThemeChange = (e: MediaQueryListEvent) => {
        if (this.currentTheme.value === 'auto') {
          this.applyTheme(e.matches ? 'dark' : 'light')
        }
      }
      
      // 兼容不同浏览器的API
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleSystemThemeChange)
      } else {
        // 旧版浏览器的兼容处理
        mediaQuery.addListener(handleSystemThemeChange)
      }
    }
  }
  
  // 应用主题
  private applyTheme(theme: ThemeType) {
    const actualTheme = theme === 'auto' ? this.detectSystemTheme() : theme
    
    // 移除现有的主题类
    document.documentElement.classList.remove('theme-light', 'theme-dark')
    
    // 添加新的主题类
    document.documentElement.classList.add(`theme-${actualTheme}`)
    
    // 设置data-theme属性
    document.documentElement.setAttribute('data-theme', actualTheme)
    
    // 更新CSS变量 - 确保传入的是 'light' 或 'dark' 类型
    this.updateCSSVariables(actualTheme as 'light' | 'dark')
  }
  
  // 更新CSS变量
  private updateCSSVariables(theme: 'light' | 'dark') {
    const root = document.documentElement
    
    if (theme === 'light') {
      // 浅色模式CSS变量 - 使用您当前的渐变背景
      root.style.setProperty('--primary-color', '#409EFF')
      root.style.setProperty('--success-color', '#67C23A')
      root.style.setProperty('--warning-color', '#E6A23C')
      root.style.setProperty('--danger-color', '#F56C6C')
      root.style.setProperty('--info-color', '#909399')
      root.style.setProperty('--text-color', '#303133')
      root.style.setProperty('--background-color', 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)')
      root.style.setProperty('--card-background', 'rgba(255, 255, 255, 0.9)')
    } else {
      // 深色模式CSS变量
      root.style.setProperty('--primary-color', '#409EFF')
      root.style.setProperty('--success-color', '#67C23A')
      root.style.setProperty('--warning-color', '#E6A23C')
      root.style.setProperty('--danger-color', '#F56C6C')
      root.style.setProperty('--info-color', '#909399')
      root.style.setProperty('--text-color', '#E5E5E5')
      root.style.setProperty('--background-color', 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)')
      root.style.setProperty('--card-background', 'rgba(45, 45, 45, 0.9)')
    }
  }
  
  // 切换主题
  public setTheme(theme: ThemeType) {
    this.currentTheme.value = theme
    localStorage.setItem('theme', theme)
    this.applyTheme(theme)
  }
  
  // 获取当前主题
  public getCurrentTheme() {
    return this.currentTheme.value
  }
  
  // 监听主题变化
  public onThemeChange(callback: (theme: ThemeType) => void) {
    watch(this.currentTheme, callback)
  }
}

// 创建单例实例
const themeManager = new ThemeManager()

// 导出主题管理器实例和类型
export default themeManager