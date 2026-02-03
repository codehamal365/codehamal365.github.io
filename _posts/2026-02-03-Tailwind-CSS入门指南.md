---
title: Tailwind CSS 入门指南
categories:
  - Tailwind
tags:
  - Tailwind
  - CSS
  - 入门
  - 指南
---


# Tailwind CSS 入门指南

## 📚 目录

1. [什么是Tailwind CSS？](#什么是tailwind-css)
2. [安装和配置](#安装和配置)
3. [核心概念](#核心概念)
4. [基础样式](#基础样式)
5. [响应式设计](#响应式设计)
6. [状态变体](#状态变体)
7. [自定义配置](#自定义配置)
8. [实用工具类](#实用工具类)
9. [最佳实践](#最佳实践)

---

## 什么是Tailwind CSS？

### 定义
Tailwind CSS 是一个 **实用优先（Utility-First）** 的 CSS 框架，它提供了一套低级别的工具类，让你可以通过组合这些类来构建自定义设计，而无需编写自定义 CSS。

### 核心特点
- **实用优先**: 提供大量原子化的工具类
- **高度可定制**: 通过配置文件自定义设计系统
- **响应式设计**: 内置响应式断点
- **状态变体**: 支持 hover、focus、active 等状态
- **暗黑模式**: 内置暗黑模式支持
- **无障碍**: 支持无障碍功能

### 与传统 CSS 的区别

```css
{% raw %}
/* 传统 CSS */
.button {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.25rem;
  font-weight: 600;
}

/* Tailwind CSS */
<button class="px-4 py-2 bg-blue-500 text-white rounded font-semibold">
  Click me
</button>
{% endraw %}
```

---

## 安装和配置

### 1. 安装 Tailwind CSS

#### 方式1: 通过 npm 安装（推荐）
```bash
{% raw %}
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
{% endraw %}
```

#### 方式2: 使用 CDN（仅用于学习）
```html
{% raw %}
<!-- 在 HTML 中添加 -->
<script src="https://cdn.tailwindcss.com"></script>
{% endraw %}
```

### 2. 配置 Tailwind CSS

#### 创建配置文件
```bash
{% raw %}
npx tailwindcss init -p
{% endraw %}
```

这会创建两个文件：
- `tailwind.config.js` - Tailwind 配置
- `postcss.config.js` - PostCSS 配置

#### tailwind.config.js
```javascript
{% raw %}
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
{% endraw %}
```

#### postcss.config.js
```javascript
{% raw %}
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
{% endraw %}
```

### 3. 在项目中使用

#### 创建 CSS 文件
```css
{% raw %}
/* src/styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
{% endraw %}
```

#### 在 JavaScript/TypeScript 中导入
```javascript
{% raw %}
// src/index.js 或 src/index.tsx
import './styles.css';
{% endraw %}
```

#### 在 HTML 中使用
```html
{% raw %}
<!DOCTYPE html>
<html>
<head>
  <link href="./styles.css" rel="stylesheet">
</head>
<body>
  <div class="p-4 bg-blue-500 text-white">
    Hello Tailwind!
  </div>
</body>
</html>
{% endraw %}
```

---

## 核心概念

### 1. 工具类（Utility Classes）

Tailwind 的核心是工具类，每个类对应一个 CSS 属性和值。

```html
{% raw %}
<!-- 文本样式 -->
<p class="text-lg font-bold text-blue-600">大号粗体蓝色文本</p>

<!-- 背景样式 -->
<div class="bg-gray-100 p-4 rounded-lg">灰色背景，内边距，圆角</div>

<!-- 边框样式 -->
<button class="border-2 border-blue-500 px-4 py-2">蓝色边框按钮</button>

<!-- 间距样式 -->
<div class="m-4 p-4">外边距4，内边距4</div>
{% endraw %}
```

### 2. 命名规则

Tailwind 使用一致的命名规则：

```html
{% raw %}
<!-- 尺寸 -->
w-4    <!-- width: 1rem (16px) -->
w-8    <!-- width: 2rem (32px) -->
w-full <!-- width: 100% -->

<!-- 颜色 -->
bg-blue-500  <!-- 背景蓝色 -->
text-red-600  <!-- 文本红色 -->
border-green-400 <!-- 边框绿色 -->

<!-- 间距 -->
m-4    <!-- margin: 1rem -->
p-2    <!-- padding: 0.5rem -->
mt-8   <!-- margin-top: 2rem -->
{% endraw %}
```

### 3. 响应式前缀

```html
{% raw %}
<!-- 移动端：小屏幕 -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- 宽度100% (默认) -->
  <!-- 中等屏幕：宽度50% -->
  <!-- 大屏幕：宽度33.33% -->
</div>

<!-- 响应式文本 -->
<p class="text-sm md:text-base lg:text-lg">
  <!-- 小屏幕：小文本 -->
  <!-- 中等屏幕：基础文本 -->
  <!-- 大屏幕：大文本 -->
</p>
{% endraw %}
```

### 4. 状态变体

```html
{% raw %}
<!-- Hover 状态 -->
<button class="bg-blue-500 hover:bg-blue-700 transition-colors">
  Hover me
</button>

<!-- Focus 状态 -->
<input class="border-2 border-gray-300 focus:border-blue-500 outline-none"
       type="text"
       placeholder="Focus me">

<!-- Active 状态 -->
<button class="bg-blue-500 active:bg-blue-800">
  Click me
</button>

<!-- Disabled 状态 -->
<button class="bg-gray-400 disabled:opacity-50" disabled>
  Disabled
</button>
{% endraw %}
```

---

## 基础样式

### 1. 颜色系统

```html
{% raw %}
<!-- 背景颜色 -->
<div class="bg-white">白色背景</div>
<div class="bg-gray-100">浅灰背景</div>
<div class="bg-gray-800">深灰背景</div>
<div class="bg-red-500">红色背景</div>
<div class="bg-blue-500">蓝色背景</div>
<div class="bg-green-500">绿色背景</div>
<div class="bg-yellow-500">黄色背景</div>
<div class="bg-purple-500">紫色背景</div>
<div class="bg-pink-500">粉色背景</div>

<!-- 文本颜色 -->
<p class="text-gray-900">深灰文本</p>
<p class="text-gray-600">中灰文本</p>
<p class="text-gray-400">浅灰文本</p>
<p class="text-blue-600">蓝色文本</p>
<p class="text-red-600">红色文本</p>
<p class="text-green-600">绿色文本</p>

<!-- 边框颜色 -->
<div class="border border-gray-300">灰色边框</div>
<div class="border-2 border-blue-500">蓝色边框</div>
{% endraw %}
```

### 2. 字体和排版

```html
{% raw %}
<!-- 字体大小 -->
<p class="text-xs">超小文本 (12px)</p>
<p class="text-sm">小文本 (14px)</p>
<p class="text-base">基础文本 (16px)</p>
<p class="text-lg">大文本 (18px)</p>
<p class="text-xl">超大文本 (20px)</p>
<p class="text-2xl">2xl文本 (24px)</p>
<p class="text-3xl">3xl文本 (30px)</p>

<!-- 字体粗细 -->
<p class="font-thin">细体 (100)</p>
<p class="font-light">轻体 (300)</p>
<p class="font-normal">正常 (400)</p>
<p class="font-medium">中等 (500)</p>
<p class="font-semibold">半粗 (600)</p>
<p class="font-bold">粗体 (700)</p>
<p class="font-extrabold">超粗 (800)</p>

<!-- 文本装饰 -->
<p class="underline">下划线</p>
<p class="line-through">删除线</p>
<p class="no-underline">无装饰</p>

<!-- 文本对齐 -->
<p class="text-left">左对齐</p>
<p class="text-center">居中对齐</p>
<p class="text-right">右对齐</p>
<p class="text-justify">两端对齐</p>

<!-- 行高 -->
<p class="leading-none">行高: 1</p>
<p class="leading-tight">行高: 1.25</p>
<p class="leading-normal">行高: 1.5</p>
<p class="leading-relaxed">行高: 1.625</p>
<p class="leading-loose">行高: 2</p>

<!-- 字母间距 -->
<p class="tracking-tight">紧间距</p>
<p class="tracking-normal">正常间距</p>
<p class="tracking-wide">宽间距</p>
{% endraw %}
```

### 3. 间距系统

```html
{% raw %}
<!-- Margin (外边距) -->
<div class="m-0">无外边距</div>
<div class="m-1">外边距 0.25rem</div>
<div class="m-2">外边距 0.5rem</div>
<div class="m-4">外边距 1rem</div>
<div class="m-8">外边距 2rem</div>
<div class="m-16">外边距 4rem</div>

<!-- Padding (内边距) -->
<div class="p-0">无内边距</div>
<div class="p-1">内边距 0.25rem</div>
<div class="p-2">内边距 0.5rem</div>
<div class="p-4">内边距 1rem</div>
<div class="p-8">内边距 2rem</div>

<!-- 方向特定 -->
<div class="mt-4">上外边距</div>
<div class="mr-4">右外边距</div>
<div class="mb-4">下外边距</div>
<div class="ml-4">左外边距</div>

<div class="pt-4">上内边距</div>
<div class="pr-4">右内边距</div>
<div class="pb-4">下内边距</div>
<div class="pl-4">左内边距</div>

<!-- 水平和垂直 -->
<div class="mx-4">左右外边距</div>
<div class="my-4">上下外边距</div>
<div class="px-4">左右内边距</div>
<div class="py-4">上下内边距</div>
{% endraw %}
```

### 4. 尺寸系统

```html
{% raw %}
<!-- 宽度 -->
<div class="w-0">宽度 0</div>
<div class="w-1/4">宽度 25%</div>
<div class="w-1/2">宽度 50%</div>
<div class="w-3/4">宽度 75%</div>
<div class="w-full">宽度 100%</div>
<div class="w-screen">宽度 100vw</div>

<!-- 高度 -->
<div class="h-0">高度 0</div>
<div class="h-1/4">高度 25%</div>
<div class="h-1/2">高度 50%</div>
<div class="h-3/4">高度 75%</div>
<div class="h-full">高度 100%</div>
<div class="h-screen">高度 100vh</div>

<!-- 最小/最大尺寸 -->
<div class="min-w-0">最小宽度 0</div>
<div class="min-w-full">最小宽度 100%</div>
<div class="max-w-xs">最大宽度 20rem</div>
<div class="max-w-sm">最大宽度 24rem</div>
<div class="max-w-md">最大宽度 28rem</div>
<div class="max-w-lg">最大宽度 32rem</div>
<div class="max-w-xl">最大宽度 36rem</div>
<div class="max-w-2xl">最大宽度 42rem</div>
<div class="max-w-3xl">最大宽度 48rem</div>
<div class="max-w-4xl">最大宽度 56rem</div>
<div class="max-w-5xl">最大宽度 64rem</div>
<div class="max-w-6xl">最大宽度 72rem</div>
<div class="max-w-full">最大宽度 100%</div>
<div class="max-w-screen-sm">最大宽度 640px</div>
<div class="max-w-screen-md">最大宽度 768px</div>
<div class="max-w-screen-lg">最大宽度 1024px</div>
<div class="max-w-screen-xl">最大宽度 1280px</div>
<div class="max-w-screen-2xl">最大宽度 1536px</div>
{% endraw %}
```

### 5. 边框系统

```html
{% raw %}
<!-- 边框宽度 -->
<div class="border">边框 1px</div>
<div class="border-0">无边框</div>
<div class="border-2">边框 2px</div>
<div class="border-4">边框 4px</div>
<div class="border-8">边框 8px</div>

<!-- 边框方向 -->
<div class="border-t">上边框</div>
<div class="border-r">右边框</div>
<div class="border-b">下边框</div>
<div class="border-l">左边框</div>

<!-- 边框颜色 -->
<div class="border-gray-300">灰色边框</div>
<div class="border-blue-500">蓝色边框</div>
<div class="border-red-500">红色边框</div>

<!-- 边框样式 -->
<div class="border-solid">实线</div>
<div class="border-dashed">虚线</div>
<div class="border-dotted">点线</div>
<div class="border-double">双线</div>

<!-- 圆角 -->
<div class="rounded">圆角 0.25rem</div>
<div class="rounded-none">无圆角</div>
<div class="rounded-sm">小圆角 0.125rem</div>
<div class="rounded-lg">大圆角 0.5rem</div>
<div class="rounded-xl">超大圆角 0.75rem</div>
<div class="rounded-2xl">2xl圆角 1rem</div>
<div class="rounded-3xl">3xl圆角 1.5rem</div>
<div class="rounded-full">全圆角 (圆形)</div>

<!-- 方向特定圆角 -->
<div class="rounded-t-lg">上圆角</div>
<div class="rounded-r-lg">右圆角</div>
<div class="rounded-b-lg">下圆角</div>
<div class="rounded-l-lg">左圆角</div>
{% endraw %}
```

### 6. 阴影系统

```html
{% raw %}
<!-- 阴影 -->
<div class="shadow">基础阴影</div>
<div class="shadow-sm">小阴影</div>
<div class="shadow-md">中等阴影</div>
<div class="shadow-lg">大阴影</div>
<div class="shadow-xl">超大阴影</div>
<div class="shadow-2xl">2xl阴影</div>
<div class="shadow-inner">内阴影</div>
<div class="shadow-none">无阴影</div>
{% endraw %}
```

### 7. 透明度和不透明度

```html
{% raw %}
<!-- 不透明度 -->
<div class="opacity-0">完全透明</div>
<div class="opacity-25">25% 不透明</div>
<div class="opacity-50">50% 不透明</div>
<div class="opacity-75">75% 不透明</div>
<div class="opacity-100">完全不透明</div>
{% endraw %}
```

### 8. 背景图片和渐变

```html
{% raw %}
<!-- 背景图片 -->
<div class="bg-cover bg-center bg-no-repeat"
     style="background-image: url('image.jpg')">
  背景图片
</div>

<!-- 渐变 -->
<div class="bg-gradient-to-r from-blue-500 to-purple-500">
  水平渐变
</div>

<div class="bg-gradient-to-b from-blue-500 to-purple-500">
  垂直渐变
</div>

<div class="bg-gradient-to-tr from-yellow-400 via-red-500 to-pink-500">
  多色渐变
</div>
{% endraw %}
```

---

## 响应式设计

### 1. 响应式断点

Tailwind 默认使用以下断点：

```css
{% raw %}
/* 默认: 0px */
/* sm: 640px */
/* md: 768px */
/* lg: 1024px */
/* xl: 1280px */
/* 2xl: 1536px */
{% endraw %}
```

### 2. 响应式示例

```html
{% raw %}
<!-- 响应式宽度 -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- 移动端: 100% -->
  <!-- 平板: 50% -->
  <!-- 桌面: 33.33% -->
</div>

<!-- 响应式文本 -->
<p class="text-sm md:text-base lg:text-lg xl:text-xl">
  <!-- 移动端: 小文本 -->
  <!-- 平板: 基础文本 -->
  <!-- 桌面: 大文本 -->
  <!-- 超大屏: 超大文本 -->
</p>

<!-- 响应式间距 -->
<div class="p-2 md:p-4 lg:p-8">
  <!-- 移动端: 小内边距 -->
  <!-- 平板: 中等内边距 -->
  <!-- 桌面: 大内边距 -->
</div>

<!-- 响应式布局 -->
<div class="flex flex-col md:flex-row">
  <!-- 移动端: 垂直排列 -->
  <!-- 平板及以上: 水平排列 -->
</div>
{% endraw %}
```

### 3. 容器组件

```html
{% raw %}
<!-- 基础容器 -->
<div class="container mx-auto px-4">
  <!-- 内容 -->
</div>

<!-- 响应式容器 -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <!-- 移动端: 左右内边距 1rem -->
  <!-- 平板: 左右内边距 1.5rem -->
  <!-- 桌面: 左右内边距 2rem -->
</div>
{% endraw %}
```

### 4. 响应式网格

```html
{% raw %}
<!-- 简单网格 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-gray-100 p-4">项目 1</div>
  <div class="bg-gray-100 p-4">项目 2</div>
  <div class="bg-gray-100 p-4">项目 3</div>
  <div class="bg-gray-100 p-4">项目 4</div>
  <div class="bg-gray-100 p-4">项目 5</div>
  <div class="bg-gray-100 p-4">项目 6</div>
</div>

<!-- 自动填充网格 -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <!-- 自动适应列数 -->
</div>
{% endraw %}
```

---

## 状态变体

### 1. Hover 状态

```html
{% raw %}
<!-- 基础 Hover -->
<button class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded">
  Hover me
</button>

<!-- Hover 边框 -->
<button class="border-2 border-blue-500 hover:border-blue-700 px-4 py-2 rounded">
  Hover 边框
</button>

<!-- Hover 阴影 -->
<button class="shadow-md hover:shadow-lg px-4 py-2 rounded">
  Hover 阴影
</button>

<!-- Hover 变换 -->
<button class="transform hover:scale-105 transition-transform px-4 py-2 rounded">
  Hover 放大
</button>
{% endraw %}
```

### 2. Focus 状态

```html
{% raw %}
<!-- 基础 Focus -->
<input class="border-2 border-gray-300 focus:border-blue-500 outline-none px-4 py-2 rounded"
       type="text"
       placeholder="Focus me">

<!-- Focus 阴影 -->
<input class="border-2 border-gray-300 focus:shadow-outline outline-none px-4 py-2 rounded"
       type="text"
       placeholder="Focus with shadow">

<!-- Focus Ring -->
<input class="border-2 border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none px-4 py-2 rounded"
       type="text"
       placeholder="Focus with ring">
{% endraw %}
```

### 3. Active 状态

```html
{% raw %}
<button class="bg-blue-500 active:bg-blue-800 text-white px-4 py-2 rounded">
  Click me
</button>
{% endraw %}
```

### 4. Disabled 状态

```html
{% raw %}
<button class="bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-2 rounded"
        disabled>
  Disabled
</button>
{% endraw %}
```

### 5. 访问状态

```html
{% raw %}
<!-- 访问链接 -->
<a href="#" class="text-blue-500 visited:text-purple-600">
  访问过的链接
</a>
{% endraw %}
```

### 6. 焦点可见性

```html
{% raw %}
<!-- 焦点可见 -->
<button class="focus:outline-none focus:ring-2 focus:ring-blue-500 px-4 py-2 rounded">
  焦点可见
</button>
{% endraw %}
```

### 7. 父级状态

```html
{% raw %}
<!-- 父级 Hover -->
<div class="group hover:bg-gray-100 p-4 rounded">
  <p class="group-hover:text-blue-500">父级 Hover 时文本变蓝</p>
</div>

<!-- 父级 Focus -->
<div class="group focus-within:bg-blue-50 p-4 rounded">
  <input class="focus:outline-none" type="text" placeholder="Focus here">
  <p class="group-focus-within:text-blue-500">输入框 Focus 时文本变蓝</p>
</div>
{% endraw %}
```

---

## 自定义配置

### 1. 扩展主题

```javascript
{% raw %}
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      // 自定义颜色
      colors: {
        'brand-primary': '#3b82f6',
        'brand-secondary': '#8b5cf6',
        'brand-accent': '#ec4899',
        'brand-dark': '#1f2937',
        'brand-light': '#f3f4f6',
      },

      // 自定义字体
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'serif': ['Georgia', 'serif'],
        'mono': ['Fira Code', 'monospace'],
      },

      // 自定义间距
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '104': '26rem',
      },

      // 自定义阴影
      boxShadow: {
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'glow': '0 0 15px rgba(59, 130, 246, 0.5)',
      },

      // 自定义圆角
      borderRadius: {
        'xl': '1.25rem',
        '2xl': '1.5rem',
      },

      // 自定义动画
      animation: {
        'bounce-slow': 'bounce 3s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },

      // 自定义过渡
      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
      },
    },
  },
  plugins: [],
}
{% endraw %}
```

### 2. 自定义变体

```javascript
{% raw %}
// tailwind.config.js
module.exports = {
  variants: {
    extend: {
      // 自定义变体
      'first-letter': '&::first-letter',
      'first-line': '&::first-line',
      'selection': '&::selection',
      'marker': '&::marker',
      'file': '&::file-selector-button',
    },
  },
  plugins: [],
}
{% endraw %}
```

### 3. 使用插件

```javascript
{% raw %}
// tailwind.config.js
module.exports = {
  plugins: [
    // 自定义插件
    function({ addUtilities, addComponents, theme }) {
      // 添加工具类
      addUtilities({
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },
      });

      // 添加组件
      addComponents({
        '.btn': {
          padding: '0.5rem 1rem',
          borderRadius: '0.25rem',
          fontWeight: '600',
          transition: 'all 0.2s',
          '&:hover': {
            transform: 'translateY(-1px)',
          },
        },
      });
    },
  ],
}
{% endraw %}
```

### 4. 自定义类名

```javascript
{% raw %}
// tailwind.config.js
module.exports = {
  prefix: 'tw-', // 为所有类添加前缀
  important: true, // 使用 !important
}
{% endraw %}
```

---

## 实用工具类

### 1. 布局工具

```html
{% raw %}
<!-- Flexbox -->
<div class="flex flex-row justify-start items-center">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div class="flex flex-col justify-center items-center">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- 定位 -->
<div class="relative">
  <div class="absolute top-0 left-0">绝对定位</div>
  <div class="sticky top-0">粘性定位</div>
</div>

<!-- 溢出 -->
<div class="overflow-hidden overflow-x-auto overflow-y-scroll">
  溢出处理
</div>
{% endraw %}
```

### 2. 交互工具

```html
{% raw %}
<!-- 鼠标指针 -->
<button class="cursor-pointer">可点击</button>
<button class="cursor-not-allowed">不可点击</button>
<button class="cursor-wait">等待</button>

<!-- 禁用选择 -->
<div class="select-none">不可选择</div>
<div class="select-text">可选择文本</div>

<!-- 拖拽 -->
<div class="draggable">可拖拽</div>

<!-- 调整大小 -->
<textarea class="resize-none">不可调整大小</textarea>
<textarea class="resize-x">水平调整</textarea>
<textarea class="resize-y">垂直调整</textarea>
<textarea class="resize">双向调整</textarea>
{% endraw %}
```

### 3. 视觉工具

```html
{% raw %}
<!-- 透明度 -->
<div class="opacity-50">50% 透明度</div>

<!-- 可见性 -->
<div class="visible">可见</div>
<div class="invisible">不可见</div>

<!-- 溢出可见 -->
<div class="overflow-visible">溢出可见</div>

<!-- 对象拟合 -->
<img class="object-cover w-32 h-32" src="image.jpg">
<img class="object-contain w-32 h-32" src="image.jpg">
<img class="object-fill w-32 h-32" src="image.jpg">
<img class="object-none w-32 h-32" src="image.jpg">
{% endraw %}
```

### 4. 表单工具

```html
{% raw %}
<!-- 表单元素 -->
<input class="appearance-none" type="checkbox">
<input class="placeholder-gray-400" type="text" placeholder="Placeholder">
<select class="bg-white">
  <option>Option 1</option>
</select>
<textarea class="resize-none"></textarea>

<!-- 滚动条 -->
<div class="scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
  自定义滚动条
</div>
{% endraw %}
```

---

## 最佳实践

### 1. 组件化思维

```html
{% raw %}
<!-- ❌ 不推荐：直接使用工具类 -->
<div class="bg-blue-500 text-white px-4 py-2 rounded font-semibold hover:bg-blue-700 transition-colors">
  Button
</div>

<!-- ✅ 推荐：创建组件类 -->
<!-- 在 CSS 中 -->
@layer components {
  .btn-primary {
    @apply bg-blue-500 text-white px-4 py-2 rounded font-semibold;
    @apply hover:bg-blue-700 transition-colors;
  }
}

<!-- 在 HTML 中 -->
<button class="btn-primary">Button</button>
{% endraw %}
```

### 2. 提取重复样式

```html
{% raw %}
<!-- ❌ 不推荐：重复的样式 -->
<div class="bg-white shadow-md rounded-lg p-4 mb-4">Card 1</div>
<div class="bg-white shadow-md rounded-lg p-4 mb-4">Card 2</div>
<div class="bg-white shadow-md rounded-lg p-4 mb-4">Card 3</div>

<!-- ✅ 推荐：提取公共类 -->
<!-- 在 CSS 中 -->
@layer components {
  .card {
    @apply bg-white shadow-md rounded-lg p-4 mb-4;
  }
}

<!-- 在 HTML 中 -->
<div class="card">Card 1</div>
<div class="card">Card 2</div>
<div class="card">Card 3</div>
{% endraw %}
```

### 3. 使用 @apply

```css
{% raw %}
/* 在 CSS 文件中 */
@layer components {
  .btn {
    @apply px-4 py-2 rounded font-semibold transition-colors;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white;
    @apply hover:bg-blue-700;
  }

  .btn-secondary {
    @apply btn bg-gray-500 text-white;
    @apply hover:bg-gray-700;
  }

  .card {
    @apply bg-white shadow-md rounded-lg p-4;
  }

  .input {
    @apply border-2 border-gray-300 rounded px-4 py-2;
    @apply focus:border-blue-500 focus:outline-none;
  }
}
{% endraw %}
```

### 4. 响应式设计模式

```html
{% raw %}
<!-- 移动优先 -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- 移动端：100% -->
  <!-- 平板：50% -->
  <!-- 桌面：33.33% -->
</div>

<!-- 容器查询（Tailwind 3.2+） -->
<div class="@container">
  <div class="@lg:text-lg">
    <!-- 容器宽度 >= 32rem 时文本变大 -->
  </div>
</div>
{% endraw %}
```

### 5. 性能优化

```html
{% raw %}
<!-- ❌ 不推荐：使用动态类名 -->
<div :class="`bg-${color}-500`">动态颜色</div>

<!-- ✅ 推荐：使用条件类 -->
<div :class="{
  'bg-red-500': color === 'red',
  'bg-blue-500': color === 'blue',
  'bg-green-500': color === 'green',
}">条件颜色</div>

<!-- ✅ 或者使用 CSS 变量 -->
<div class="bg-[var(--color)]" style="--color: #3b82f6">CSS 变量</div>
{% endraw %}
```

### 6. 暗黑模式

```html
{% raw %}
<!-- 基础暗黑模式 -->
<div class="bg-white dark:bg-gray-800 text-black dark:text-white">
  <p>浅色模式：白色背景，黑色文字</p>
  <p>深色模式：深灰背景，白色文字</p>
</div>

<!-- 按钮暗黑模式 -->
<button class="bg-blue-500 dark:bg-blue-700 text-white px-4 py-2 rounded">
  按钮
</button>

<!-- 边框暗黑模式 -->
<div class="border border-gray-300 dark:border-gray-700 p-4">
  边框
</div>
{% endraw %}
```

### 7. 自定义主题

```javascript
{% raw %}
// tailwind.config.js
module.exports = {
  darkMode: 'class', // 或 'media'
  theme: {
    extend: {
      colors: {
        'brand': {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
    },
  },
}
{% endraw %}
```

### 8. 响应式设计模式

```html
{% raw %}
<!-- 移动优先 -->
<div class="flex flex-col md:flex-row">
  <!-- 移动端：垂直排列 -->
  <!-- 平板及以上：水平排列 -->
</div>

<!-- 隐藏/显示 -->
<div class="hidden md:block">仅在平板及以上显示</div>
<div class="block md:hidden">仅在移动端显示</div>

<!-- 响应式间距 -->
<div class="space-y-2 md:space-y-4 lg:space-y-6">
  <!-- 垂直间距随屏幕变大而增加 -->
</div>
{% endraw %}
```

---

## 总结

Tailwind CSS 是一个强大的实用优先 CSS 框架，通过学习本指南，你已经掌握了：

1. **核心概念** - 工具类、命名规则、响应式前缀
2. **基础样式** - 颜色、字体、间距、尺寸、边框、阴影
3. **响应式设计** - 断点、响应式类、容器查询
4. **状态变体** - hover、focus、active、disabled
5. **自定义配置** - 扩展主题、自定义变体、插件
6. **实用工具** - 布局、交互、视觉、表单
7. **最佳实践** - 组件化、提取重复、@apply、性能优化

### 下一步学习建议

1. **实践项目** - 使用 Tailwind CSS 构建实际项目
2. **学习高级特性** - 深入学习 Tailwind CSS 高级特性
3. **探索插件** - 了解 Tailwind 插件生态系统
4. **自定义配置** - 根据项目需求定制设计系统
5. **性能优化** - 学习如何优化 Tailwind 构建

### 资源推荐

- **官方文档**: https://tailwindcss.com/docs
- **Tailwind UI**: https://tailwindui.com
- **Tailwind Components**: https://tailwindcomponents.com
- **Playground**: https://play.tailwindcss.com

祝你 Tailwind CSS 学习愉快！🚀