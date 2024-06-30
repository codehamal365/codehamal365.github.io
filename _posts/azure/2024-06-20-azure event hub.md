---
title: Azure EventHub Trigger
categories:
  - Azure
tags:
  - Azure EventHub
---

# Azure Functions-Eventhub Trigger（Local）

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

* 按如下所示运行 `func init` 命令，在名为 az-functions 的文件夹中创建使用指定运行时的函数项目

  ```bash
  func init az-functions --worker-runtime python
  ```

* 创建函数

  ```bash
  cd az-functions
  
  func new --name EventHubTrigger --template "Azure Event Hub trigger" --authlevel "anonymous"
  ```

  该`func new`命令执行后会在`EventHubTrigger`目录下生成`__init__.py`和`function.json`两个文件

  **__init.py__**

  ```python
  import logging
  
  import azure.functions as func
  
  
  def main(event: func.EventHubEvent):
      logging.info('Python EventHub trigger processed an event: %s',
                   event.get_body().decode('utf-8'))
  ```

  **function.json**

  ```json
  {
    "scriptFile": "__init__.py",
    "bindings": [
      {
        "type": "eventHubTrigger",
        "name": "event",
        "direction": "in",
        "eventHubName": "ju-demo",
        "connection": "AzureEventHubConnectionString",
       // "cardinality": "many",
        "consumerGroup": "$Default"
      }
    ]
  }
  ```

  **local.setting.json**

  ```json
  {
    "IsEncrypted": false,
    "Values": {
      "FUNCTIONS_WORKER_RUNTIME": "python",
      "AzureWebJobsStorage": "UseDevelopmentStorage=true",
      "AzureEventHubConnectionString": "Endpoint=sb://odc-demo.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=JnuG9+9wUL4NctCqARuzGGmpBcuAEKSd3i6bVN5PliM="
    }
  }
  ```

  注意事项

  1. `function.json`中的connection 配置在`local.setting.json`的Values中

  2. `function.json`中的`cardinality`中需要去掉，否则`init.py`中的event: func.EventHubEvent需要配置为多个event.详情请看[issue](https://github.com/Azure/azure-functions-python-worker/issues/699)

  3. `local.setting.json`中的`AzureWebJobsStorage`需配置值`UseDevelopmentStorage=true`,并在Vscode中安装插件`azurite`,并使用

     `ctrl+shift+p`启用`Azurite Blob Service`开启本地存储服务

     

* 执行`func start`运行函数

  会出现如下log

  ```
  Azure Functions Core Tools
  Core Tools Version:       4.0.4483 Commit hash: N/A  (64-bit)
  Function Runtime Version: 4.1.3.17473
  
  
  Functions:
  
          HttpTrigger: [GET,POST] http://localhost:7071/api/HttpTrigger
  
          KafkaOutput: [GET,POST] http://localhost:7071/api/KafkaOutput
  
          EventHubTrigger: eventHubTrigger
  
  For detailed output, run func with --verbose flag.
  ```

  

  ## 向Event-hub发送消息

  使用send_message.py向EventHub发送消息。

  ```python
  import logging
  import datetime
  import time
  import json
  import random
  
  from azure.eventhub import (
      EventData,
      EventHubProducerClient,
  )
  
  logger = logging.getLogger("azure")
  
  connect_str = "Endpoint=sb://****/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=****"
  eventhub_name = "eventhub_name"
  try:
      # Create a producer client to send messages to the event hub.
      client = EventHubProducerClient.from_connection_string(
          conn_str=connect_str,
          eventhub_name=eventhub_name,
      )
  
      try:
          start_time = time.time()
          curbatch = client.create_batch()
  
          # while True:
          device_id = random.randrange(0, 10)
          processed_date = str(datetime.datetime.now())
  
          json_message = {"id": device_id, "processed_date": processed_date}
  
          json_message_send = json.dumps(json_message)
          print(f"sending: {json_message_send}")
          time.sleep(1)
  
          curbatch.add(EventData(json_message_send))
          client.send_batch(curbatch)
      except:
          print("failed")
          raise
      finally:
          end_time = time.time()
          client.close()
  
  except:
      print("failed")
  
  ```

  会收到如下log,表明Azure functions成功接受到event-hub消息

  ```
  [2022-05-23T10:12:14.454Z] Python EventHub trigger processed an event: {"id": 4, "processed_date": "2022-05-23 18:12:33.561915"}
  ```

  ## 附录

  python接受event-hub消息脚本。

  ```python
  import asyncio
  from azure.eventhub.aio import EventHubConsumerClient
  
  connect_str = "Endpoint=sb://****/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=****"
  eventhub_name = "eventhub_name"
  
  
  async def main():
      # Create a consumer client for the event hub.
      client = EventHubConsumerClient\
          .from_connection_string(connect_str, consumer_group="$Default", eventhub_name=eventhub_name)
      async with client:
          # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
          await client.receive(on_event=on_event)
  
  
  async def on_event(partition_context, event):
      # Print the event data.
      print(f"""Received the event: \"{event.body_as_str(encoding='UTF-8')}\"
       from the partition with ID: \"{partition_context.partition_id}""")
  
      # Update the checkpoint so that the program doesn't read the events
      # that it has already read when you run it next time.
      await partition_context.update_checkpoint(event)
  
  
  if __name__ == '__main__':
      loop = asyncio.get_event_loop()
      # Run the main method.
      loop.run_until_complete(main())
  ```

  

  


