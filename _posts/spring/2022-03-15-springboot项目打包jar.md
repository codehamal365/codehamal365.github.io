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

***

参考链接：

> https://docs.spring.io/spring-boot/docs/2.5.2/maven-plugin/reference/htmlsingle/
> https://docs.spring.io/spring-boot/docs/current/reference/html/build-tool-plugins-maven-plugin.html
