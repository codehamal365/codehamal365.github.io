---
title: Azure API Management
categories:
  - Azure
tags:
  - Azure API Management
---


# API Management

This is a simple documentation. You can refer to [official documentation](https://docs.microsoft.com/en-us/azure/api-management) for details.

## About API Management

Azure API Management is a hybrid, multicloud management platform for APIs across all environments. This article provides an overview of common scenarios and key components of API Management.

## Advantage

APIs enable digital experiences, simplify application integration, underpin new digital products, and make data and services reusable and universally accessible. With the proliferation and increasing dependency on APIs, organizations need to manage them as first-class assets throughout their lifecycle.

Azure API Management helps customers meet these challenges:

* Abstract backend architecture diversity and complexity from API consumers

* Securely expose services hosted on and outside of Azure as APIs

* Protect, accelerate, and observe APIs

* Enable API discovery and consumption by internal and external users

## Quickstart

### Create API Management service instance by using Azure Cli

[More information](https://docs.microsoft.com/en-us/azure/api-management/get-started-create-service-instance-cli)

* Create a resource group

  ```bash
  az group create --name myResourceGroup --location centralus
  ```

* Create a new service

  ```bash
  # It can take between 30 and 40 minutes to create and activate an API Management service in this tier. The previous command uses the --no-wait option # so that the command returns immediately while the service is created.
  az apim create --name myapim --resource-group myResourceGroup \
    --publisher-name Contoso --publisher-email admin@contoso.com \
    --no-wait
  
  # Check the status of the deployment by running the az apim show command:
  az apim show --name myapim --resource-group myResourceGroup --output table
  ```

* Clean up resources

  ```bash
  az group delete --name myResourceGroup
  ```

### Create your first api

You can follow this [instruction](https://docs.microsoft.com/en-us/azure/api-management/import-and-publish) and create your api based on api documentation in Json format.

Microsoft provides the backend API used in this example, and hosts it on Azure at [https://conferenceapi.azurewebsites.net?format=json](https://conferenceapi.azurewebsites.net/?format=json).

You can get More Information about mock api, policies and product on the instruction page.

## API Management components

Azure API Management is made up of an API gateway, a management plane, and a developer portal. These components are Azure-hosted and fully managed by default. API Management is available in various tiers differing in capacity and features.
* API gateway
  All requests from client applications first reach the API gateway, which then forwards them to respective backend services. 
  The API gateway acts as a façade to the backend services, allowing API providers to abstract API implementations and evolve backend architecture without impacting API consumers. The gateway enables consistent configuration of routing, security, throttling, caching, and observability.
* Management plane
  API providers interact with the service through the management plane, which provides full access to the API Management service capabilities.
  Customers interact with the management plane through Azure tools including the Azure portal, Azure PowerShell, Azure CLI, a Visual Studio Code extension, or client SDKs in several popular programming languages.
* Developer portal
  The open-source developer portal is an automatically generated, fully customizable website with the documentation of your APIs.
  API providers can customize the look and feel of the developer portal by adding custom content, customizing styles, and adding their branding. Extend the developer portal further by self-hosting.
* Integration with Azure services

## Key concepts

### APIs
APIs are the foundation of an API Management service instance. Each API represents a set of operations available to app developers. Each API contains a reference to the backend service that implements the API, and its operations map to backend operations.
Operations in API Management are highly configurable, with control over URL mapping, query and path parameters, request and response content, and operation response caching.

More information:
* Import and publish your first API
* Mock API responses

### Products

Products are how APIs are surfaced to developers. Products in API Management have one or more APIs, and can be open or protected. Protected products require a subscription key, while open products can be consumed freely.

When a product is ready for use by developers, it can be published. Once published, it can be viewed or subscribed to by developers. Subscription approval is configured at the product level and can either require an administrator's approval or be automatic.

### Groups

Groups are used to manage the visibility of products to developers. API Management has the following built-in groups:
* Administrators - Manage API Management service instances and create the APIs, operations, and products that are used by developers. Azure subscription administrators are members of this group.
* Delopers - Authenticated developer portal users that build applications using your APIs. Developers are granted access to the developer portal and build applications that call the operations of an API.
* Guests - Unauthenticated developer portal users, such as prospective customers visiting the developer portal. They can be granted certain read-only access, such as the ability to view APIs but not call them.

### Developers

Developers represent the user accounts in an API Management service instance. Developers can be created or invited to join by administrators, or they can sign up from the developer portal. Each developer is a member of one or more groups, and can subscribe to the products that grant visibility to those groups.

When developers subscribe to a product, they are granted the primary and secondary key for the product for use when calling the product's APIs.

### Policies

With policies, an API publisher can change the behavior of an API through configuration. Policies are a collection of statements that are executed sequentially on the request or response of an API. Popular statements include format conversion from XML to JSON and call-rate limiting to restrict the number of incoming calls from a developer. For a complete list, see API Management policies.

Policy expressions can be used as attribute values or text values in any of the API Management policies, unless the policy specifies otherwise. Some policies such as the Control flow and Set variable policies are based on policy expressions.

Policies can be applied at different scopes, depending on your needs: global (all APIs), a product, a specific API, or an API operation.

## Use Cases

Azure API Management is ideal for:

- **API Monetization**: Charge for API usage through subscriptions and rate limiting.
- **Legacy System Modernization**: Expose legacy APIs as modern REST APIs.
- **Microservices Orchestration**: Combine multiple microservices into a single API facade.
- **Hybrid and Multi-Cloud**: Manage APIs across on-premises, Azure, and other clouds.

Example: A retail company uses APIM to expose product catalog APIs, securing them with OAuth2 and throttling to prevent abuse.

## Policy Examples

Policies allow customization of API behavior. Here are some examples:

### Rate Limiting

```xml
<policies>
    <inbound>
        <rate-limit calls="100" renewal-period="60" />
    </inbound>
</policies>
```

This limits clients to 100 calls per minute.

### CORS Policy

```xml
<policies>
    <inbound>
        <cors allow-credentials="true">
            <allowed-origins>
                <origin>https://example.com</origin>
            </allowed-origins>
            <allowed-methods>
                <method>GET</method>
                <method>POST</method>
            </allowed-methods>
        </cors>
    </inbound>
</policies>
```

Enables cross-origin requests from specific domains.

### Transformation Policy

```xml
<policies>
    <inbound>
        <set-header name="Authorization" exists-action="override">
            <value>@("Bearer " + context.Request.Headers.GetValueOrDefault("X-API-Key"))</value>
        </set-header>
    </inbound>
</policies>
```

Adds authorization header based on a custom key.

## Monitoring and Analytics

APIM provides built-in analytics:

- **Application Insights Integration**: Monitor API performance and errors.
- **Metrics**: Track request counts, response times, and error rates.
- **Logs**: Detailed logs for troubleshooting.

To enable: In the Azure portal, go to API Management > Application Insights > Enable.

## Integration with Other Azure Services

- **Azure Functions**: Expose serverless functions as APIs.
- **Logic Apps**: Orchestrate workflows triggered by API calls.
- **Event Grid**: Publish events based on API operations.

Example: Integrate with Azure Key Vault for secure storage of secrets used in policies.

## Best Practices

- **Versioning**: Use API versioning to manage changes without breaking clients.
- **Security**: Always use HTTPS, validate tokens, and apply rate limiting.
- **Documentation**: Keep the developer portal updated with accurate API docs.
- **Testing**: Use the test console in the portal to validate APIs.

## Troubleshooting Common Issues

- **401 Unauthorized**: Check subscription keys and policies.
- **429 Too Many Requests**: Adjust rate limiting policies.
- **502 Bad Gateway**: Verify backend service availability.

For more, refer to [Azure APIM Troubleshooting](https://docs.microsoft.com/en-us/azure/api-management/api-management-troubleshoot-issues).

## Additional Resources

- [Azure APIM Samples](https://github.com/Azure-Samples/azure-api-management-samples)
- [Community Forums](https://docs.microsoft.com/en-us/answers/topics/azure-api-management.html)



