# MCP React Code Generator - SSE 支持

## 🎉 功能概述

本应用已升级支持 **Server-Sent Events (SSE)** 流式响应，可以实时显示代码生成进度和状态。

## 🚀 新增功能

### 1. 流式代码生成 (`/invoke/stream`)
- **实时进度显示**: 显示代码生成的各个步骤
- **分步骤反馈**: 解析数据 → 加载模板 → 渲染代码 → 优化输出
- **错误处理**: 流式错误信息反馈
- **非阻塞**: 客户端可以实时获取进度更新

### 2. 可视化测试界面 (`/test`)
- **交互式界面**: 支持普通调用和流式调用对比
- **实时进度条**: 可视化显示生成进度
- **日志显示**: 实时显示处理步骤
- **结果预览**: 格式化显示生成的React代码

## 📝 API 端点

### 原有端点（保持兼容）
- `GET /` - 服务状态
- `GET /schema` - API schema信息
- `POST /invoke` - 普通代码生成

### 新增端点
- `POST /invoke/stream` - SSE流式代码生成
- `GET /test` - 测试页面

## 🔧 使用方法

### 1. 启动服务器
```bash
python -m uvicorn main:app --reload --port 8000
```

### 2. 方式一：使用测试页面
访问 `http://localhost:8000/test`，在界面中：
1. 输入或修改MCP JSON数据
2. 点击"流式生成 (SSE)"按钮
3. 观察实时进度和日志
4. 查看最终生成的React代码

### 3. 方式二：使用测试脚本
```bash
python test_sse.py
```

### 4. 方式三：直接API调用

#### 普通调用
```bash
curl -X POST "http://localhost:8000/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "mcp_json": {
      "model": {
        "name": "MyComponent",
        "style": {
          "width": 300,
          "height": 200,
          "backgroundColor": "#f0f8ff"
        }
      },
      "control": {
        "props": {
          "hasAvatar": true
        }
      },
      "prompt": "生成一个用户卡片组件"
    }
  }'
```

#### SSE流式调用
```bash
curl -X POST "http://localhost:8000/invoke/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "mcp_json": {
      "model": {
        "name": "MyComponent",
        "style": {
          "width": 300,
          "height": 200,
          "backgroundColor": "#f0f8ff"
        }
      },
      "control": {
        "props": {
          "hasAvatar": true
        }
      },
      "prompt": "生成一个用户卡片组件"
    },
    "stream": true
  }'
```

## 📊 SSE 数据格式

流式响应使用标准SSE格式，每个事件包含JSON数据：

```javascript
// 开始事件
data: {"type": "start", "message": "开始生成 React 代码"}

// 进度事件
data: {"type": "progress", "step": "parsing", "message": "正在解析 MCP 数据结构...", "progress": 20}

// 结果事件
data: {"type": "result", "output": "function MyComponent() { ... }"}

// 结束事件
data: {"type": "end"}

// 错误事件
data: {"type": "error", "error": "错误信息"}
```

## 🎯 使用场景

1. **开发调试**: 实时观察代码生成过程
2. **用户体验**: 为长时间的代码生成提供进度反馈
3. **错误排查**: 精确定位生成过程中的问题
4. **性能监控**: 分析各个生成步骤的耗时

## 🔄 兼容性

- ✅ 保持原有API完全兼容
- ✅ 支持现代浏览器的EventSource API
- ✅ 支持curl和Python requests等客户端
- ✅ 自动错误恢复和连接管理

## 🛠 技术实现

- **后端**: FastAPI + StreamingResponse
- **前端**: 原生EventSource API
- **格式**: 标准SSE协议
- **编码**: UTF-8支持中文
- **错误处理**: 优雅的错误传播和恢复

## 📋 依赖更新

新增依赖项：
```
requests  # 用于测试脚本
python-multipart  # 支持更多文件类型
```

安装依赖：
```bash
pip install -r requirements.txt
```

## 🎉 快速体验

1. 启动服务: `python -m uvicorn main:app --reload --port 8000`
2. 打开浏览器: `http://localhost:8000/test`
3. 点击"流式生成 (SSE)"按钮
4. 观察实时进度和结果！

现在您的MCP React Code Generator支持流式响应了！🎊 