---
title: Swagger Editor
categories:
  - Swagger
tags:
  - Swagger Editor
---


# Swagger Editor 使用指南

在 API 开发流程中，编写规范的 OpenAPI 文档至关重要。Swagger Editor 提供了可视化编辑器，支持实时预览和验证 OpenAPI 规范，同时可直接测试 API 接口。

它是编写 YAML/JSON API 文档的理想工具，支持语法高亮、错误提示和代码生成。

## 主要特性

- **实时预览**：编辑时右侧同步显示 API 文档。
- **语法验证**：自动检测 OpenAPI 规范错误。
- **Try it out**：直接在编辑器中测试 API 调用。
- **代码生成**：内置生成客户端和服务端代码。
- **导入/导出**：支持 YAML/JSON 格式。

## 安装方式

### Docker 启动（推荐）
```bash
docker pull swaggerapi/swagger-editor
docker run -d -p 80:8080 swaggerapi/swagger-editor
```

### 高级配置
```bash
# 从 URL 加载现有规范
docker run -d -p 80:8080 -e URL="https://example.com/api.yaml" swaggerapi/swagger-editor

# 挂载本地文件
docker run -d -p 80:8080 -v $(pwd)/api.yaml:/tmp/api.yaml -e SWAGGER_FILE=/tmp/api.yaml swaggerapi/swagger-editor

# 自定义访问路径
docker run -d -p 80:8080 -e BASE_URL=/editor swaggerapi/swagger-editor
```

### 本地开发
```bash
git clone https://github.com/swagger-api/swagger-editor
cd swagger-editor
npm install
npm start
```



## docker启动

> docker pull swaggerapi/swagger-editor
> docker run -d -p 80:8080 swaggerapi/swagger-editor

当然也可以想swagger-ui一样，配置`URL`或`SWAGGER_FILE`(两个同时存在，`URL`优先级更高)、`BASE_URL`访问路径。

例如如下

> docker run -d -p 80:8080 --name swagger-editor -e URL="https://petstore3.swagger.io/api/v3/openapi.json" swaggerapi/swagger-editor
>
> docker run -d -p 80:8080 --name swagger-editor -v $(pwd):/tmp -e SWAGGER_FILE=/tmp/swagger.json swaggerapi/swagger-editor
>
> docker run -d -p 80:8080 --name swagger-editor -e BASE_URL=/swagger-editor swaggerapi/swagger-editor



## OpenAPI 规范编写指南

OpenAPI 3.0 规范定义了 API 文档结构。关键部分包括：

- **info**：API 基本信息（标题、版本、描述）
- **servers**：服务器 URL
- **paths**：API 端点定义
- **components**：可复用组件（schemas, parameters, responses）

### 编写最佳实践
- 使用描述性名称和摘要
- 定义详细的请求/响应 schema
- 添加示例数据
- 使用引用（$ref）避免重复
- 包含安全定义

参考官方文档：
> https://swagger.io/specification/

### 示例结构
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /users:
    get:
      summary: Get users
      responses:
        '200':
          description: Success
```



## 代码生成功能

Swagger Editor 内置代码生成器，支持多种语言和框架：

- 服务端：Spring, Node.js, Flask 等
- 客户端：JavaScript, Python, Java 等

点击 "Generate Client" 或 "Generate Server" 选择目标。

## 替代工具

- **Stoplight Studio**：功能更丰富的桌面应用
- **Apicurio**：在线 OpenAPI 编辑器
- **VS Code 插件**：OpenAPI (Swagger) Editor
- **Postman**：可导入/导出 OpenAPI 规范

## 集成工作流

- 与 CI/CD 集成验证规范
- 使用 OpenAPI Generator 生成代码
- 结合 Swagger UI 进行文档展示

## 注意事项

- 定期更新 Docker 镜像以获取最新功能
- 对于复杂 API，考虑分模块定义
- 使用版本控制管理 API 规范文件

