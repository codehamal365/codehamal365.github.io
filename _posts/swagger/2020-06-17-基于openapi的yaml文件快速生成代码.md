---
title: OpenApi代码生成
categories:
  - Swagger
tags:
  - OpenApi tools
---


# OpenApi tools
有时候项目在需求对接或是澄清阶段，客户或是技术经理会把需求的api接口通过yaml定义出来，也就是我们所说的`swagger-api`文件。这样开发人员能更清楚的了解到接口的入参和出参，方便开发。
这时候，你可能觉得自己根据yaml手写model和api定义接口就可以了，我以前也是这么做的，但是看到团队的代码，发现有一种更简洁的方法,那就是根据`openapi-generator`自动生成java代码，这样就方便多了，简直不要太爽了。

# 官方资料
官方参考资料可以参考如下。
> https://github.com/OpenAPITools/openapi-generator

本篇所讲的是基于`openapi-generator`的maven插件，参考地址如下
> https://github.com/OpenAPITools/openapi-generator/tree/master/modules/openapi-generator-maven-plugin

截止当前使用版本为：`v5.4.0`

# 具体步骤

## 添加pom依赖
**build 块**
```xml
<!-- build 块 -->
<build>
    <plugins>
        <plugin>
            <groupId>org.openapitools</groupId>
            <artifactId>openapi-generator-maven-plugin</artifactId>
            <version>5.4.0</version>
            <executions>
                <execution>
                    <id>generatePetEtc</id>
                    <goals>
                        <goal>generate</goal>
                    </goals>
                    <configuration>
                        <inputSpec>${project.basedir}/doc/api.yaml</inputSpec>
                        <generatorName>spring</generatorName>
                        <apiPackage>org.example.api</apiPackage>
                        <modelPackage>org.example.model</modelPackage>
                        <!-- 这里会将代码生成在src目录，实际中我们可以省略该处 那么代码会生成在target目录 -->
                        <output>${project.basedir}</output>
                        <supportingFilesToGenerate>ApiUtil.java</supportingFilesToGenerate>
                        <configOptions>
                            <skipDefaultInterface>true</skipDefaultInterface>
                            <interfaceOnly>true</interfaceOnly>
                        </configOptions>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```
**dependencies 块**

注意这里依赖以下模块，不然会报错
- web 依赖http
- validation-api 依赖api的校验部分
- swagger-annotations 代码生成的依赖
- jackson-databind-nullable 数据绑定依赖

```xml
<dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
        </dependency>

        <dependency>
            <groupId>io.swagger.core.v3</groupId>
            <artifactId>swagger-annotations</artifactId>
            <version>2.1.13</version>
        </dependency>

        <dependency>
            <groupId>org.openapitools</groupId>
            <artifactId>jackson-databind-nullable</artifactId>
            <version>0.2.2</version>
            <scope>compile</scope>
        </dependency>
</dependencies>
```

## build块解读
```
- <inputSpec>${project.basedir}/doc/api.yaml</inputSpec>
  - 项目doc目录下的api.yaml
  - 关于api.yaml写法可以参考官方文档 
  > https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/test/resources/3_0/petstore.yaml
- <output>${project.basedir}</output>
  实践中最好不要改配置，这样代码生成都在target目录下，不会影响源代码。
- `<execution>`块可以写多个
```

## 执行 mvn clean package
执行成功后,切换到 /target/generated-sources/openapi/src/main/java/org/example   会看到生成的model和api接口。odel和api接口。