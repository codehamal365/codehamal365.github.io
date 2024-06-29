---
sidebar_position: 2
---

# Cordova打包项目

如何把一个h5应用打包成android的app? 使用Cordova就是一种简单不错的办法。

当然也有其他的一些办法如使用HBuilderX这一强大的IDE工具，里面支持打包Android或ios的app,微信小程序等。或者一些第三方的打包平台，也支持把h5的应用打包成app，但有可能是收费的。

使用HBuilderX的话若开发体系都是基于HBuilder则是不错的选择，但太依赖于HBuilder。而使用Cordova打包的话，则依赖较少，比较简单。无论是网页的h5或者使用vue框架等打包的单页应用，都可以使用Cordova命令行工具快速的打包。

Apache Cordova是一个开源的移动开发框架。允许你用标准的web技术-HTML5,CSS3和JavaScript做跨平台开发。 应用在每个平台的具体执行被封装了起来，并依靠符合标准的API绑定去访问每个设备的功能。应用的实现是通过web页面，默认的本地文件名称是是index.html，这个本地文件应用CSS,JavaScript,图片，媒体文件和其他运行需要的资源。应用执行在原生应用包装的

简单来说就是：使用Cordova这个框架可以让你支持混合应用开发，把h5的web应用打包成各种平台上能跑的类似原生的应用体验。且它还提供了一些访问平台设备的插件或api,方便使用js访问到硬件功能。

## **1、为啥要用Cordova？**

混合应用开发快啊，且一次开发多端部署。BAT大厂目前采用的都是这种技术，原生开发虽然性能和体验是好，但是无法跨平台，维护和开发成本过高。Hybrid App（混合模式移动应用）兼具“Native App良好用户交互体验的优势”和“Web App跨平台开发的优势”所以很流行。使用Cordova,开发者可以用标准WEB技术HTML5、CSS3、JavaScript，来开发跨平台App且一些原生才有的一些特性，cordova提供了一些符合标准的API绑定去访问每个设备的功能。

## **2、Cordova安装**

Cordova的命令行运行在nodejs上面并且可以通过npm安装。 根据 平台具体指导安装相应平台的依赖。打开命令提示符或终端，然后键入

```shell
npm install -g cordova
```

安装完成后，使用**cordova -v**可以查看下是否安装成功。

## 3、Cordova打包android app步骤

### 第一步，创建demo模板应用。

```shell
cordova create hello com.example.hello demo 
```

(文件夹名称hello,包名com.example.hello，应用名demo)

### 第二步，在项目页面文件在www中，放入对应文件,直接把打包后dist里的文件拷贝进去替换即可。

我们使用这个[vue3-vant4-mobile](https://gitcode.com/xiangshu233/vue3-vant4-mobile/overview)项目，clone该项目(https://gitcode.com/xiangshu233/vue3-vant4-mobile.git), `pnpm build`后，将dist下面的文件拷贝到www目录。

### 第三步，命令符进入到Cordova项目中，添加browser平台

```shell
cordova platform add browser
```

### 第四步，浏览器运行

```shell
cordova run browser
```

确保在流浪器中能够正常运行。

### 第五步，打包apk安卓运行，生成的安卓包

```shell
cordova platform add android 
```

>(前提条件：电脑上已有jdk和android sdk等环境)

### 第六步骤，开始生成android的apk

```shell
cordova build android
```

打包完成后会在`platforms/android/app/build/outputs/apk/debug`生成 `app-debug.apk`。安装到手机即可查看效果。

最后打包完成后可能遇到的跨域问题，缓存问题，网上都有解决方案，可自行百度。比如跳转路由增加时间戳，可以有效解决缓存问题，设置代理，解决跨域问题。


## 结尾

更多关于cordova的命令和说明请查看官方文档，https://cordova.apache.org/docs/en/latest/

