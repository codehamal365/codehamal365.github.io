---
title: Spring WebSocket
categories:
  - Spring
tags:
  - Spring WebSocket
---


WebSocket 的 6 种集成方式
================================

介绍
==

`WebSocket`的各种集成方式目前主要有以下几种

*   `Javax`
*   `WebMVC`
*   `WebFlux`
*   `Java-WebSocket`
*   `SocketIO`
*   `Netty`

今天主要介绍一下前3种方式，毕竟现在的主流框架还是`Spring Boot`

而后3种其实和`Spring Boot`并不强行绑定，基于`Java`就可以支持，不过我也会对后3种做个简单的介绍，大家先混个眼熟就行了

那么接下来我们就来讲讲前3种方式（`Javax`，`WebMVC`，`WebFlux`）在`Spring Boot`中的服务端和客户端配置（客户端配置也超重要的有木有，平时用不到，用到了却基本找不到文档，这也太绝望了）

Javax
=====

在`java`的扩展包`javax.websocket`中就定义了一套`WebSocket`的接口规范

服务端
---

一般使用注解的方式来进行配置

### 第一步

java

复制代码

```java
@Component
@ServerEndpoint("/websocket/{type}")
public class JavaxWebSocketServerEndpoint {

    @OnOpen
    public void onOpen(Session session, EndpointConfig config,
                       @PathParam(value = "type") String type) {
        //连接建立
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {
        //连接关闭
    }

    @OnMessage
    public void onMessage(Session session, String message) {
        //接收文本信息
    }

    @OnMessage
    public void onMessage(Session session, PongMessage message) {
        //接收pong信息
    }

    @OnMessage
    public void onMessage(Session session, ByteBuffer message) {
        //接收二进制信息，也可以用byte[]接收
    }

    @OnError
    public void onError(Session session, Throwable e) {
        //异常处理
    }
}
```

我们在类上添加`@ServerEndpoint`注解来表示这是一个服务端点，同时可以在注解中配置路径，这个路径可以配置成动态的，使用`{}`包起来就可以了

`@OnOpen`用来标记对应的方法作为客户端连接上来之后的回调，`Session`就相当于和客户端的连接啦，我们可以把它缓存起来用于发送消息；通过`@PathParam`注解就可以获得动态路径中对应值了

`@OnClose`用来标记对应的方法作为客户端断开连接之后的回调，我们可以在这个方法中移除对应`Session`的缓存，同时可以接受一个`CloseReason`的参数用于获取关闭原因

`@OnMessage`用来标记对应的方法作为接收到消息之后的回调，我们可以接受文本消息，二进制消息和`pong`消息

`@OnError`用来标记对应的方法作为抛出异常之后的回调，可以获得对应的`Session`和异常对象

### 第二步


```maven
 <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

```java
@Configuration(proxyBeanMethods = false)
public class JavaxWebSocketConfiguration {

    @Bean
    public ServerEndpointExporter serverEndpointExporter() {
        return new ServerEndpointExporter();
    }
}
```

依赖`Spring`的`WebSocket`模块，手动注入`ServerEndpointExporter`就可以了

需要注意`ServerEndpointExporter`是`Spring`中的类，算是`Spring`为了支持`javax.websocket`的原生用法所提供的支持类

### 冷知识

`javax.websocket`库中定义了`PongMessage`而没有`PingMessage`

通过我的测试发现基本上所有的`WebSocket`包括前端`js`自带的，都实现了自动回复；也就是说当接收到一个`ping`消息之后，是会自动回应一个`pong`消息，所以没有必要再自己接受`ping`消息来处理了，即我们不会接受到`ping`消息

当然我上面讲的`ping`和`pong`都是需要使用框架提供的`api`，如果是我们自己通过`Message`来自定义心跳数据的话是没有任何的处理的，下面是对应的`api`

```java
//发送ping
session.getAsyncRemote().sendPing(ByteBuffer buffer);

//发送pong
session.getAsyncRemote().sendPong(ByteBuffer buffer);
```

然后我又发现`js`自带的`WebSocket`是没有发送`ping`的`api`的，所以是不是可以猜想当初就是约定服务端发送`ping`，客户端回复`pong`

客户端
---

客户端也是使用注解配置

### 第一步

```java
@ClientEndpoint
public class JavaxWebSocketClientEndpoint {

    @OnOpen
    public void onOpen(Session session) {
        //连接建立
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {
        //连接关闭
    }

    @OnMessage
    public void onMessage(Session session, String message) {
        //接收文本消息
    }

    @OnMessage
    public void onMessage(Session session, PongMessage message) {
        //接收pong消息
    }

    @OnMessage
    public void onMessage(Session session, ByteBuffer message) {
        //接收二进制消息
    }

    @OnError
    public void onError(Session session, Throwable e) {
        //异常处理
    }
}
```

客户端使用`@ClientEndpoint`来标记，其他的`@OnOpen`，`@OnClose`，`@OnMessage`，`@OnError`和服务端一模一样

### 第二步

```java

WebSocketContainer container = ContainerProvider.getWebSocketContainer();
Session session = container.connectToServer(JavaxWebSocketClientEndpoint.class, uri);
```
我们可以通过`ContainerProvider`来获得一个`WebSocketContainer`，然后调用`connectToServer`方法将我们的客户端类和连接的`uri`传入就行了

### 冷知识

通过`ContainerProvider#getWebSocketContainer`获得`WebSocketContainer`其实是基于`SPI`实现的

在`Spring`的环境中我更推荐大家使用`ServletContextAware`来获得，代码如下

```java
@Component
public class JavaxWebSocketContainer implements ServletContextAware {

    private volatile WebSocketContainer container;

    public WebSocketContainer getContainer() {
        if (container == null) {
            synchronized (this) {
                if (container == null) {
                    container = ContainerProvider.getWebSocketContainer();
                }
            }
        }
        return container;
    }

    @Override
    public void setServletContext(@NonNull ServletContext servletContext) {
        if (container == null) {
            container = (WebSocketContainer) servletContext
                .getAttribute("javax.websocket.server.ServerContainer");
        }
    }
}

```

发消息
---
```java
Session session = ...

//发送文本消息
session.getAsyncRemote().sendText(String message);

//发送二进制消息
session.getAsyncRemote().sendBinary(ByteBuffer message);

//发送对象消息，会尝试使用Encoder编码
session.getAsyncRemote().sendObject(Object message);

//发送ping
session.getAsyncRemote().sendPing(ByteBuffer buffer);

//发送pong
session.getAsyncRemote().sendPong(ByteBuffer buffer);

```

WebMVC
======

依赖肯定是必不可少的

```maven
 <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

服务端
---

### 第一步

```java
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;

public class ServletWebSocketServerHandler implements WebSocketHandler {

    @Override
    public void afterConnectionEstablished(@NonNull WebSocketSession session) throws Exception {
        //连接建立
    }

    @Override
    public void handleMessage(@NonNull WebSocketSession session, @NonNull WebSocketMessage<?> message) throws Exception {
        //接收消息
    }

    @Override
    public void handleTransportError(@NonNull WebSocketSession session, @NonNull Throwable exception) throws Exception {
        //异常处理
    }

    @Override
    public void afterConnectionClosed(@NonNull WebSocketSession session, @NonNull CloseStatus closeStatus) throws Exception {
        //连接关闭
    }

    @Override
    public boolean supportsPartialMessages() {
        //是否支持接收不完整的消息
        return false;
    }
}

```

我们实现一个`WebSocketHandler`来处理`WebSocket`的连接，关闭，消息和异常

### 第二步

```java
@Configuration
@EnableWebSocket
public class ServletWebSocketServerConfigurer implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(@NonNull WebSocketHandlerRegistry registry) {
        registry
            //添加处理器到对应的路径
            .addHandler(new ServletWebSocketServerHandler(), "/websocket")
            .setAllowedOrigins("*");
    }
}
```

首先需要添加`@EnableWebSocket`来启用`WebSocket`

然后实现`WebSocketConfigurer`来注册`WebSocket`路径以及对应的`WebSocketHandler`

### 握手拦截

提供了`HandshakeInterceptor`来拦截握手

```java
@Configuration
@EnableWebSocket
public class ServletWebSocketServerConfigurer implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(@NonNull WebSocketHandlerRegistry registry) {
        registry
            //添加处理器到对应的路径
            .addHandler(new ServletWebSocketServerHandler(), "/websocket")
            //添加握手拦截器
            .addInterceptors(new ServletWebSocketHandshakeInterceptor())
            .setAllowedOrigins("*");
    }
    
    public static class ServletWebSocketHandshakeInterceptor implements HandshakeInterceptor {

        @Override
        public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {
            //握手之前
            //继续握手返回true, 中断握手返回false
            return false;
        }

        @Override
        public void afterHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Exception exception) {
            //握手之后
        }
    }
}

```
            

### 冷知识

我在集成的时候发现这种方式没办法动态匹配路径，它的路径就是固定的，没办法使用如`/websocket/**`这样的通配符

我在研究了一下之后发现可以在`UrlPathHelper`上做点文章

```java
@Configuration
@EnableWebSocket
public class ServletWebSocketServerConfigurer implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(@NonNull WebSocketHandlerRegistry registry) {
        if (registry instanceof ServletWebSocketHandlerRegistry) {
            //替换UrlPathHelper
            ((ServletWebSocketHandlerRegistry) registry)
                .setUrlPathHelper(new PrefixUrlPathHelper("/websocket"));
        }

        registry
            //添加处理器到对应的路径
            .addHandler(new ServletWebSocketServerHandler(), "/websocket/**")
            .setAllowedOrigins("*");
    }
    
    public class PrefixUrlPathHelper extends UrlPathHelper {

        private String prefix;

        @Override
        public @NonNull String resolveAndCacheLookupPath(@NonNull HttpServletRequest request) {
            //获得原本的Path
            String path = super.resolveAndCacheLookupPath(request);
            //如果是指定前缀就返回对应的通配路径
            if (path.startsWith(prefix)) {
                return prefix + "/**";
            }
            return path;
        }
    }
}

```


因为它内部实际上就是用一个`Map<String, WebSocketHandler>`来存的，所以没有办法用通配符

主要是有现成的`AntPathMatcher`实现通配应该不麻烦才对啊

客户端
---

### 第一步

```java
public class ServletWebSocketClientHandler implements WebSocketHandler {

    @Override
    public void afterConnectionEstablished(@NonNull WebSocketSession session) throws Exception {
        //连接建立
    }

    @Override
    public void handleMessage(@NonNull WebSocketSession session, @NonNull WebSocketMessage<?> message) throws Exception {
        //接收消息
    }

    @Override
    public void handleTransportError(@NonNull WebSocketSession session, @NonNull Throwable exception) throws Exception {
        //异常处理
    }

    @Override
    public void afterConnectionClosed(@NonNull WebSocketSession session, @NonNull CloseStatus closeStatus) throws Exception {
        //连接关闭
    }

    @Override
    public boolean supportsPartialMessages() {
        //是否支持接收不完整的消息
        return false;
    }
}

```

和服务端一样我们需要先实现一个`WebSocketHandler`来处理`WebSocket`的连接，关闭，消息和异常

### 第二步

```java
WebSocketClient client = new StandardWebSocketClient();
WebSocketHandler handler = new ServletWebSocketClientHandler();
WebSocketConnectionManager manager = new WebSocketConnectionManager(client, handler, uri);
manager.start();
```

首先我们需要先`new`一个`StandardWebSocketClient`，可以传入一个`WebSocketContainer`参数，获得该对象的方式我之前已经介绍过了，这边就先略过

然后`new`一个`WebSocketConnectionManager`传入`WebSocketClient`，`WebSocketHandler`还有路径`uri`

最后调用一下`WebSocketConnectionManager`的`start`方法就可以啦

### 冷知识

这里如果大家去看`WebSocketClient`的实现类就会发现有`StandardWebSocketClient`还有`JettyWebSocketClient`等等，所以大家可以根据自身项目所使用的容器来选择不同的`WebSocketClient`实现类

这里给大家贴一小段`Spring`适配不同容器`WebSocket`的代码

```java
public abstract class AbstractHandshakeHandler implements HandshakeHandler, Lifecycle {

    private static final boolean tomcatWsPresent;

    private static final boolean jettyWsPresent;

    private static final boolean jetty10WsPresent;

    private static final boolean undertowWsPresent;

    private static final boolean glassfishWsPresent;

    private static final boolean weblogicWsPresent;

    private static final boolean websphereWsPresent;

    static {
        ClassLoader classLoader = AbstractHandshakeHandler.class.getClassLoader();
        tomcatWsPresent = ClassUtils.isPresent(
            "org.apache.tomcat.websocket.server.WsHttpUpgradeHandler", classLoader);
        jetty10WsPresent = ClassUtils.isPresent(
            "org.eclipse.jetty.websocket.server.JettyWebSocketServerContainer", classLoader);
        jettyWsPresent = ClassUtils.isPresent(
            "org.eclipse.jetty.websocket.server.WebSocketServerFactory", classLoader);
        undertowWsPresent = ClassUtils.isPresent(
            "io.undertow.websockets.jsr.ServerWebSocketContainer", classLoader);
        glassfishWsPresent = ClassUtils.isPresent(
            "org.glassfish.tyrus.servlet.TyrusHttpUpgradeHandler", classLoader);
        weblogicWsPresent = ClassUtils.isPresent(
            "weblogic.websocket.tyrus.TyrusServletWriter", classLoader);
        websphereWsPresent = ClassUtils.isPresent(
            "com.ibm.websphere.wsoc.WsWsocServerContainer", classLoader);
    }
}

```

发消息
---

```java
import org.springframework.web.socket.*;

WebSocketSession session = ...

//发送文本消息
session.sendMessage(new TextMessage(CharSequence message);

//发送二进制消息
session.sendMessage(new BinaryMessage(ByteBuffer message));

//发送ping
session.sendMessage(new PingMessage(ByteBuffer message));

//发送pong
session.sendMessage(new PongMessage(ByteBuffer message));

```

WebFlux
=======

`WebFlux`的`WebSocket`不需要额外的依赖包

服务端
---

### 第一步
```java

import org.springframework.web.reactive.socket.WebSocketHandler;
import org.springframework.web.reactive.socket.WebSocketSession;

public class ReactiveWebSocketServerHandler implements WebSocketHandler {

    @NonNull
    @Override
    public Mono<Void> handle(WebSocketSession session) {
        Mono<Void> send = session.send(Flux.create(sink -> {
            //可以持有sink对象在任意时候调用next发送消息
            sink.next(WebSocketMessage message);
        })).doOnError(it -> {
            //异常处理
        });

        Mono<Void> receive = session.receive()
                .doOnNext(it -> {
                    //接收消息
                })
                .doOnError(it -> {
                    //异常处理
                })
                .then();

        @SuppressWarnings("all")
        Disposable disposable = session.closeStatus()
                .doOnError(it -> {
                    //异常处理
                })
                .subscribe(it -> {
                    //连接关闭
                });

        return Mono.zip(send, receive).then();
    }
}

```

首先需要注意这里的`WebSocketHandler`和`WebSocketSession`是`reactive`包下的

通过`WebSocketSession#send`方法来持有一个`FluxSink<WebSocketMessage>`来用于发送消息

通过`WebSocketSession#receive`来订阅消息

通过`WebSocketSession#closeStatus`来订阅连接关闭事件

### 第二步

```java
@Component
public class ReactiveWebSocketServerHandlerMapping extends SimpleUrlHandlerMapping {

    public ReactiveWebSocketServerHandlerMapping() {
        Map<String, WebSocketHandler> map = new HashMap<>();
        map.put("/websocket/**", new ReactiveWebSocketServerHandler());
        setUrlMap(map);
        setOrder(100);
    }
}

```
注册一个`HandlerMapping`同时配置路径和对应的`WebSocketHandler`

### 第三步

```java
@Configuration(proxyBeanMethods = false)
public class ReactiveWebSocketConfiguration {

    @Bean
    public WebSocketHandlerAdapter webSocketHandlerAdapter() {
        return new WebSocketHandlerAdapter();
    }
}

```

注入`WebSocketHandlerAdapter`

### 冷知识

我们自定义的`HandlerMapping`需要设置`order`，如果不设置，默认为`Ordered.LOWEST_PRECEDENCE`，会导致这个`HandlerMapping`被放在最后，当有客户端连接上来时会被其他的`HandlerMapping`优先匹配上而连接失败

客户端
---

### 第一步

```java
public class ReactiveWebSocketClientHandler implements WebSocketHandler {

    @NonNull
    @Override
    public Mono<Void> handle(WebSocketSession session) {
        Mono<Void> send = session.send(Flux.create(sink -> {
            //可以持有sink对象在任意时候调用next发送消息
            sink.next(WebSocketMessage message);
        })).doOnError(it -> {
            //处理异常
        });

        Mono<Void> receive = session.receive()
                .doOnNext(it -> {
                    //接收消息
                })
                .doOnError(it -> {
                    //异常处理
                })
                .then();

        @SuppressWarnings("all")
        Disposable disposable = session.closeStatus()
                .doOnError(it -> {
                    //异常处理
                })
                .subscribe(it -> {
                    //连接关闭
                });

        return Mono.zip(send, receive).then();
    }
}

```

客户端`WebSocketHandler`的写法和服务端的一样

### 第二步

```java
import org.springframework.web.reactive.socket.client.WebSocketClient;

WebSocketClient client = ReactorNettyWebSocketClient();
WebSocketHandler handler = new ReactiveWebSocketClientHandler();
client.execute(uri, handler).subscribe();

```

首先我们需要先`new`一个`ReactorNettyWebSocketClient`

然后调用一下`WebSocketClient`的`execute`方法传入路径`uri`和`WebSocketHandler`并继续调用`subscribe`方法就行啦

### 冷知识

和`WebMVC`中的`WebSocketClient`一样，`Reactive`包中的`WebSocketClient`也有很多实现类，比如`ReactorNettyWebSocketClient`，`JettyWebSocketClient`，`UndertowWebSocketClient`，`TomcatWebSocketClient`等等，也是需要大家基于自身项目的容器使用不同的实现类

这里也给大家贴一小段`Reactive`适配不同容器`WebSocket`的代码

```java
public class HandshakeWebSocketService implements WebSocketService, Lifecycle {

    private static final boolean tomcatPresent;

    private static final boolean jettyPresent;

    private static final boolean jetty10Present;

    private static final boolean undertowPresent;

    private static final boolean reactorNettyPresent;

    static {
        ClassLoader loader = HandshakeWebSocketService.class.getClassLoader();
        tomcatPresent = ClassUtils.isPresent("org.apache.tomcat.websocket.server.WsHttpUpgradeHandler", loader);
        jettyPresent = ClassUtils.isPresent("org.eclipse.jetty.websocket.server.WebSocketServerFactory", loader);
        jetty10Present = ClassUtils.isPresent("org.eclipse.jetty.websocket.server.JettyWebSocketServerContainer", loader);
        undertowPresent = ClassUtils.isPresent("io.undertow.websockets.WebSocketProtocolHandshakeHandler", loader);
        reactorNettyPresent = ClassUtils.isPresent("reactor.netty.http.server.HttpServerResponse", loader);
    }
}

```

发消息
---

我们需要使用在`WebSocketHandler`中获得的`FluxSink<WebSocketMessage>`来发送消息

```java
import org.springframework.web.reactive.socket.CloseStatus;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;

public class ReactiveWebSocket {

    private final WebSocketSession session;

    private final FluxSink<WebSocketMessage> sender;

    public ReactiveWebSocket(WebSocketSession session, FluxSink<WebSocketMessage> sender) {
        this.session = session;
        this.sender = sender;
    }

    public String getId() {
        return session.getId();
    }

    public URI getUri() {
        return session.getHandshakeInfo().getUri();
    }

    public void send(Object message) {
        if (message instanceof WebSocketMessage) {
            sender.next((WebSocketMessage) message);
        } else if (message instanceof String) {
            //发送文本消息
            sender.next(session.textMessage((String) message));
        } else if (message instanceof DataBuffer) {
            //发送二进制消息
            sender.next(session.binaryMessage(factory -> (DataBuffer) message));
        } else if (message instanceof ByteBuffer) {
            ////发送二进制消息
            sender.next(session.binaryMessage(factory -> factory.wrap((ByteBuffer) message)));
        } else if (message instanceof byte[]) {
            ////发送二进制消息
            sender.next(session.binaryMessage(factory -> factory.wrap((byte[]) message)));
        } else {
            throw new IllegalArgumentException("Message type not match");
        }
    }

    public void ping() {
        //发送ping
        sender.next(session.pingMessage(factory -> factory.wrap(ByteBuffer.allocate(0))));
    }

    public void pong() {
        //发送pong
        sender.next(session.pongMessage(factory -> factory.wrap(ByteBuffer.allocate(0))));
    }

    public void close(CloseStatus reason) {
        sender.complete();
        session.close(reason).subscribe();
    }
}


```

Java-WebSocket
==============

这是一个纯`java`的第三方库，专门用于实现`WebSocket`

[Github](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FTooTallNate%2FJava-WebSocket "https://github.com/TooTallNate/Java-WebSocket")上已经有很详细的使用教程了，现在有`9k+`的`Star`

SocketIO
========

该库使用的协议是经过自己封装的，支持很多的语言，提供了统一的接口，所以需要使用它提供的`Server`和`Client`来连接，如[socket.io-server-java](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fsocketio%2Fsocket.io-server-java "https://github.com/socketio/socket.io-server-java")和[socket.io-client-java](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fsocketio%2Fsocket.io-client-java "https://github.com/socketio/socket.io-client-java")

这个库我了解下来主要用于实时聊天等场景，所以如果只是普通的`WebSocket`功能就有点大材小用了

[Github](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fsocketio "https://github.com/socketio")上也有非常详细的使用文档，大家如果有兴趣可以研究一下

Netty
=====

这个大家应该都比较熟悉了，就算没用过肯定也听过

网上的文档和示例也非常多，我这里就不介绍有的没的了，[Github传送门](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fnetty%2Fnetty "https://github.com/netty/netty")
