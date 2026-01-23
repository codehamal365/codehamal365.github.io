---
title: Azure CosmosDB
categories:
  - Azure
tags:
  - Azure CosmosDB
---

# Azure Cosmos DB

Azure Cosmos DB is a fully managed NoSQL database service for modern app development. It offers single-digit millisecond response times, automatic and instant scalability, and guaranteed speed at any scale.

## Key Features

- **Global Distribution**: Replicate data across multiple Azure regions for low-latency access.
- **Multi-Model**: Supports document, key-value, graph, and column-family data models.
- **Consistency Levels**: Choose from strong, bounded staleness, session, consistent prefix, or eventual consistency.
- **Serverless Option**: Pay only for throughput and storage used.
- **Integrated Analytics**: Use Azure Synapse Link for real-time analytics without data movement.

## Getting Started

### Prerequisites

- Azure subscription
- Python 3.6+
- Install SDK: `pip install azure-cosmos`

### Connection

Use connection string or key-based authentication.

```python
from azure.cosmos.aio import CosmosClient

client = CosmosClient.from_connection_string(os.environ['CosmosDBConnectionString'])
```

## Database and Container Management

### Create Database

```python
database = await client.create_database("MyDatabase")
```

### Create Container with Partition Key

```python
from azure.cosmos import PartitionKey

container = await database.create_container(
    id="MyContainer",
    partition_key=PartitionKey(path="/partitionKey")
)
```

## CRUD Operations

### Create Item

```python
item = {"id": "1", "name": "John", "partitionKey": "users"}
await container.create_item(item)
```

### Read Item

```python
item = await container.read_item(item="1", partition_key="users")
```

### Update Item

```python
item["name"] = "Jane"
await container.replace_item(item="1", body=item)
```

### Delete Item

```python
await container.delete_item(item="1", partition_key="users")
```

### Query Items

```python
query = "SELECT * FROM c WHERE c.partitionKey = @pk"
parameters = [{"name": "@pk", "value": "users"}]
items = container.query_items(query=query, parameters=parameters)
async for item in items:
    print(item)
```

## Async Operations Example

The following example demonstrates async operations for bulk inserts.

```python
import asyncio
import os
from contextlib import suppress
from typing import Dict

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError

async def create_item(container_client: ContainerProxy, item: Dict):
    await container_client.create_item(item)

async def main():
    async with CosmosClient.from_connection_string(
            os.environ['CosmosDBConnectionString']
    ) as client:
        database = client.get_database_client("odcpersistence")
        with suppress(CosmosResourceNotFoundError):
            await database.delete_container('mappings')

        container_client = await database.create_container(
            id="mappings", partition_key=PartitionKey(path="/id")
        )

        jobs = [
            create_item(container_client, {"id": f"id{i}", "data": f"value{i}"})
            for i in range(10)
        ]
        await asyncio.gather(*jobs)

if __name__ == '__main__':
    asyncio.run(main())
```

## Partitioning and Scaling

- **Partition Key**: Choose a property that distributes data evenly.
- **Throughput**: Provision RU/s at database or container level.
- **Auto-Scale**: Enable to automatically adjust throughput based on usage.

## Best Practices

- **Choose Appropriate Consistency**: Balance performance and consistency needs.
- **Optimize Queries**: Use indexed properties and avoid cross-partition queries.
- **Monitor Usage**: Use Azure Monitor for metrics and alerts.
- **Backup**: Enable continuous backup for data protection.

## Troubleshooting

- **RU Limit Exceeded**: Increase provisioned throughput.
- **Partition Key Issues**: Ensure even distribution to avoid hot partitions.
- **Connection Errors**: Verify firewall settings and connection strings.

## Additional Resources

- [Azure Cosmos DB Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/)
- [Python SDK Samples](https://github.com/Azure/azure-cosmos-python)
- [Performance Tips](https://docs.microsoft.com/en-us/azure/cosmos-db/performance-tips)
