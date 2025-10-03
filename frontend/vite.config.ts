import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      // 将所有 /api 开头的请求代理到后端
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // 去除 /api 前缀
      },
      // 静态资源代理
      '/image': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // 登录相关
      '/login': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/register': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/logout': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/csrf': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // 其他API路径代理
      '/user': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/task': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/pretty': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/city': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/order': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/depart': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
