---
title: Azure Functions
categories:
  - Azure
tags:
  - Azure Functions
---

# Azure Functions
本快速入门以python、linux(Ubuntu)作为基本环境,更多环境案例请参考[官方链接](https://docs.microsoft.com/zh-cn/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser)，并以命令行形式作为demo演示。

## 配置环境

* 安装python，请参考[链接](https://wiki.python.org/moin/BeginnersGuide/Download)

* 安装Azure Functions Core Tools

  ```bash
  # ubuntu
  sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
  
  # 更新apt源
  sudo apt-get update
  
  # 安装core tools包
  sudo apt-get install azure-functions-core-tools-4
  ```

  window、mac安装请参考[链接](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)

* 推荐使用vscode作为ide

  * 安装[Python插件](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  * 安装[Azure Functions插件](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)

  如果安装了Azure Functions插件，可以参考[Vscode创建Functions](https://docs.microsoft.com/zh-cn/azure/azure-functions/create-first-function-vs-code-python)可视化创建。

## 命令行创建函数

* 按如下所示运行 `func init` 命令，在名为 LocalFunctionProj 的文件夹中创建使用指定运行时的函数项目

  ```bash
  func init az-functions --worker-runtime python --docker
  ```

  **注意**:`--docker`会在项目目录创建Dockerfile文件。如需要创建容器，请加上该参数。

  命令执行后项目目录`az-functions`会生成如下配置文件

  * `local.setting.json`，更多配置[参考](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-develop-local#local-settings-file),可配置远程存储卡连接串信息等。
  * `host.json`，更多配置[参考](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-host-json)

* 创建函数

  ```bash
  cd az-functions
  
  func new --name HttpExample --template "HTTP trigger" --authlevel "anonymous"
  ```

  该`func new`命令执行后会在`HttpExample`目录下生成`__init__.py`和`function.json`两个文件

  **__init.py__**

  ```python
  import logging
  
  import azure.functions as func
  
  
  def main(req: func.HttpRequest) -> func.HttpResponse:
      logging.info('Python HTTP trigger function processed a request.')
  
      name = req.params.get('name')
      if not name:
          try:
              req_body = req.get_json()
          except ValueError:
              pass
          else:
              name = req_body.get('name')
  
      if name:
          return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
      else:
          return func.HttpResponse(
               "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
               status_code=200
          )
  ```

  对于 HTTP 触发器，该函数将接收 *function.json* 中定义的变量 `req` 中的请求数据。 `req` 是 [azure.functions.HttpRequest 类](https://docs.microsoft.com/zh-CN/python/api/azure-functions/azure.functions.httprequest)的实例。 在 *function.json* 中定义为 `$return` 的返回对象是 [azure.functions.HttpResponse 类](https://docs.microsoft.com/zh-CN/python/api/azure-functions/azure.functions.httpresponse)的一个实例。 要了解详细信息，请参阅 [Azure Functions HTTP 触发器和绑定](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-bindings-http-webhook?tabs=python)。

  **function.json**

  *function.json* 是一个配置文件，其中定义了函数的输入和输出 `bindings`，包括触发器类型。

  如果需要，可以更改 `scriptFile` 以调用不同的 Python 文件。

  ```json
  {
      "scriptFile": "__init__.py",
      "bindings": [
          {
              "authLevel": "function",
              "type": "httpTrigger",
              "direction": "in",
              "name": "req",
              "methods": [
                  "get",
                  "post"
              ]
          },
          {
              "type": "http",
              "direction": "out",
              "name": "$return"
          }
      ]
  }
  ```

  每个绑定都需要一个方向、类型和唯一的名称。 HTTP 触发器具有类型为 [`httpTrigger`](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-bindings-http-webhook-trigger) 的输入绑定和类型为 [`http`](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-bindings-http-webhook-output) 的输出绑定。

  如要获取模板列表，可执行`func templates list -l python`

* 执行`func start`运行函数

  会出现如下log

  ```
   ...
  
   Now listening on: http://0.0.0.0:7071
   Application started. Press Ctrl+C to shut down.
  
   Http Functions:
  
           HttpExample: [GET,POST] http://localhost:7071/api/HttpExample
   ...
  ```

  可以在浏览器访问` http://localhost:7071/api/HttpExample`

  

## 构建函数容器

执行如下

```bash
docker build --file Dockerfile --force-rm --tag az-functions .
exec docker run --rm -p 7071:80 --name az-functions az-functions
```

访问地址`curl http://localhost:7071/api/HttpExample`



## 发布函数到Azure

### 创建函数的支持性 Azure 资源

在将函数代码部署到 Azure 之前，需要创建三个资源：

- 一个资源组：相关资源的逻辑容器。
- 一个存储帐户：维护有关项目的状态和其他信息。
- 一个函数应用：提供用于执行函数代码的环境。 函数应用映射到本地函数项目，可让你将函数分组为一个逻辑单元，以便更轻松地管理、部署和共享资源。

1. 请登录到 Azure：

   请先安装`az命令`

   ```azurecli
   az login
   ```

2. 使用 Azure CLI 时，可以启用 `param-persist` 选项，它自动跟踪所创建资源的名称。 要了解详细信息，请参阅 [Azure CLI 持久参数](https://docs.microsoft.com/zh-CN/cli/azure/param-persist-howto)。

   ```azurecli
   az config param-persist on
   ```

3. 在所选区域中创建名为 `AzureFunctionsQuickstart-rg` 的资源组：

   ```azurecli
   az group create --name AzureFunctionsQuickstart-rg --location <REGION>
   ```

   [az group create](https://docs.microsoft.com/zh-CN/cli/azure/group#az-group-create) 命令可创建资源组。 在上述命令中，使用从 `<REGION>` 命令返回的可用区域代码，将 `<REGION>` 替换为附近的区域。

   > 不能在同一资源组中托管 Linux 和 Windows 应用。 如果名为 `AzureFunctionsQuickstart-rg` 的现有资源组有 Windows 函数应用或 Web 应用，必须使用其他资源组。

4. 在资源组和区域中创建常规用途存储帐户：

   ```azurecli
   az storage account create --name <STORAGE_NAME> --sku Standard_LRS
   ```

   [az storage account create](https://docs.microsoft.com/zh-CN/cli/azure/storage/account#az-storage-account-create) 命令可创建存储帐户。

   在上一个示例中，将 `<STORAGE_NAME>` 替换为适合你且在 Azure 存储中唯一的名称。 名称只能包含 3 到 24 个数字和小写字母字符。 `Standard_LRS` 指定 [Functions 支持](https://docs.microsoft.com/zh-cn/azure/azure-functions/storage-considerations#storage-account-requirements)的常规用途帐户。

5. 在 Azure 中创建函数应用：

   ```azurecli
   az functionapp create --consumption-plan-location westeurope --runtime python --runtime-version 3.9 --functions-version 4 --name <APP_NAME> --os-type linux --storage-account <STORAGE_NAME>
   ```

   [az functionapp create](https://docs.microsoft.com/zh-CN/cli/azure/functionapp#az-functionapp-create) 命令可在 Azure 创建函数应用。 如果使用的是 Python 3.8、3.7 或 3.6，请将 `--runtime-version` 分别更改为 `3.8`、`3.7` 或 `3.6`。 你必须提供 `--os-type linux`，因为 Python 函数无法在 Windows 上运行，这是默认设置。

   在上一个示例中，将 `<APP_NAME>` 替换为适合自己的全局唯一名称。 `<APP_NAME>` 也是函数应用的默认 DNS 域。

   此命令将创建一个函数应用，该应用在 [Azure Functions 消耗计划](https://docs.microsoft.com/zh-cn/azure/azure-functions/consumption-plan)下指定的语言运行时中运行，根据本教程产生的用量，此操作是免费的。 该命令还会在同一资源组中预配关联的 Azure Application Insights 实例，可以使用它来监视函数应用和查看日志。 有关详细信息，请参阅[监视 Azure Functions](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-monitoring)。 该实例在激活之前不会产生费用。

### Deploy到Azure

在 Azure 中成功创建函数应用后，便可以使用 [func azure functionapp publish](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-run-local#project-file-deployment) 命令部署本地函数项目。

在以下示例中，请将 `<APP_NAME>` 替换为你的应用的名称。

```bash
func azure functionapp publish <APP_NAME>
```

publish 命令显示类似于以下输出的结果:

```
...

Getting site publishing info...
Creating archive for current directory...
Performing remote build for functions project.

...

Deployment successful.
Remote build succeeded!
Syncing triggers...
Functions in msdocs-azurefunctions-qs:
    HttpExample - [httpTrigger]
        Invoke url: https://msdocs-azurefunctions-qs.azurewebsites.net/api/httpexample
```

运行以下命令以在 Azure 门户中查看 Application Insights 中的准实时[流式处理日志](https://docs.microsoft.com/zh-cn/azure/azure-functions/functions-run-local#enable-streaming-logs)：

```console
func azure functionapp logstream <APP_NAME> --browser
```

在单独的终端窗口或浏览器中，再次调用远程函数。 终端中显示了 Azure 中函数执行的详细日志。

## 清理资源

若要继续执行[下一步](https://docs.microsoft.com/zh-cn/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser#next-steps)并添加 Azure 存储队列输出绑定，请保留所有资源，以备将来使用。

否则，请使用以下命令删除资源组及其包含的所有资源，以免产生额外的费用。

```azurecli
az group delete --name AzureFunctionsQuickstart-rg
```