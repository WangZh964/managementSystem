# 用户管理系统 (User Management System)

## 📋 项目简介

这是一个基于前后端分离架构的用户管理系统，提供完整的用户信息管理功能，包括用户增删改查、部门管理、城市信息管理等模块。

## 🚀 技术栈

### 后端技术栈
- **框架**: Django 5.1.4
- **数据库**: MySQL
- **编程语言**: Python 3.11
- **ORM**: Django ORM
- **API**: RESTful API设计
- **认证**: Session + Token认证
- **文件上传**: Django FileField

### 前端技术栈
- **框架**: Vue 3.5.21
- **构建工具**: Vite 7.1.6
- **语言**: TypeScript
- **UI组件库**: Element Plus 2.11.3 + Naive UI 2.43.1
- **状态管理**: Pinia 3.0.3
- **路由**: Vue Router 4.5.1
- **HTTP客户端**: Axios 1.12.2
- **样式**: Tailwind CSS 4.1.13
- **图表**: ECharts 6.0.0 + Vue-ECharts 7.0.3

## 📊 功能模块

### 1. 用户管理模块
- ✅ 用户列表展示（分页功能）
- ✅ 添加新用户
- ✅ 编辑用户信息
- ✅ 删除用户
- ✅ 用户信息字段：姓名、密码、年龄、账户余额、性别、部门、入职时间

### 2. 部门管理模块
- ✅ 部门列表展示
- ✅ 部门增删改查
- ✅ 部门与用户关联

### 3. 城市管理模块
- ✅ 城市列表展示
- ✅ 城市信息管理（名称、人口、Logo图片）
- ✅ 图片上传功能

### 4. 管理员模块
- ✅ 管理员登录/注册
- ✅ 管理员信息管理
- ✅ 权限控制

### 5. 其他功能模块
- ✅ 靓号管理
- ✅ 任务管理
- ✅ 订单管理
- ✅ 数据图表展示

## 🛠️ 项目结构

```
managementProject/
├── backend/                 # Django后端项目
│   ├── app01/              # 主应用
│   │   ├── models.py       # 数据模型
│   │   ├── views/          # 视图函数
│   │   ├── utils/          # 工具类
│   │   └── migrations/     # 数据库迁移文件
│   ├── djangoProject01/    # Django项目配置
│   └── manage.py          # Django管理脚本
└── frontend/               # Vue前端项目
    ├── src/
    │   ├── views/         # 页面组件
    │   ├── components/    # 公共组件
    │   ├── api/           # API接口
    │   └── utils/         # 工具函数
```

## ⚙️ 安装与运行

### 环境要求
- Python 3.10+
- Node.js 16+
- MySQL 5.7+

### 后端启动

1. **安装依赖**
```bash
cd backend
pip install django==5.1.4 mysqlclient corsheaders
```

2. **数据库配置**
- 创建MySQL数据库：`db_users`
- 修改 `backend/djangoProject01/settings.py` 中的数据库配置

3. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **启动服务**
```bash
python manage.py runserver
```

### 前端启动

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

## 🔧 核心特性

### 1. 前后端分离架构
- 前端使用Vue3 + TypeScript构建SPA应用
- 后端提供RESTful API接口
- 支持CORS跨域请求

### 2. 数据验证与错误处理
- 前端表单验证
- 后端ModelForm验证
- 统一的错误响应格式
- 详细的调试信息输出

### 3. 文件上传功能
- 支持图片上传
- 自动文件路径处理
- 文件类型验证

### 4. 权限控制
- 基于Session的登录认证
- Token认证支持
- 中间件权限验证

### 5. 响应式设计
- 支持移动端和桌面端
- 现代化UI设计
- 用户体验优化

## 🐛 已修复的关键问题

1. **城市管理模块**
   - 修复图片上传处理逻辑
   - 解决编辑和添加城市时的400错误

2. **用户管理模块**
   - 修复字段转换问题（depart_id → depart）
   - 解决数据库约束错误（create_time字段）
   - 完善表单验证和错误处理

3. **API接口优化**
   - 统一响应格式
   - 增强错误信息提示
   - 添加调试日志

## 📈 项目亮点

- **现代化技术栈**: 使用最新的Vue3和Django5框架
- **类型安全**: TypeScript提供更好的开发体验
- **组件化开发**: 可复用的组件设计
- **RESTful API**: 标准的API设计规范
- **响应式布局**: 适配多种设备
- **完善的错误处理**: 详细的错误信息和调试支持

## 🔮 未来规划

- [ ] 添加角色权限管理
- [ ] 实现数据导入导出功能
- [ ] 添加数据统计报表
- [ ] 支持多语言国际化
- [ ] 添加单元测试和集成测试
- [ ] 部署到生产环境

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证。

---

**开发团队**: 个人项目  
**最后更新**: 2025年9月  
**项目状态**: ✅ 已完成核心功能开发