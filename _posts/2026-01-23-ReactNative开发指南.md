---
title: "ReactNative开发指南"
date: 2026-01-23
categories: reactnative
tags: reactnative development guide
---


# React Native 开发指南

## 目录
1. [React Native 开发流程](#1-react-native-开发流程)
2. [部署与测试](#2-部署与测试)
3. [打包与发布](#3-打包与发布)

---

## 1. React Native 开发流程

### 1.1 创建 React Native 工程

#### 使用 React Native CLI（推荐）
```bash
# 创建新项目（推荐使用最新版本）
npx @react-native-community/cli init MyApp

# 或者指定版本
npx @react-native-community/cli init MyApp --version 0.72.0
```

#### 使用 Expo（适合初学者）
```bash
# 创建新项目
npx create-expo-app MyApp

# 进入项目目录
cd MyApp

# 启动开发服务器
npx expo start
```

#### 项目结构说明
```
MyApp/
├── android/          # Android 原生代码
├── ios/              # iOS 原生代码
├── src/              # 源代码目录（推荐）
│   ├── components/   # 组件
│   ├── screens/      # 页面
│   ├── utils/        # 工具函数
│   └── navigation/   # 路由导航
├── App.tsx          # 入口文件
├── package.json
└── metro.config.js   # 打包配置
```

### 1.2 创建 View（视图）

#### 基础 View 组件
{% raw %}
```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const MyView = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Hello React Native</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  text: {
    fontSize: 18,
    color: '#333',
  },
});

export default MyView;
```
{% endraw %}

#### 常用布局属性
{% raw %}
```tsx
// Flexbox 布局
<View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
  <View style={{ width: 100, height: 100, backgroundColor: 'red' }} />
  <View style={{ width: 100, height: 100, backgroundColor: 'blue' }} />
</View>

// 边距和内边距
<View style={{ margin: 10, padding: 20, borderWidth: 1, borderColor: '#ccc' }}>
  <Text>Content</Text>
</View>

// 圆角和阴影
<View style={{ borderRadius: 10, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.25 }}>
  <Text>Card</Text>
</View>
```
{% endraw %}

### 1.3 常用组件

#### 核心组件库
```tsx
import {
  // 基础组件
  View,           // 容器组件
  Text,           // 文本组件
  Image,          // 图片组件
  ScrollView,     // 可滚动容器
  FlatList,       // 高性能列表
  SectionList,    // 分组列表

  // 输入组件
  TextInput,      // 输入框
  Button,         // 按钮
  TouchableOpacity, // 可点击容器
  TouchableHighlight,

  // 导航组件
  NavigatorIOS,   // iOS 导航（已弃用）

  // 其他组件
  ActivityIndicator, // 加载指示器
  Switch,         // 开关
  Slider,         // 滑块
  Picker,         // 选择器（已弃用）
  Alert,          // 弹窗
  Modal,          // 模态框
} from 'react-native';
```

#### 常用第三方组件

**UI 组件库**
```bash
# React Native Paper (Material Design)
npm install react-native-paper

# React Native Elements
npm install react-native-elements

# NativeBase (推荐使用最新版本)
npm install native-base

# UI Kitten
npm install @ui-kitten/components @ui-kitten/eva-icons
```

**导航组件**
```bash
# React Navigation (推荐)
npm install @react-navigation/native
npm install react-native-screens react-native-safe-area-context

# Stack Navigator
npm install @react-navigation/stack
npm install react-native-gesture-handler

# Tab Navigator
npm install @react-navigation/bottom-tabs

# Drawer Navigator
npm install @react-navigation/drawer
```

**表单组件**
```bash
# React Hook Form
npm install react-hook-form

# Formik
npm install formik yup
```

**图片组件**
```bash
# React Native Fast Image
npm install react-native-fast-image

# React Native Image Picker
npm install react-native-image-picker
```

**状态管理**
```bash
# Redux Toolkit
npm install @reduxjs/toolkit react-redux

# Zustand (轻量级)
npm install zustand

# MobX
npm install mobx mobx-react-lite
```

### 1.4 开发工具与调试

#### 开发工具
```bash
# React Native Debugger (推荐)
# 下载: https://github.com/jhen0409/react-native-debugger/releases

# Flipper (Facebook 官方)
# 下载: https://fbflipper.com/

# VS Code 扩展
# - React Native Tools
# - ESLint
# - Prettier
```

#### 调试命令
```bash
# 启动开发服务器
npx react-native start

# Android 运行
npx react-native run-android

# iOS 运行
npx react-native run-ios

# 清除缓存
npx react-native start --reset-cache

# 重新构建
cd android && ./gradlew clean && cd ..
```

### 1.5 重要文档链接

#### 官方文档
- [React Native 官方文档](https://reactnative.dev/docs/getting-started)
- [React Native 中文文档](https://reactnative.cn/)
- [Expo 文档](https://docs.expo.dev/)

#### 学习资源
- [React Native School](https://reactnativeschool.com/)
- [React Native Tutorial](https://www.youtube.com/playlist?list=PL4cUxeGkcC9ixPU-QkScoRBVxtPPzVjrQ)
- [React Native Navigation](https://reactnavigation.org/)

#### 组件文档
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [React Native Elements](https://reactnativeelements.com/docs)
- [React Navigation](https://reactnavigation.org/docs/getting-started)

#### 工具文档
- [Metro Bundler](https://facebook.github.io/metro/)
- [Fastlane](https://docs.fastlane.tools/)

---

## 2. 部署与测试

### 2.1 真机测试准备

#### Android 真机测试

**1. 开启开发者选项**
```
设置 → 关于手机 → 连续点击"版本号"7次 → 开启开发者选项
```

**2. 开启 USB 调试**
```
设置 → 开发者选项 → USB调试 → 开启
```

**3. 连接设备**
```bash
# 检查设备是否连接
adb devices

# 应该显示类似：
# List of devices attached
# 1234567890ABCDEF    device
```

**4. 运行应用**
```bash
# 确保设备已连接
adb devices

# 运行应用到真机
npx react-native run-android

# 指定设备运行（多设备时）
adb -s <device_id> react-native run-android
```

### 2.2 ADB 数据线部署

#### ADB 常用命令
```bash
# 查看已连接设备
adb devices

# 安装 APK
adb install app-release.apk

# 卸载应用
adb uninstall com.yourapp.package

# 查看应用日志
adb logcat | grep "ReactNative"

# 清除应用数据
adb shell pm clear com.yourapp.package

# 重启 ADB 服务
adb kill-server
adb start-server

# 端口转发（用于调试）
adb reverse tcp:8081 tcp:8081
adb reverse tcp:8097 tcp:8097
```

#### 常见问题解决
```bash
# 问题：设备未识别
# 解决方案：
adb kill-server
adb start-server
adb devices

# 问题：端口占用
# 解决方案：
adb reverse --remove tcp:8081
adb reverse tcp:8081 tcp:8081

# 问题：应用崩溃
# 查看日志：
adb logcat | grep "ReactNative"
```

### 2.3 ADB WiFi 部署

#### 前提条件
- 手机和电脑在同一 WiFi 网络
- 手机开启 USB 调试（首次需要）

#### 配置步骤

**1. 首次连接（需要 USB 数据线）**
```bash
# 连接设备到 USB
adb devices

# 获取设备 IP 地址（在手机设置中查看）
# 或者使用命令：
adb shell ip addr show wlan0

# 连接到 WiFi（假设设备 IP 为 192.168.1.100）
adb tcpip 5555
adb connect 192.168.1.100:5555

# 断开 USB 连接
adb disconnect
```

**2. 后续 WiFi 连接**
```bash
# 直接连接（无需 USB）
adb connect 192.168.1.100:5555

# 查看连接状态
adb devices

# 断开连接
adb disconnect 192.168.1.100:5555
```

**3. 运行应用到 WiFi 设备**
```bash
# 确保 WiFi 连接正常
adb devices

# 运行应用
npx react-native run-android

# 或者指定设备
adb -s 192.168.1.100:5555 react-native run-android
```

#### WiFi 部署脚本
创建 `scripts/run-wifi.sh`：
```bash
#!/bin/bash

# WiFi 部署脚本
DEVICE_IP="192.168.1.100"  # 修改为你的设备 IP

echo "连接到设备 $DEVICE_IP..."
adb connect $DEVICE_IP:5555

echo "检查设备连接..."
adb devices

echo "运行应用到设备..."
npx react-native run-android

echo "完成！"
```

使用方法：
```bash
chmod +x scripts/run-wifi.sh
./scripts/run-wifi.sh
```

### 2.4 开发服务器配置

#### Metro 配置
`metro.config.js`:
```javascript
const { getDefaultConfig } = require('metro-config');

module.exports = (async () => {
  const {
    resolver: { sourceExts, assetExts },
  } = await getDefaultConfig();

  return {
    transformer: {
      babelTransformerPath: require.resolve('react-native-svg-transformer'),
    },
    resolver: {
      assetExts: assetExts.filter(ext => ext !== 'svg'),
      sourceExts: [...sourceExts, 'svg'],
    },
  };
})();
```

#### 环境变量配置
创建 `.env` 文件：
```env
API_URL=https://api.example.com
APP_NAME=MyApp
```

使用 `react-native-config`:
```bash
npm install react-native-config
```

在代码中使用：
```javascript
import Config from 'react-native-config';

const apiUrl = Config.API_URL;
```

### 2.5 测试策略

#### 单元测试
```bash
# 安装 Jest
npm install --save-dev jest @types/jest

# 配置 package.json
{
  "scripts": {
    "test": "jest"
  },
  "jest": {
    "preset": "react-native",
    "setupFilesAfterEnv": ["@testing-library/jest-native/extend-expect"]
  }
}
```

#### 组件测试
```bash
npm install --save-dev @testing-library/react-native @testing-library/jest-native
```

{% raw %}
```javascript
// __tests__/MyComponent.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import MyComponent from '../src/components/MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    const { getByText } = render(<MyComponent />);
    expect(getByText('Hello')).toBeTruthy();
  });

  it('handles button press', () => {
    const onPress = jest.fn();
    const { getByText } = render(<MyComponent onPress={onPress} />);
    fireEvent.press(getByText('Press me'));
    expect(onPress).toHaveBeenCalled();
  });
});
```
{% endraw %}

#### E2E 测试
```bash
# Detox (推荐)
npm install --save-dev detox @types/detox
```

---

## 3. 打包与发布

### 3.1 Android 打包准备

#### 1. 生成签名密钥
```bash
# 进入 android 目录
cd android

# 生成密钥库（.jks 文件）
keytool -genkeypair -v \
  -keystore my-release-key.keystore \
  -alias my-key-alias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# 保存密钥信息：
# - 密钥库密码
# - 密钥别名
# - 密钥密码
```

#### 2. 配置 gradle
编辑 `android/app/build.gradle`:
```gradle
android {
    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_RELEASE_STORE_FILE')) {
                storeFile file(MYAPP_RELEASE_STORE_FILE)
                storePassword MYAPP_RELEASE_STORE_PASSWORD
                keyAlias MYAPP_RELEASE_KEY_ALIAS
                keyPassword MYAPP_RELEASE_KEY_PASSWORD
            }
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### 3. 配置环境变量
创建 `android/gradle.properties`:
```properties
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_STORE_PASSWORD=your_password
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_KEY_PASSWORD=your_password
```

### 3.2 手动打包步骤

#### 1. 清理项目
```bash
cd android
./gradlew clean
cd ..
```

#### 2. 生成 Release APK
```bash
# 生成 APK
cd android
./gradlew assembleRelease

# 或者生成 App Bundle (AAB) - Google Play 推荐
./gradlew bundleRelease

# 查看生成的文件
ls app/build/outputs/apk/release/
# app-release.apk

ls app/build/outputs/bundle/release/
# app-release.aab
```

#### 3. 测试 APK
```bash
# 安装 APK 到设备
adb install app/build/outputs/apk/release/app-release.apk

# 或者直接运行
adb install -r app/build/outputs/apk/release/app-release.apk
```

### 3.3 使用 Fastlane 自动化打包

#### 1. 安装 Fastlane
```bash
# 安装 Fastlane
sudo gem install fastlane -NV

# 或者使用 Homebrew (macOS)
brew install fastlane
```

#### 2. 初始化 Fastlane
```bash
cd android
fastlane init
```

#### 3. 配置 Fastlane
创建 `android/fastlane/Fastfile`:
```ruby
default_platform(:android)

platform :android do
  desc "Build and release to Google Play"
  lane :release do
    # 构建
    gradle(
      task: "bundle",
      build_type: "Release",
      flavor: "Production"
    )

    # 上传到 Google Play
    upload_to_play_store(
      track: "internal",
      aab: "../android/app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Build APK"
  lane :build_apk do
    gradle(
      task: "assemble",
      build_type: "Release"
    )
  end

  desc "Clean build"
  lane :clean do
    gradle(task: "clean")
  end
end
```

#### 4. 使用 Fastlane
```bash
# 构建 APK
fastlane android build_apk

# 构建并发布
fastlane android release

# 清理
fastlane android clean
```

### 3.4 使用 CI/CD 工具

#### GitHub Actions
创建 `.github/workflows/build.yml`:
```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: |
        npm install
        cd android && ./gradlew clean

    - name: Build APK
      run: |
        cd android
        ./gradlew assembleRelease

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-release
        path: android/app/build/outputs/apk/release/app-release.apk
```

#### Expo EAS Build
```bash
# 安装 EAS CLI
npm install -g eas-cli

# 登录
eas login

# 配置 eas.json
{
  "build": {
    "preview": {
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "android": {
        "buildType": "app-bundle"
      }
    }
  }
}

# 构建
eas build --platform android --profile preview
```

### 3.5 发布到应用商店

#### Google Play Store

**1. 创建 Google Play 开发者账号**
- 访问: https://play.google.com/console
- 支付 $25 注册费
- 填写开发者信息

**2. 准备发布材料**
- 应用图标 (512x512 px)
- 应用截图 (手机、平板)
- 应用描述
- 隐私政策链接
- 应用分类

**3. 上传应用**
```bash
# 使用 Fastlane 上传
fastlane android release

# 或者手动上传
# 访问 Google Play Console
# 选择应用 → 发布管理 → 应用发布
# 上传 AAB 文件
```

**4. 发布流程**
```
1. 上传 AAB 文件
2. 填写发布说明
3. 选择发布轨道（内部测试、封闭测试、开放测试、生产）
4. 提交审核
5. 等待审核通过（通常 2-7 天）
6. 发布到生产环境
```

#### 其他应用商店

**华为应用市场**
- 访问: https://developer.huawei.com/consumer/cn/
- 上传 APK 文件
- 填写应用信息

**小米应用商店**
- 访问: https://dev.mi.com/
- 上传 APK 文件

**OPPO/vivo 应用商店**
- 分别访问各自开发者平台
- 上传 APK 文件

### 3.6 版本管理

#### 版本号配置
`android/app/build.gradle`:
```gradle
android {
    defaultConfig {
        versionCode 1
        versionName "1.0.0"
    }

    flavorDimensions "version"
    productFlavors {
        development {
            dimension "version"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
        }
        production {
            dimension "version"
        }
    }
}
```

#### 自动化版本管理
```bash
# 使用 react-native-version
npm install --save-dev react-native-version

# package.json
{
  "scripts": {
    "version": "react-native-version"
  }
}
```

### 3.7 常见问题

#### 打包失败
```bash
# 1. 清理缓存
cd android && ./gradlew clean && cd ..

# 2. 删除 node_modules
rm -rf node_modules
npm install

# 3. 重新构建
npx react-native run-android --variant=release

# 4. 检查签名配置
cat android/app/build.gradle | grep signingConfigs
```

#### APK 太大
```bash
# 1. 启用 ProGuard
android {
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}

# 2. 使用 App Bundle (AAB)
# AAB 只包含设备需要的代码和资源

# 3. 优化图片资源
# 使用 WebP 格式
# 压缩图片
```

#### 应用崩溃
```bash
# 查看崩溃日志
adb logcat | grep "AndroidRuntime"

# 或者使用 Android Studio
# View → Tool Windows → Logcat
```

---

## 附录：常用命令速查

### 开发命令
```bash
# 启动开发服务器
npx react-native start

# 运行到 Android
npx react-native run-android

# 运行到 iOS
npx react-native run-ios

# 清除缓存
npx react-native start --reset-cache
```

### Android 命令
```bash
# 构建 APK
cd android && ./gradlew assembleRelease

# 构建 AAB
cd android && ./gradlew bundleRelease

# 清理
cd android && ./gradlew clean

# 安装 APK
adb install app/build/outputs/apk/release/app-release.apk
```

### ADB 命令
```bash
# 查看设备
adb devices

# 安装 APK
adb install app.apk

# 卸载应用
adb uninstall com.yourapp.package

# 查看日志
adb logcat | grep "ReactNative"

# WiFi 连接
adb connect 192.168.1.100:5555
adb tcpip 5555
```

### Fastlane 命令
```bash
# 构建 APK
fastlane android build_apk

# 发布到 Google Play
fastlane android release

# 清理
fastlane android clean
```

---

**文档版本**: 1.0
**最后更新**: 2026-01-22
**维护者**: React Native 开发团队
