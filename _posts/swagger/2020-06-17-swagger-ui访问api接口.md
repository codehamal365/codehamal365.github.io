---
title: Swagger UI
categories:
  - Swagger
tags:
  - Swagger UI
---


# Swagger UI：API 接口可视化测试工具

在 API 开发完成后，需要高效的测试工具。Swagger UI 提供基于 OpenAPI 规范的交互式文档，支持直接在浏览器中测试 API，无需额外配置。

相比 Postman，Swagger UI 直接从规范生成测试界面，更适合开发阶段快速验证。

## 主要特性

- **交互式文档**：自动生成 API 文档界面
- **在线测试**：直接在页面执行 API 调用
- **多种格式支持**：YAML/JSON OpenAPI 规范
- **响应预览**：显示请求/响应详情
- **认证支持**：Bearer Token, API Key 等

## Spring Boot 集成

对于 Spring Boot 项目，最简单的方式是添加依赖：

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.0.2</version>
</dependency>
```

配置类：
```java
@Configuration
public class SwaggerConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info().title("My API").version("1.0"));
    }
}
```

访问：http://localhost:8080/swagger-ui.html

## 官方资料

> https://github.com/swagger-api/swagger-ui

这是一个 Node.js 项目，支持本地开发和 Docker 部署。

## dev开发说明

### 步骤

1. `git clone https://github.com/swagger-api/swagger-ui.git`
2. `cd swagger-ui`
3. `npm run dev`
4. Wait a bit
5. Open http://localhost:3200/

### 使用本地yaml或json文件替换api说明文档

之前`openapi`使用的是yaml文件，我们可以直接拿过来，当然`json`文件也可以，但是最好和`openapi`同一起来，这样方便也好书写。

可以在`dev-helper/index.html`文件中替换为该yaml文件。那么本地文件放在哪呢？

在`dev-helper`文件下新建目录`examples`，然后url替换为`url: "./examples/your-local-api-definition.yaml"`

这样启动之后，就可以调试本地`api接口`了。



## api页面之线上

如果公司或自己有服务器，可以将该项目生成的静态文件放到服务器上的目录。例如nginx的目录。

执行步骤如下。

1. `npm run build`
2. 替换`dist`目录下的`index.html`里的`url`参数
3. 放入nginx目录
4. 启动nginx即可



## Docker 部署

### 基本启动
```bash
docker pull swaggerapi/swagger-ui
docker run -d -p 8080:8080 --name swagger-ui swaggerapi/swagger-ui
```

### 高级配置
```bash
# 指定 API 规范 URL
docker run -d -p 8080:8080 \
  -e SWAGGER_JSON_URL=https://petstore.swagger.io/v2/swagger.json \
  swaggerapi/swagger-ui

# 挂载本地文件
docker run -d -p 8080:8080 \
  -v $(pwd)/api.yaml:/app/api.yaml \
  -e SWAGGER_JSON=/app/api.yaml \
  swaggerapi/swagger-ui

# 自定义访问路径和标题
docker run -d -p 8080:8080 \
  -e BASE_URL=/docs \
  -e SWAGGER_JSON_URL=https://api.example.com/swagger.json \
  swaggerapi/swagger-ui
```

访问：http://localhost:8080/docs

### 环境变量
- `SWAGGER_JSON`：本地 JSON 文件路径
- `SWAGGER_JSON_URL`：远程规范 URL
- `BASE_URL`：UI 访问路径
- `VALIDATOR_URL`：规范验证器 URL

更多配置参考：[官方文档](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/configuration.md#docker)

## 替代工具

- **ReDoc**：专注于文档展示的工具
- **Postman**：功能强大的 API 测试平台
- **Insomnia**：现代化的 API 客户端
- **Stoplight**：企业级 API 设计平台

## 最佳实践

- **安全配置**：生产环境限制访问，添加认证
- **版本管理**：为 API 规范建立版本控制
- **自动化集成**：与 CI/CD 集成自动生成文档
- **性能监控**：监控 API 响应时间和错误率

## 自定义主题

可以通过 CSS 自定义 UI 外观：

```html
<link rel="stylesheet" type="text/css" href="custom.css" />
```

## 故障排除

- **CORS 问题**：确保 API 支持跨域请求
- **规范错误**：使用在线验证器检查 OpenAPI 文件
- **加载失败**：检查网络连接和文件路径
