---
title: Spring IOC
categories:
  - Spring
tags:
  - Spring IOC
---


## spring容器注入组件的四种方式

- `@ComponetScan`和`@Component`（`@Componet`、`@Controller`,`@Service`,`@Repository`）使用包扫描和组件标注

  例如`@SpringbootApplication`注解

  ~~~java
  @SpringBootApplication
  源码
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.RUNTIME)
  @Documented
  @Inherited
  @SpringBootConfiguration
  @EnableAutoConfiguration
  @ComponentScan(excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
  		@Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
  public @interface SpringBootApplication
  ~~~

  默认是加载和Application类所在同一目录下的包和所有子包的配置类。如果需要额外添加其他非上述包下的组件，可以增加注解`@ComponentScan`

- `@Configuration`和`@Bean`方式

  使用场景：导入第三方包组件，或其他jar包中类。

  ~~~java
  public class User {
      //@Value("Tom")
      public String username;
   
      public User(String s) {
          this.username = s;
      }
  }
   
   
  @Configuration
  public class ImportConfig {
      @Bean
      public User user(){
          return new User("Lily");
      }
  }
   
   
  @RestController
  public class ImportDemoController {
   
      @Autowired
      private User user;
   
   
      @RequestMapping("/importDemo")
      public String demo() throws Exception {
          String s = user.username;
          return "ImportDemo@SpringBoot " + s;
      }
  }
  ~~~

  

- `@Import`给容器导入一个组件

  - `@Import`,要导入组件的类，容器会自动注册该组件，id默认是全类名

    ~~~java
    public class ImportDemo {
        public void doSomething () {
            System.out.println("ImportDemo.doSomething()");
        }
    }
     
    @Configuration
    @Import({ImportDemo.class})
    public class ImportConfig{
        @Bean
        public User user(){
            return new User("Lily");
        }
    }
     
     
    @RestController
    public class ImportDemoController {
     
        @Autowired
        private User user;
     
        @Autowired
        private ImportDemo importDemo;
     
        @RequestMapping("/importDemo")
        public String demo() throws Exception {
            importDemo.doSomething();
            
            String s = user.username;
            
     
            return "ImportDemo@SpringBoot " + s;
        }
    }
    ~~~

    

  - `ImportSelector`,返回需要导入组件的全类名数组

    ~~~java
    //自定义逻辑返回需要导入的组件
    public class MyImportSelector implements ImportSelector {
     
        //返回值，就是到导入到容器中的组件全类名
        //AnnotationMetadata:当前标注@Import注解的类的所有注解信息
        @Override
        public String[] selectImports(AnnotationMetadata importingClassMetadata) {
            // TODO Auto-generated method stub
            //importingClassMetadata
            //方法不要返回null值
            //当前类的所有注解
            Set<String> annotationTypes = importingClassMetadata.getAnnotationTypes();
            System.out.println("当前配置类的注解信息："+annotationTypes);
            //注意不能返回null,不然会报NullPointException
            return new String[]	       	{"com.adolph.springboot.bean.User01","com.adolph.springboot.bean.User02"};
        }
    }
     
    public class User01 {
    	public String username;
     
        public User01() {
            System.out.println("user01...constructor");
        }
    }
     
    public class User02 {
        public String username;
     
        public User02() {
            System.out.println("user02...constructor");
        }
    }
     
    @Configuration
    @Import({ImportDemo.class, MyImportSelector.class})
    public class ImportConfig {
     
        /**
         * 给容器中注册组件；
         * 1）、包扫描+组件标注注解（@Controller/@Service/@Repository/@Component）[自己写的类]
         * 2）、@Bean[导入的第三方包里面的组件]
         * 3）、@Import[快速给容器中导入一个组件]
         * 		1）、@Import(要导入到容器中的组件)；容器中就会自动注册这个组件，id默认是全类名
         * 		2）、ImportSelector:返回需要导入的组件的全类名数组；
         * 		3）、ImportBeanDefinitionRegistrar:手动注册bean到容器中
         * 4）、使用Spring提供的 FactoryBean（工厂Bean）;
         * 		1）、默认获取到的是工厂bean调用getObject创建的对象
         * 		2）、要获取工厂Bean本身，我们需要给id前面加一个&，&userFactoryBean
         */
     
        @Bean
        public User user(){
            return new User("Lily");
        }
    }
     
    @RestController
    public class ImportDemoController {
     
        @Autowired
        private User user;
     
        @Autowired
        private ImportDemo importDemo;
     
        @Autowired
        private User01 user01;
     
        
     
        @RequestMapping("/importDemo")
        public String demo() throws Exception {
            importDemo.doSomething();
            user01.username = "user01";
            String s = user.username;
            String s1 = user01.username;
     
            return "ImportDemo@SpringBoot " + s + " " + s1;
        }
    }
    ~~~

    

  - `ImportBeanDefinitionRegistrar`,手动注册bean到容器

    ~~~java
    public class User03 {
        public String username;
     
        public User03() {
            System.out.println("user03...constructor");
        }
    }
    
    
    public class MyImportBeanDefinitionRegistrar implements ImportBeanDefinitionRegistrar {
     
        /**
         * AnnotationMetadata：当前类的注解信息
         * BeanDefinitionRegistry:BeanDefinition注册类；
         * 		把所有需要添加到容器中的bean；调用
         * 		BeanDefinitionRegistry.registerBeanDefinition手工注册进来
         */
        @Override
        public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
     
            boolean definition = registry.containsBeanDefinition("com.paopaoedu.springboot.bean.User01");
            boolean definition2 = registry.containsBeanDefinition("com.paopaoedu.springboot.bean.User02");
            if(definition && definition2){
                //指定Bean定义信息作用域都可以在这里定义；（Bean的类型，Bean。。。）
                RootBeanDefinition beanDefinition = new RootBeanDefinition(User03.class);
                //注册一个Bean，指定bean名
                registry.registerBeanDefinition("User03", beanDefinition);
            }
        }
     
    }
    ~~~

- 使用spring提供的FactoryBean
  - 默认获取到的是工厂bean调用getObject创建的对象
  - 要获取工厂Bean本身，我们需要给id前面加一个&,&xxxFactoryBean 注意类名是X，这里就是小写的x？

~~~java
public class UserFactoryBean implements FactoryBean<User04> {
    @Override
    public User04 getObject() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("UserFactoryBean...getObject...");
        return new User04("User04");
    }
 
    @Override
    public Class<?> getObjectType() {
        // TODO Auto-generated method stub
        return User04.class;
    }
 
    //是否单例？
    //true：这个bean是单实例，在容器中保存一份
    //false：多实例，每次获取都会创建一个新的bean；
    @Override
    public boolean isSingleton() {
        // TODO Auto-generated method stub
        return true;
    }
}
 
 
public class User04 {
    public String username;
    public User04(String s) {
        String nowtime= DateUtil.now();
        username=s+" "+nowtime;
    }
}
 
 
 
@Configuration
@Import({ImportDemo.class, MyImportSelector.class, MyImportBeanDefinitionRegistrar.class})
public class ImportConfig {
 
    /**
     * 给容器中注册组件；
     * 1）、包扫描+组件标注注解（@Controller/@Service/@Repository/@Component）[自己写的类]
     * 2）、@Bean[导入的第三方包里面的组件]
     * 3）、@Import[快速给容器中导入一个组件]
     * 		1）、@Import(要导入到容器中的组件)；容器中就会自动注册这个组件，id默认是全类名
     * 		2）、ImportSelector:返回需要导入的组件的全类名数组；
     * 		3）、ImportBeanDefinitionRegistrar:手动注册bean到容器中
     * 4）、使用Spring提供的 FactoryBean（工厂Bean）;
     * 		1）、默认获取到的是工厂bean调用getObject创建的对象
     * 		2）、要获取工厂Bean本身，我们需要给id前面加一个&，&userFactoryBean
     */
    @Bean
    public UserFactoryBean userFactoryBean(){
        return new UserFactoryBean();
    }
 
    @Bean
    public User user(){
        return new User("Lily");
    }
}
 
 
@RestController
public class ImportDemoController {
 
    @Autowired
    private User user;
 
    @Autowired
    private ImportDemo importDemo;
 
    @Autowired
    private User01 user01;
 
    @Autowired
    private UserFactoryBean userFactoryBean;
 
    @RequestMapping("/importDemo")
    public String demo() throws Exception {
        importDemo.doSomething();
        user01.username = "user01";
        String s = user.username;
        String s1 = user01.username;
        String s4 = userFactoryBean.getObject().username;
 
        return "ImportDemo@SpringBoot " + s + " " + s1 + " " + s4;
    }
}
 
 
@SpringBootApplication
public class SpringBootLearningApplication {
 
    public static void main(String[] args) {
        SpringApplication.run(SpringBootLearningApplication.class, args);
 
        AnnotationConfigApplicationContext context =
                new AnnotationConfigApplicationContext("com.paopaoedu.springboot.config");
        ImportDemo importDemo = context.getBean(ImportDemo.class);
        importDemo.doSomething();
        printClassName(context);
 
        Object bean1 = context.getBean("userFactoryBean");
        Object bean2 = context.getBean("userFactoryBean");
        System.out.println(bean1 == bean2);
    }
 
    private static void printClassName(AnnotationConfigApplicationContext annotationConfigApplicationContext){
        String[] beanDefinitionNames = annotationConfigApplicationContext.getBeanDefinitionNames();
        for (int i = 0; i < beanDefinitionNames.length; i++) {
            System.out.println("匹配的类"+beanDefinitionNames[i]);
        }
    }
}
~~~
