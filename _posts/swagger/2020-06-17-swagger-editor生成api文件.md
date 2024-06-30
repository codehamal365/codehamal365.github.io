---
title: Swagger Editor
categories:
  - Swagger
tags:
  - Swagger Editor
---


# Swagger Editor

前面我们分别说了用`openapi`插件生成代码，用`swagger-ui`来测试api接口。那么这两个的前提都是`api`文档yaml文件的存在。那么我们怎么正确的编写

yaml文件呢？今天的主角`swagger-editor`就能很方便的帮我们完成这件事，可以让我们编写的时候及时预览。

当然，这里有个更牛的地方就是，你也可以使用预览界面去做api的测试。**可以编写边测试，而且可以实时修改api文档接口。简直不要太舒服。**

## 参考文档

> https://github.com/swagger-api/swagger-editor

该项目也是一个`nodejs`项目，我们可以把项目down下来本来启动，但感觉也没这个必要。我们可以直接用docker启动，简单方便。



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



## 关于api文档说明

那么有人肯定会问，`openapi`文档的书写要求，字段说明是哪些。可以参考如下。

> https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md

其实我也写的少，只是项目中看别人用到了，所有需要编写的时候，大概还是得看文档来写。



## 更多

当你访问编辑页面，你会看到工具栏还有生成服务端和客户端代码的功能。可谓是真的强大，大家可以研究下是怎么做的。

不过我看到官方有另外两个项目：

- `https://github.com/swagger-api/swagger-codegen`
- `https://github.com/swagger-api/swagger-parser`

大致应该是基于这两个项目做的。有兴趣的朋友可以参考下。

