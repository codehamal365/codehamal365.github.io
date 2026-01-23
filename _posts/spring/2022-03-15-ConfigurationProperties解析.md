---
title: SpringBoot configuration properties 解析
categories:
  - Spring
tags:
  - Spring configuration properties
---



SpringBoot configuration properties 解析

项目中我们一般通过`@Value`来获取application.yaml或application.yaml文件中配置的属性值来配置到bean对象中，一般这种对于单个或几个会比较合适。如果属性很多，这样配置很不方便。关于@Value，之前我们有讲到过，这里主要说另外一个`@ConfigurationProperties`主角，它能绑定多个值到一个对象上。

### 官方文档说明

```
Annotation for externalized configuration. Add this to a class definition or a
{@code @Bean} method in a {@code @Configuration} class if you want to bind and validate
 some external Properties (e.g. from a .properties file).
 <p>
Binding is either performed by calling setters on the annotated class or, if
{@link ConstructorBinding @ConstructorBinding} is in use, by binding to the constructor
 parameters.
 <p>
 Note that contrary to {@code @Value}, SpEL expressions are not evaluated since property
 values are externalized.
```

对于官方的文档，主要说了这几点意思。

- 外部化配置的注解。主要用在一个类上或者标注有`@Configuration`类中`@Bean`方法上
- 能够绑定外部化属性，同时也能够对属性进行校验
- 绑定的过程要么是通过类属性的setters方法，要么通过`@ConstructorBinding`绑定都构造方法的参数上
- 和`@Value`的区别就是不支持SpEL表达式

### 实例

**application.yaml**

```yaml
car:
  name: BMW
  price: 30.50
#  buyDate: 2021-10-22
```

#### 1、通过class进行进行绑定

方式一，结合`@EnableConfigurationProperties`使用

```java
@Data
@ConfigurationProperties(prefix = "car")
public class Car {
    private String name;
    private Double price;
    private Date buyDate;
}

@Configuration
@EnableConfigurationProperties(Car.class)
public class Config {
    
}
```

方式二，直接在类上标注`@Component`注解

```java
@Data
@Component
@ConfigurationProperties(prefix = "car")
public class Car {
    private String name;
    private Double price;
    private Date buyDate;
}
```

#### 2、通过@Bean方式进行绑定

```java
@Bean
@ConfigurationProperties(prefix = "car")
public Car car(){
  return new Car();
}
```

#### 3、通过@ConstructorBinding进行绑定

默认的属性绑定是通过setter方法进行，如果使用构造方法可以进行绑定。当然以前的版本都是使用`@Configuration`和`@ConfigurationProperties`进行配置的，如果使用`@ConstructorBinding`

只需要在类上加上`@ConfigurationProperties`和`@ConstructorBinding`,同时在启动类上加上`@ConfigurationPropertiesScan`即可。**这里的boot版本是2.2.0以后**

```java
@Data
@ConfigurationProperties(prefix = "car")
@ConstructorBinding
@SuppressWarnings("all")
public class Car {
    private String name;
    private Double price;
    private Date buyDate;

    public Car(String name, Double price, Date buyDate) {
        // 这里会打印出名字
        System.out.println("constructor: " + name);
        this.name = name;
        this.price = price;
        this.buyDate = buyDate;
    }

    public void setName(String name) {
        System.out.println("setter: " + name);
        this.name = name;
    }
}

@SpringBootApplication
@ConfigurationPropertiesScan
public class SpringbootTestApplication {

    @Autowired
    Car car;

    public static void main(String[] args) {
        SpringApplication.run(SpringbootTestApplication.class, args);
    }

}
```

### 原理

> Springboot verion 2.5.2

熟悉spring的应该知道，对spring bean的的生命周期流程涉及到的类有`BeanFactoryPostProcessor`和`BeanPostProcessor`。这里对`ConfigurationProperties`进行属性绑定的就是`ConfigurationPropertiesBindingPostProcessor`这个`BeanPostProcessor`,它**被框架添加到容器**，用于

解析`bean`组件上的注解`@ConfigurationProperties`,将属性源中的属性设置到`bean`组件中。

> ```
> ConfigurationPropertiesBindingPostProcessor`所在包为: `org.springframework.boot.context.properties`
> ```

#### 1、引入到容器

在idea中查看`ConfigurationPropertiesBindingPostProcessor`类的引用关系依次是：

> EnableConfigurationPropertiesRegistrar

```java
// EnableConfigurationPropertiesRegistrar
static void registerInfrastructureBeans(BeanDefinitionRegistry registry) {
		ConfigurationPropertiesBindingPostProcessor.register(registry);
		BoundConfigurationProperties.register(registry);
}
```

> EnableConfigurationProperties

```java
@Import(EnableConfigurationPropertiesRegistrar.class)
public @interface EnableConfigurationProperties {

	/**
	 * The bean name of the configuration properties validator.
	 * @since 2.2.0
	 */
	String VALIDATOR_BEAN_NAME = "configurationPropertiesValidator";

	/**
	 * Convenient way to quickly register
	 * {@link ConfigurationProperties @ConfigurationProperties} annotated beans with
	 * Spring. Standard Spring Beans will also be scanned regardless of this value.
	 * @return {@code @ConfigurationProperties} annotated beans to register
	 */
	Class<?>[] value() default {};

}
```

> spring-boot-autoconfigure-2.5.2.jar

**spring.factories**

```
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.context.ConfigurationPropertiesAutoConfiguration,\
```

>ConfigurationPropertiesAutoConfiguration

```java
@Configuration(
    proxyBeanMethods = false
)
@EnableConfigurationProperties
public class ConfigurationPropertiesAutoConfiguration {
    public ConfigurationPropertiesAutoConfiguration() {
    }
}
```

由此总结出springboot启动后会自动把`ConfigurationPropertiesBindingPostProcessor`配置ioc容器中。

#### 2、初始化自生的属性

`ConfigurationPropertiesAutoConfiguration`实现了`BeanPostProcessor`、`ApplicationContextAware`、

`InitializingBean`,在实现的方法中依次初始化了三个属性

```java
// 应用上下文
private ApplicationContext applicationContext;

// bean注册工厂，实例为AutowireCapableBeanFactory
private BeanDefinitionRegistry registry;

// 处理@ConfigurationProperties属性的具体绑定工作
private ConfigurationPropertiesBinder binder;
```

#### 3、处理属性绑定工作

大致步骤，先获取是否是**ConfigurationPropertiesBean**，然后进行具体绑定工作

```java
// 步骤1 执行BeanPostProcessor的postProcessBeforeInitialization
@Override
public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
  // 通过bean和beanName
  // 获取ConfigurationProperties类型的ConfigurationPropertiesBean
  bind(ConfigurationPropertiesBean.get(this.applicationContext, bean, beanName));
  return bean;
}

// 步骤2
private void bind(ConfigurationPropertiesBean bean) {
  // 判断是否为空和属性是否绑定
		if (bean == null || hasBoundValueObject(bean.getName())) {
			return;
		}
		Assert.state(bean.getBindMethod() == BindMethod.JAVA_BEAN, "Cannot bind @ConfigurationProperties for bean '"
				+ bean.getName() + "'. Ensure that @ConstructorBinding has not been applied to regular bean");
		try {
      // ConfigurationPropertiesBinder#bind()
			this.binder.bind(bean);
		}
		catch (Exception ex) {
			throw new ConfigurationPropertiesBindException(bean, ex);
		}
	}

private boolean hasBoundValueObject(String beanName) {
		return this.registry.containsBeanDefinition(beanName) && this.registry
				.getBeanDefinition(beanName) instanceof ConfigurationPropertiesValueObjectBeanDefinition;
}
```

**ConfigurationPropertiesBinder#bind()**

```java
BindResult<?> bind(ConfigurationPropertiesBean propertiesBean) {
  Bindable<?> target = propertiesBean.asBindTarget();
  ConfigurationProperties annotation = propertiesBean.getAnnotation();
  // 执行下面的方法
  BindHandler bindHandler = getBindHandler(target, annotation);
  // 该binder里面包含了所有的环境变量的配置数据
  // 然后利用Properties配置bean
  return getBinder().bind(annotation.prefix(), target, bindHandler);
}

private <T> BindHandler getBindHandler(Bindable<T> target, ConfigurationProperties annotation) {
  // 获取Validators
  List<Validator> validators = getValidators(target);
  BindHandler handler = getHandler();
  handler = new ConfigurationPropertiesBindHander(handler);
  if (annotation.ignoreInvalidFields()) {
    handler = new IgnoreErrorsBindHandler(handler);
  }
  if (!annotation.ignoreUnknownFields()) {
    UnboundElementsSourceFilter filter = new UnboundElementsSourceFilter();
    handler = new NoUnboundElementsBindHandler(handler, filter);
  }
  // 如果校验器不为空，则进行校验
  if (!validators.isEmpty()) {
    handler = new ValidationBindHandler(handler, validators.toArray(new Validator[0]));
  }
  for (ConfigurationPropertiesBindHandlerAdvisor advisor : getBindHandlerAdvisors()) {
    handler = advisor.apply(handler);
  }
  return handler;
}

// 对属性进行校验的验证器
private List<Validator> getValidators(Bindable<?> target) {
  List<Validator> validators = new ArrayList<>(3);
  if (this.configurationPropertiesValidator != null) {
    validators.add(this.configurationPropertiesValidator);
  }
  // 如果引入了jsr303(例如hibernate实现),而且bean属性上有@Validated
  // 则添加该校验
  if (this.jsr303Present && target.getAnnotation(Validated.class) != null) {
    validators.add(getJsr303Validator());
  }
  // 如果该对象本身不为null且对象实现了Validator接口，则把自己加入到validators列表中去
  if (target.getValue() != null && target.getValue().get() instanceof Validator) {
    validators.add((Validator) target.getValue().get());
  }
  return validators;
}
```

### 总结

- 只要被配置到容器中的类且类上标注@ConfigurationProperties都会进行属性绑定

- 属性绑定支持jsr303校验规则

- 如果该类实现了`org.springframework.validation.Validator`也可以增强校验。例如

  ```java
  @Data
  @ConfigurationProperties(prefix = "car")
  @Component("car")
  @SuppressWarnings("all")
  public class Car implements Validator {
      private String name;
      private Double price;
      private Date buyDate;
  
  
      public void setName(String name) {
          System.out.println("setter: " + name);
          this.name = name;
      }
  
      @Override
      public boolean supports(Class<?> clazz) {
          return clazz.isAssignableFrom(Car.class);
      }
  
      @Override
      public void validate(Object target, Errors errors) {
          System.out.println(target);
          ValidationUtils.rejectIfEmpty(errors, "other", "name不能为空");
          //throw new RuntimeException();
      }
  }
  ```

### 高级用法

#### 1. 嵌套对象绑定

@ConfigurationProperties 支持嵌套对象的绑定：

**application.yaml**

```yaml
app:
  server:
    host: localhost
    port: 8080
  database:
    url: jdbc:mysql://localhost:3306/mydb
    username: admin
    password: secret
    pool:
      max-size: 10
      min-size: 2
```

**Java 配置类**

```java
@Data
@ConfigurationProperties(prefix = "app")
@Component
public class AppProperties {
    private Server server;
    private Database database;

    @Data
    public static class Server {
        private String host;
        private int port;
    }

    @Data
    public static class Database {
        private String url;
        private String username;
        private String password;
        private Pool pool;

        @Data
        public static class Pool {
            private int maxSize;
            private int minSize;
        }
    }
}
```

#### 2. 集合和Map绑定

支持List、Set和Map的绑定：

**application.yaml**

```yaml
app:
  servers:
    - host: server1
      port: 8080
    - host: server2
      port: 8081
  features:
    logging: true
    caching: false
  metadata:
    version: "1.0"
    author: "dev"
```

**Java 类**

```java
@Data
@ConfigurationProperties(prefix = "app")
@Component
public class AppProperties {
    private List<Server> servers;
    private Set<String> features;
    private Map<String, String> metadata;

    @Data
    public static class Server {
        private String host;
        private int port;
    }
}
```

#### 3. 属性验证

使用JSR-303注解进行验证：

```java
@Data
@ConfigurationProperties(prefix = "app.database")
@Component
@Validated
public class DatabaseProperties {
    @NotBlank
    private String url;

    @NotBlank
    private String username;

    @NotBlank
    private String password;

    @Min(1)
    @Max(100)
    private int maxConnections = 10;

    @Pattern(regexp = "^(mysql|postgresql|oracle)$")
    private String driver = "mysql";
}
```

#### 4. 自定义转换器

对于复杂类型转换，可以实现Converter：

```java
@Configuration
public class CustomConvertersConfiguration {
    @Bean
    public Converter<String, Duration> stringToDurationConverter() {
        return new Converter<String, Duration>() {
            @Override
            public Duration convert(String source) {
                return Duration.parse(source);
            }
        };
    }
}
```

**application.yaml**

```yaml
app:
  timeout: PT30S  # ISO-8601 duration format
```

**Java**

```java
@Data
@ConfigurationProperties(prefix = "app")
@Component
public class AppProperties {
    private Duration timeout;
}
```

#### 5. 枚举绑定

```yaml
app:
  mode: DEVELOPMENT
```

```java
public enum AppMode {
    DEVELOPMENT, PRODUCTION, TEST
}

@Data
@ConfigurationProperties(prefix = "app")
@Component
public class AppProperties {
    private AppMode mode;
}
```

#### 6. 多配置文件源

@ConfigurationProperties 可以从多个属性源读取：

```java
@Configuration
@PropertySource("classpath:custom.properties")
@PropertySource("file:/external/config.properties")
public class PropertySourcesConfig {
    // ...
}
```

#### 7. 与@ConfigurationPropertiesScan结合

在Spring Boot 2.2+中，可以使用@ConfigurationPropertiesScan：

```java
@SpringBootApplication
@ConfigurationPropertiesScan("com.example.config")
public class Application {
    // 会扫描com.example.config包下的@ConfigurationProperties类
}
```

#### 8. 最佳实践

- 使用@ConfigurationPropertiesScan而不是@EnableConfigurationProperties
- 总是为集合和Map设置默认值
- 使用@Validated进行验证
- 对于复杂配置，考虑分组验证
- 使用构造函数绑定以获得不可变对象

#### 9. 测试@ConfigurationProperties

```java
@SpringBootTest
@TestPropertySource(properties = {
    "app.database.url=jdbc:test://localhost",
    "app.database.username=test"
})
public class DatabasePropertiesTest {

    @Autowired
    private DatabaseProperties properties;

    @Test
    public void testPropertiesBinding() {
        assertEquals("jdbc:test://localhost", properties.getUrl());
        assertEquals("test", properties.getUsername());
    }
}
```

### 总结扩展

@ConfigurationProperties 是Spring Boot中处理外部配置的强大工具，它提供了：

- 类型安全的配置绑定
- 嵌套对象支持
- 集合和Map支持
- 内置验证
- 自定义转换器支持
- 多属性源支持

相比@Value，@ConfigurationProperties更适合复杂配置对象的绑定。

### 思考

- 以上实例中，实体类对应的属性配置在application.yaml,那能不能从其他自定义的yaml中配置或者从配置中心获取呢？
- 配置的参数如何转换，例如时间，日期格式等等。
- 如何实现配置的热更新？
- @ConfigurationProperties与Spring Cloud Config的集成？
