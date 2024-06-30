---
title: Swagger UI
categories:
  - Swagger
tags:
  - Swagger UI
---


# 写在前面

之前我们写过可以通过`openapi`的插件快速生成代码(包括我们常用的model、api的接口等)，这样我们就能快速开发业务了。那么接口开发完成后，我们除了通过ut测试接口的完备性，同样也可以通过`postman`来测试接口是否正确。那么`postman`有一个问题就是，我们需要手动去配入接口的路径和参数，那么有人可能就说了，一个人配置后共享配置的`json`文件就行了，可行是可行，甚至还有在线的类型共享测试接口的开源软件。

我们今天其实并不关心这个问题，我们关心我们自己开发的时候如何去快速测试接口，提高效率，并不是来考虑团队协作之类的。

那么主角`swagger-ui`就来了,我们一起看看吧。

# 官方资料

官方资料可参考

> https://github.com/swagger-api/swagger-ui

说明以下，这是一个`nodejs`项目，我们可以先安装`node`环境。然后体验本地dev开发。

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



## docker启动swagger-ui

步骤。

1. `docker pull swaggerapi/swagger-ui`
2. `docker run  --name swagger-ui -p 8888:8080 -e BASE_URL=/swagger -e SWAGGER_JSON=/foo/api.yml -v ~/tmp/api:/foo swaggerapi/swagger-ui`

3. 访问`http://localhost:8888/swagger`就可以看到ui界面了。

这里我们配置了`BASE_URL`即是host后面的路径，通过volume配置了api的路径。

关于docker的更多配置可以参考[配置](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/configuration.md#docker)。

当然我们也可以对官方的镜像做定制来满足我们的各种需求。后面如果有时间，会写一篇文章。
