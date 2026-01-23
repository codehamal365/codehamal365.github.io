---
title: Spring自定义配置文件
categories:
  - Spring
tags:
  - PropertySource
  - ConfigurationProperties
---


在`@ConfigurationProperties`一节中，我们知道了application.yaml中配置的属性会被绑定到该类的属性中，那么如果很多配置都写到application中，会导致配置很乱。同时，如果配置是从其他远程或者目录加载，application.yaml配置并不适合的适合，怎么去加载其他的配置文件呢。下面先讲以下两种方法，其实springboot应该也支持以其他profile的形式去剥离配置，但是目前以springboot-2.5.2这块还在研究中，后续如果可以，会补充上来。

## 通过`@PropertySource`注解

先来看下`@PropertySource`源码

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Repeatable(PropertySources.class)
public @interface PropertySource {
    /**
     * 资源的名称
     */
    String name() default "";
    /**
     * 资源文件路径，可以是数据多个文件地址
     * 可以是classpath地址如：
     *                  "classpath:/com/myco/app.properties"
     * 也可以是对应的文件系统地址如：
     *                  "file:/path/to/file"
     */
    String[] value();
    /**
     * 是否忽略文件资源是否存在，默认是false,也就是说配置不存在的文件地址spring启动将会报错
     */
    boolean ignoreResourceNotFound() default false;
    /**
     * 这个没什么好说的了就是对应的字符编码了，默认是空值，如果配置文件中有中文应该设置为utf-8     */
    String encoding() default "";
    /**
     * 关键的元素了 读取对应资源文件的工厂类了 默认的是PropertySourceFactory
     */
    Class<? extends PropertySourceFactory> factory() default PropertySourceFactory.class;
}
```

对于`@PropertySource`,官方的使用说明如下：

- 在一个`@Configuration`标注的类上加上该注解，并设置value属性等。实测`@Component`也可以。

- 加上该注解后，即可通过`Environment`#`getProperty`获取相关的配置属性。同时也可以进行属性绑定。

- `value`的属性值支持`${}`placeholde格式，所以多文件格式支持多placeholder并以逗号分隔

- 如果配置多个文件而且文件配置属性值冲突，将以最后一个配置的为准

- 默认的`PropertySourceFactory`是PropertySourceFactory的子类`DefaultPropertySourceFactory`该子类支持`.xml`和`.properties`文件的解析。

- 如果需要支持其他文件格式例如Yaml文件解析，需要自定义解析类并实现`PropertySourceFactory`接口

  ```java
  public class YamlPropertySourceFactory implements PropertySourceFactory {
  
          @Override
          public PropertySource<?> createPropertySource(String name, EncodedResource encodedResource)
                  throws IOException {
              YamlPropertiesFactoryBean factory = new YamlPropertiesFactoryBean();
              factory.setResources(encodedResource.getResource());
              Properties properties = factory.getObject();
              return new PropertiesPropertySource(encodedResource.getResource()
                      .getFilename(), properties);
          }
  }
  ```

  那么为什么`@Component`或`@Configuration`类上加上`@PropertySource`就可以解析了呢？

  Spring-boot启动过程中依次调用。

  - `AbstractApplicationContext`#`refresh`里的`invokeBeanFactoryPostProcessors(beanFactory)`方法

    ```java
    protected void invokeBeanFactoryPostProcessors(ConfigurableListableBeanFactory beanFactory) {
    		PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(beanFactory, getBeanFactoryPostProcessors());
    
    		// Detect a LoadTimeWeaver and prepare for weaving, if found in the meantime
    		// (e.g. through an @Bean method registered by ConfigurationClassPostProcessor)
    		if (!NativeDetector.inNativeImage() && beanFactory.getTempClassLoader() == null && beanFactory.containsBean(LOAD_TIME_WEAVER_BEAN_NAME)) {
    			beanFactory.addBeanPostProcessor(new LoadTimeWeaverAwareProcessor(beanFactory));
    			beanFactory.setTempClassLoader(new ContextTypeMatchClassLoader(beanFactory.getBeanClassLoader()));
    		}
    }
    ```

  - PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(beanFactory, getBeanFactoryPostProcessors());

    ```java
    public static void invokeBeanFactoryPostProcessors(
    			ConfigurableListableBeanFactory beanFactory, List<BeanFactoryPostProcessor> beanFactoryPostProcessors) {
    
    				// 省略部分代码
    				invokeBeanDefinitionRegistryPostProcessors(currentRegistryProcessors, registry, beanFactory.getApplicationStartup());
    				currentRegistryProcessors.clear();
    			}
    			// 省略部分代码
    	}
    ```

  - invokeBeanDefinitionRegistryPostProcessors(currentRegistryProcessors, registry, beanFactory.getApplicationStartup());

    ```java
    private static void invokeBeanDefinitionRegistryPostProcessors(
    			Collection<? extends BeanDefinitionRegistryPostProcessor> postProcessors, BeanDefinitionRegistry registry, ApplicationStartup applicationStartup) {
    		
        // 这里会执行ConfigurationClassPostProcessor#postProcessBeanDefinitionRegistry
    		for (BeanDefinitionRegistryPostProcessor postProcessor : postProcessors) {
    			StartupStep postProcessBeanDefRegistry = applicationStartup.start("spring.context.beandef-registry.post-process")
    					.tag("postProcessor", postProcessor::toString);
    			postProcessor.postProcessBeanDefinitionRegistry(registry);
    			postProcessBeanDefRegistry.end();
    		}
    	}
    ```

  - ConfigurationClassPostProcessor#processConfigBeanDefinitions

  - ConfigurationClassParser#doProcessConfigurationClass

    ```java
    protected final SourceClass doProcessConfigurationClass(
    			ConfigurationClass configClass, SourceClass sourceClass, Predicate<String> filter)
    			throws IOException {
    
    		if (configClass.getMetadata().isAnnotated(Component.class.getName())) {
    			// Recursively process any member (nested) classes first
    			processMemberClasses(configClass, sourceClass, filter);
    		}
    
    		// Process any @PropertySource annotations
    		for (AnnotationAttributes propertySource : AnnotationConfigUtils.attributesForRepeatable(
    				sourceClass.getMetadata(), PropertySources.class,
    				org.springframework.context.annotation.PropertySource.class)) {
    			if (this.environment instanceof ConfigurableEnvironment) {
    				processPropertySource(propertySource);
    			}
    			else {
    				logger.info("Ignoring @PropertySource annotation on [" + sourceClass.getMetadata().getClassName() +
    						"]. Reason: Environment must implement ConfigurableEnvironment");
    			}
    		}
    
    		// Process any @ComponentScan annotations
    		Set<AnnotationAttributes> componentScans = AnnotationConfigUtils.attributesForRepeatable(
    				sourceClass.getMetadata(), ComponentScans.class, ComponentScan.class);
    		if (!componentScans.isEmpty() &&
    				!this.conditionEvaluator.shouldSkip(sourceClass.getMetadata(), ConfigurationPhase.REGISTER_BEAN)) {
    			for (AnnotationAttributes componentScan : componentScans) {
    				// The config class is annotated with @ComponentScan -> perform the scan immediately
    				Set<BeanDefinitionHolder> scannedBeanDefinitions =
    						this.componentScanParser.parse(componentScan, sourceClass.getMetadata().getClassName());
    				// Check the set of scanned definitions for any further config classes and parse recursively if needed
    				for (BeanDefinitionHolder holder : scannedBeanDefinitions) {
    					BeanDefinition bdCand = holder.getBeanDefinition().getOriginatingBeanDefinition();
    					if (bdCand == null) {
    						bdCand = holder.getBeanDefinition();
    					}
    					if (ConfigurationClassUtils.checkConfigurationClassCandidate(bdCand, this.metadataReaderFactory)) {
    						parse(bdCand.getBeanClassName(), holder.getBeanName());
    					}
    				}
    			}
    		}
    
    		// Process any @Import annotations
    		processImports(configClass, sourceClass, getImports(sourceClass), filter, true);
    
    		// Process any @ImportResource annotations
    		AnnotationAttributes importResource =
    				AnnotationConfigUtils.attributesFor(sourceClass.getMetadata(), ImportResource.class);
    		if (importResource != null) {
    			String[] resources = importResource.getStringArray("locations");
    			Class<? extends BeanDefinitionReader> readerClass = importResource.getClass("reader");
    			for (String resource : resources) {
    				String resolvedResource = this.environment.resolveRequiredPlaceholders(resource);
    				configClass.addImportedResource(resolvedResource, readerClass);
    			}
    		}
    
    		// Process individual @Bean methods
    		Set<MethodMetadata> beanMethods = retrieveBeanMethodMetadata(sourceClass);
    		for (MethodMetadata methodMetadata : beanMethods) {
    			configClass.addBeanMethod(new BeanMethod(methodMetadata, configClass));
    		}
    
    		// Process default methods on interfaces
    		processInterfaces(configClass, sourceClass);
    
    		// Process superclass, if any
    		if (sourceClass.getMetadata().hasSuperClass()) {
    			String superclass = sourceClass.getMetadata().getSuperClassName();
    			if (superclass != null && !superclass.startsWith("java") &&
    					!this.knownSuperclasses.containsKey(superclass)) {
    				this.knownSuperclasses.put(superclass, configClass);
    				// Superclass found, return its annotation metadata and recurse
    				return sourceClass.getSuperClass();
    			}
    		}
    
    		// No superclass -> processing is complete
    		return null;
    	}
    ```

  - ConfigurationClassParser#processPropertySource

    ```java
    private void processPropertySource(AnnotationAttributes propertySource) throws IOException {
    		String name = propertySource.getString("name");
    		if (!StringUtils.hasLength(name)) {
    			name = null;
    		}
    		String encoding = propertySource.getString("encoding");
    		if (!StringUtils.hasLength(encoding)) {
    			encoding = null;
    		}
    		String[] locations = propertySource.getStringArray("value");
    		Assert.isTrue(locations.length > 0, "At least one @PropertySource(value) location is required");
    		boolean ignoreResourceNotFound = propertySource.getBoolean("ignoreResourceNotFound");
    
    		Class<? extends PropertySourceFactory> factoryClass = propertySource.getClass("factory");
    		PropertySourceFactory factory = (factoryClass == PropertySourceFactory.class ?
    				DEFAULT_PROPERTY_SOURCE_FACTORY : BeanUtils.instantiateClass(factoryClass));
    
    		for (String location : locations) {
    			try {
    				String resolvedLocation = this.environment.resolveRequiredPlaceholders(location);
    				Resource resource = this.resourceLoader.getResource(resolvedLocation);
    				addPropertySource(factory.createPropertySource(name, new EncodedResource(resource, encoding)));
    			}
    			catch (IllegalArgumentException | FileNotFoundException | UnknownHostException | SocketException ex) {
    				// Placeholders not resolvable or resource not found when trying to open it
    				if (ignoreResourceNotFound) {
    					if (logger.isInfoEnabled()) {
    						logger.info("Properties location [" + location + "] not resolvable: " + ex.getMessage());
    					}
    				}
    				else {
    					throw ex;
    				}
    			}
    		}
    	}
    ```

    这里有两个比较重要的方法

    ```java
    // ApplicationServeletEnvironment
    // 这里去解析placeholder
    String resolvedLocation = this.environment.resolveRequiredPlaceholders(location);
    //org.springframework.boot.web.servlet.context.AnnotationConfigServletWebServerApplic//ationContext
    // 这里去获取resource 例如 file:xxx,classpath:xxx
    Resource resource = this.resourceLoader.getResource(resolvedLocation);
    // 把propertyResource添加到Environment中的MutablePropertySources
    addPropertySource(factory.createPropertySource(name, new EncodedResource(resource, encoding)));
    ```

    上面的流程走完就把PropertiesPropertySource添加到Environment中了，最后只需要按需获取或绑定属性就行了。

    ##  通过EnvironmentPostProcessor设置

    ### 1.编写类实现该接口

    ```java
    // 这里配置在最后执行
    @Order(Ordered.LOWEST_PRECEDENCE)
    public class MyEnvironmentPostProcessor implements EnvironmentPostProcessor {
    
        @Override
        public void postProcessEnvironment(ConfigurableEnvironment environment,
                                           SpringApplication application) {
    				
            YamlPropertiesFactoryBean yaml = new YamlPropertiesFactoryBean();
            // 通过环境变量获取files路径，这里可以配置在application.yaml中或环境变量中
            String files = environment.getProperty("files");
    				// 我们在上面讲到PropertyResource是通过ResourceLoader加载资源的
            // 包括各种路径资源file:xxx或者classpath:xxx 
            DefaultResourceLoader defaultResourceLoader = new DefaultResourceLoader();
            Resource resource = defaultResourceLoader.getResource(files);
          	
            yaml.setResources(resource);
            MutablePropertySources propertySources = environment.getPropertySources();
            propertySources.addFirst(new PropertiesPropertySource("Config", yaml.getObject()));
        }
    }
    ```

    ### 2.配置spring.factories 使MyEnvironmentPostProcessor生效

    在resource下创建**META-INF**文件夹，在**META-INF**下创建**spring.factories**，并且引入刚刚编写的**MyEnvironmentPostProcessor** 类

    ```
    org.springframework.boot.env.EnvironmentPostProcessor=MyEnvironmentPostProcessor
    ```

    这样也可以配置资源文件了。

## 其他配置加载方式

### Spring Profiles

使用Spring Profiles来加载不同环境的配置：

```yaml
# application-dev.properties
app.database.url=jdbc:mysql://localhost:3306/dev_db
app.database.username=dev_user

# application-prod.properties
app.database.url=jdbc:mysql://prod-server:3306/prod_db
app.database.username=prod_user
```

```java
@Configuration
@PropertySource({
    "classpath:application-${spring.profiles.active}.properties",
    "classpath:custom-${spring.profiles.active}.properties"
})
public class ProfileConfig {
    // 配置类
}
```

### 命令行参数和系统属性

Spring Boot支持多种外部配置源，按优先级顺序：

1. 命令行参数：`--app.name=MyApp`
2. Java系统属性：`-Dapp.name=MyApp`
3. 操作系统环境变量
4. Profile-specific配置文件
5. 主配置文件（application.properties/yml）
6. @PropertySource注解的配置
7. 默认属性

```bash
# 命令行运行
java -jar app.jar --app.database.url=jdbc:mysql://external:3306/db
```

### 外部配置文件

从外部目录加载配置：

```bash
# 指定配置目录
java -jar app.jar --spring.config.location=file:/external/config/
```

或者在application.properties中指定：

```properties
spring.config.location=file:/external/config/custom.properties,classpath:application.properties
```

### Spring Cloud Config

集成Spring Cloud Config Server：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

```properties
# bootstrap.properties
spring.cloud.config.uri=http://config-server:8888
spring.cloud.config.name=myapp
spring.profiles.active=dev
```

### 多PropertySource示例

```java
@Configuration
@PropertySources({
    @PropertySource(value = "classpath:default.properties"),
    @PropertySource(value = "file:/opt/config/override.properties",
                   ignoreResourceNotFound = true),
    @PropertySource(value = "file:/secrets/database.properties",
                   ignoreResourceNotFound = true,
                   encoding = "UTF-8")
})
public class MultiSourceConfig {
}
```

### 自定义PropertySource

实现自定义属性源：

```java
public class DatabasePropertySource extends PropertySource<Map<String, Object>> {

    public DatabasePropertySource(String name, DataSource dataSource) {
        super(name, loadPropertiesFromDatabase(dataSource));
    }

    private static Map<String, Object> loadPropertiesFromDatabase(DataSource dataSource) {
        // 从数据库加载配置
        Map<String, Object> properties = new HashMap<>();
        // ... 数据库查询逻辑
        return properties;
    }

    @Override
    public Object getProperty(String name) {
        return this.source.get(name);
    }
}
```

### 配置验证和转换

```java
@Configuration
@ConfigurationProperties(prefix = "app.security")
@Validated
public class SecurityProperties {

    @NotBlank
    private String jwtSecret;

    @Min(300)
    @Max(86400)
    private int tokenExpiration = 3600;

    @Pattern(regexp = "^(SHA256|SHA512)$")
    private String hashAlgorithm = "SHA256";

    // 自定义转换器
    private Duration sessionTimeout;

    public Duration getSessionTimeout() {
        return sessionTimeout;
    }

    public void setSessionTimeout(Duration sessionTimeout) {
        this.sessionTimeout = sessionTimeout;
    }
}
```

### 测试配置加载

```java
@SpringBootTest
@TestPropertySource(properties = {
    "app.custom.value=test",
    "app.database.url=jdbc:h2:mem:test"
})
public class ConfigTest {

    @Autowired
    private Environment environment;

    @Test
    public void testCustomProperties() {
        assertEquals("test", environment.getProperty("app.custom.value"));
    }
}
```

### 配置热更新

使用@ConfigurationProperties配合@RefreshScope：

```java
@Configuration
@ConfigurationProperties(prefix = "app.dynamic")
@RefreshScope
public class DynamicConfig {
    private String message = "default";

    // getter/setter
}
```

配合Spring Cloud Config可以实现配置热更新。

### 最佳实践

1. **使用层次化配置**：application.properties -> profile-specific -> external -> overrides

2. **敏感信息加密**：使用Spring Cloud Config的加密功能

3. **配置验证**：使用@Validated和JSR-303注解

4. **文档化配置**：为所有配置属性添加注释

5. **环境隔离**：不同环境使用不同的配置源

6. **监控配置**：记录配置加载和变更

7. **回退机制**：提供合理的默认值

### 常见问题

1. **属性不生效**：检查PropertySource优先级和覆盖规则

2. **编码问题**：设置正确的encoding属性

3. **路径解析**：使用正确的classpath:或file:前缀

4. **循环依赖**：避免配置类之间的循环引用

5. **性能影响**：大量外部配置可能影响启动时间

### 思考扩展

- 通过environmentPostProcessor的资源文件如何动态设置呢
- environmentPostProcessor的原理是啥，是怎么动态调用的
- spring中resourceLoader有哪些，是怎么动态处理不同资源的。`DefaultResourceLoader`是怎么做到的。
- 如何实现配置的版本控制和审计？
- 微服务架构中如何管理分布式配置？
- 配置加载失败时的降级策略？
