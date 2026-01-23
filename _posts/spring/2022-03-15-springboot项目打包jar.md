---
title: SpringBoot项目打包
categories:
  - Spring
tags:
  - PropertySource
  - ConfigurationProperties
---


# springboot项目打包

## plugin基本配置

在springboot应用中，我们可以使用`spring-boot-maven-plugin`插件来打包应用，我们只需在`pom.xml`中加入以下配置：

```xml
<project>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

无需任何配置，springbot会自动定位到应用程序入口的Class，我们执行以下maven命令即可打包

```bash
mvn clean package
```

以`spring-exec-jar`项目为例，打包后我们在target目录下可以看到两个jar文件：

```bash
$ ls
classes
generated-sources
maven-archiver
maven-status
springboot-exec-jar-1.0-SNAPSHOT.jar
springboot-exec-jar-1.0-SNAPSHOT.jar.original
```

其中，`springboot-exec-jar-1.0-SNAPSHOT.jar.original`是Maven标准打包插件打的jar包，它只包含我们自己的Class，不包含依赖，而`springboot-exec-jar-1.0-SNAPSHOT.jar`是Spring Boot打包插件创建的包含依赖的jar，可以直接运行：

```xml
java -jar springboot-exec-jar-1.0-SNAPSHOT.jar
```

这样，部署一个Spring Boot应用就非常简单，无需预装任何服务器，只需要上传jar包即可。

在打包的时候，因为打包后的Spring Boot应用不会被修改，因此，默认情况下，`spring-boot-devtools`这个依赖不会被打包进去。但是要注意，使用早期的Spring Boot版本时，需要配置一下才能排除`spring-boot-devtools`这个依赖：

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <excludeDevtools>true</excludeDevtools>
    </configuration>
</plugin>
```

如果不喜欢默认的项目名+版本号作为文件名，可以加一个配置指定文件名：

```xml
<project >
    <build>
        <finalName>awesome-app</finalName>
    </build>
</project>
```

## 可能遇到的问题

如果pom中父类依赖并非`spring-boot-starter-parent`项目打包的时候可能会遇到问题。

按照上面的条件，我们依次执行如下命令。

```bash
mvn clean install -DskipTests=true
java -jar app-demo.jar
app-demo.jar中没有主清单属性
```

会出现jar中没有主清单属性错误。查看了生成的包，只有几十k,说明并没有打包成功。

那这种情况的解决办法就是修改pom文件

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <executions>
                <execution>
                    <goals>
                        <goal>repackage</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

然后继续打包发现就没有问题了。

### 分析原因

- maven中的插件和phase都需要绑定在goal上，真正执行的是goal中的mojo
- Spring-boot-maven-plugin的作用是将项目打包成可执行的jar
- 如果打包的项目父工程是spring-boot-starter-parent,那么会将上述插件绑定到repackage的goal上
- 否则，我们需要手动指定repackage
- repackage的goal,会在打包后，将原包，添加上original的后缀，然后重新打出来我们执行的jar包。

## spring boot maven plugin 说明

Spring Boot的Maven插件（Spring Boot Maven plugin）能够以Maven的方式为应用提供Spring Boot的支持，即为Spring Boot应用提供了执行Maven操作的可能。
Spring Boot Maven plugin能够将Spring Boot应用打包为可执行的jar或war文件，然后以通常的方式运行Spring Boot应用。
Spring Boot Maven plugin的最新版本为2017.6.8发布的1.5.4.RELEASE，要求Java 8, Maven 3.2及以后。

### Spring Boot Maven plugin的5个Goals

spring-boot:repackage，默认goal。在mvn package之后，再次打包可执行的jar/war，同时保留mvn package生成的jar/war为.origin
spring-boot:run，运行Spring Boot应用
spring-boot:start，在mvn integration-test阶段，进行Spring Boot应用生命周期的管理
spring-boot:stop，在mvn integration-test阶段，进行Spring Boot应用生命周期的管理
spring-boot:build-info，生成Actuator使用的构建信息文件build-info.properties
### 配置pom.xml文件

```xml
<build>
	<plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
		</plugin>
	</plugins>
</build>
```

### mvn package spring-boot:repackage说明

Spring Boot Maven plugin的最主要goal就是repackage，其在Maven的package生命周期阶段，能够将mvn package生成的软件包，再次打包为可执行的软件包，并将mvn package生成的软件包重命名为*.original。

基于上述配置，对一个生成Jar软件包的项目执行如下命令。

mvn package spring-boot:repackage
可以看到生成的两个jar文件，一个是*.jar，另一个是*.jar.original。

在执行上述命令的过程中，Maven首先在package阶段打包生成*.jar文件；然后执行spring-boot:repackage重新打包，查找Manifest文件中配置的Main-Class属性，如下所示：

```bahs
Manifest-Version: 1.0
Implementation-Title: gs-consuming-rest
Implementation-Version: 0.1.0
Archiver-Version: Plexus Archiver
Built-By: sam
Implementation-Vendor-Id: org.springframework
Spring-Boot-Version: 1.5.3.RELEASE
Implementation-Vendor: Pivotal Software, Inc.
Main-Class: org.springframework.boot.loader.JarLauncher
Start-Class: com.ericsson.ramltest.MyApplication
Spring-Boot-Classes: BOOT-INF/classes/
Spring-Boot-Lib: BOOT-INF/lib/
Created-By: Apache Maven 3.5.0
Build-Jdk: 1.8.0_131
```

注意，其中的Main-Class属性值为org.springframework.boot.loader.JarLauncher；

Start-Class属性值为com.ericsson.ramltest.MyApplication。

其中com.ericsson.ramltest.MyApplication类中定义了main()方法，是程序的入口。

通常，Spring Boot Maven plugin会在打包过程中自动为Manifest文件设置Main-Class属性，事实上该属性究竟作用几何，还可以受Spring Boot Maven plugin的配置属性layout控制的，示例如下。

```xml
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
  <configuration>
    <mainClass>${start-class}</mainClass>
    <layout>ZIP</layout>
  </configuration>
  <executions>
    <execution>
      <goals>
        <goal>repackage</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

注意，这里的layout属性值为ZIP。

**layout属性的值可以如下：**

**JAR**，即通常的可执行jar
Main-Class: org.springframework.boot.loader.JarLauncher

**WAR**，即通常的可执行war，需要的servlet容器依赖位于WEB-INF/lib-provided
Main-Class: org.springframework.boot.loader.warLauncher

**ZIP**，即DIR，类似于JAR
Main-Class: org.springframework.boot.loader.PropertiesLauncher

**MODULE**，将所有的依赖库打包（scope为provided的除外），但是不打包Spring Boot的任何Launcher。
NONE，将所有的依赖库打包，但是不打包Spring Boot的任何Launcher。

integration-test阶段中的Spring Boot Maven plugin的start/stop

```xml
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
  <executions>
    <execution>
      <goals>
        <goal>repackage</goal>
      </goals>
    </execution>
    <execution>
      <id>pre-integration-test</id>
      <goals>
        <goal>start</goal>
      </goals>
      <configuration>
        <profiles>
          <profile>test</profile>
        </profiles>
      </configuration>
    </execution>
    <execution>
      <id>post-integration-test</id>
      <goals>
        <goal>stop</goal>
      </goals>
    </execution>
  </executions>
  <configuration>
    <mainClass>${start-class}</mainClass>
    <executable>true</executable>
    <fork>false</fork>
    <wait>1000</wait>
    <maxAttempts>180</maxAttempts>
  </configuration>
</plugin>
```

## Gradle支持

对于使用Gradle的项目，配置类似：

```gradle
plugins {
    id 'org.springframework.boot' version '2.7.0'
    id 'java'
}

bootJar {
    mainClass = 'com.example.Application'
    archiveFileName = 'awesome-app.jar'
    // 排除devtools
    exclude '**/spring-boot-devtools-*.jar'
}
```

## 高级配置选项

### 多环境打包

```xml
<profiles>
    <profile>
        <id>prod</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <configuration>
                        <profiles>
                            <profile>prod</profile>
                        </profiles>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

### 自定义Manifest

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <mainClass>com.example.Application</mainClass>
        <layout>JAR</layout>
        <executable>true</executable>
    </configuration>
</plugin>
```

### 多模块项目打包

对于多模块项目，可以在父模块配置插件：

```xml
<!-- 在父pom.xml中 -->
<build>
    <pluginManagement>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.springframework.boot</groupId>
                            <artifactId>spring-boot-configuration-processor</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </pluginManagement>
</build>

<!-- 在启动模块中 -->
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <goals>
                <goal>repackage</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

## Docker集成

### 多阶段Docker构建

```dockerfile
# 构建阶段
FROM maven:3.8.4-openjdk-11 as builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# 运行阶段
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
```

### Jib插件

使用Google Jib进行容器化：

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>3.3.1</version>
    <configuration>
        <to>
            <image>my-registry/my-app</image>
        </to>
    </configuration>
</plugin>
```

## 原生镜像打包

使用GraalVM创建原生镜像：

```xml
<plugin>
    <groupId>org.graalvm.buildtools</groupId>
    <artifactId>native-maven-plugin</artifactId>
    <version>0.9.13</version>
    <extensions>true</extensions>
    <executions>
        <execution>
            <id>build-native</id>
            <goals>
                <goal>build</goal>
            </goals>
            <phase>package</phase>
        </execution>
    </executions>
    <configuration>
        <buildArgs>
            <buildArg>--no-fallback</buildArg>
        </buildArgs>
    </configuration>
</plugin>
```

## 安全加固

### 可执行JAR签名

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jarsigner-plugin</artifactId>
    <version>3.0.0</version>
    <executions>
        <execution>
            <id>sign</id>
            <goals>
                <goal>sign</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### 依赖检查

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>7.1.1</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

## CI/CD集成

### GitHub Actions示例

```yaml
name: Build and Deploy
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up JDK 11
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    - name: Build with Maven
      run: mvn clean package -DskipTests
    - name: Upload JAR
      uses: actions/upload-artifact@v3
      with:
        name: app-jar
        path: target/*.jar
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'java -jar target/*.jar'
            }
        }
    }
}
```

## 性能优化

### JVM调优

```bash
java -server \
  -Xms512m -Xmx1024m \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -jar app.jar
```

### 应用启动优化

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <mainClass>com.example.Application</mainClass>
        <layoutFactory>
            <type>ZIP</type>
        </layoutFactory>
    </configuration>
</plugin>
```

## 故障排除

### 常见问题

1. **"no main manifest attribute"**：检查是否正确配置了mainClass

2. **依赖冲突**：使用`mvn dependency:tree`分析依赖树

3. **内存不足**：增加Maven内存：`MAVEN_OPTS="-Xmx2g"`

4. **编码问题**：设置正确的文件编码

5. **平台兼容性**：确保构建和运行环境一致

### 调试技巧

```bash
# 启用调试
java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 -jar app.jar

# 查看JAR内容
jar tf app.jar

# 解压JAR
jar xf app.jar
```

## 最佳实践

1. **版本管理**：使用一致的Spring Boot版本
2. **依赖管理**：定期更新依赖，检查安全漏洞
3. **构建优化**：使用多线程构建，缓存依赖
4. **测试集成**：在构建过程中运行测试
5. **文档化**：记录构建和部署过程
6. **监控**：监控应用启动时间和资源使用

***

参考链接：

> https://docs.spring.io/spring-boot/docs/2.5.2/maven-plugin/reference/htmlsingle/
> https://docs.spring.io/spring-boot/docs/current/reference/html/build-tool-plugins-maven-plugin.html
> https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html
