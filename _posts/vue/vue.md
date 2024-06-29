---
sidebar_position: 1
---

## vue3

项目demo参考：`git@github.com:codehamal365/vue3-demo.git`

### Api风格


Vue 的组件可以按两种不同的风格书写：**选项式 API** 和 **组合式 API**。

#### 选项式 API (Options API)[](https://cn.vuejs.org/guide/introduction.html#options-api)

使用选项式 API，我们可以用包含多个选项的对象来描述组件的逻辑，例如 `data`、`methods` 和 `mounted`。选项所定义的属性都会暴露在函数内部的 `this` 上，它会指向当前的组件实例。

```vue
<script>
export default {
  // data() 返回的属性将会成为响应式的状态
  // 并且暴露在 `this` 上
  data() {
    return {
      count: 0
    }
  },

  // methods 是一些用来更改状态与触发更新的函数
  // 它们可以在模板中作为事件处理器绑定
  methods: {
    increment() {
      this.count++
    }
  },

  // 生命周期钩子会在组件生命周期的各个不同阶段被调用
  // 例如这个函数就会在组件挂载完成后被调用
  mounted() {
    console.log(`The initial count is ${this.count}.`)
  }
}
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

#### 组合式 API (Composition API)[](https://cn.vuejs.org/guide/introduction.html#composition-api)

通过组合式 API，我们可以使用导入的 API 函数来描述组件逻辑。在单文件组件中，组合式 API 通常会与 [``](https://cn.vuejs.org/api/sfc-script-setup.html) 搭配使用。这个 `setup` attribute 是一个标识，告诉 Vue 需要在编译时进行一些处理，让我们可以更简洁地使用组合式 API。比如，`<script setup>` 中的导入和顶层变量/函数都能够在模板中直接使用。

下面是使用了组合式 API 与 `<script setup>` 改造后和上面的模板完全一样的组件：

```vue
<script setup>
import { ref, onMounted } from 'vue'

// 响应式状态
const count = ref(0)

// 用来修改状态、触发更新的函数
function increment() {
  count.value++
}

// 生命周期钩子
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

### 创建项目

我们可以使用`nvm`来安装对应的node,然后使用以下命令来创建`vue3-demo`项目

> // 查看已安装的node版本
>
> nvm list 
>
> // 查看所有的node版本
>
> nvm list available
>
> // 安装node
>
> nvm install 16.3.2(版本号)
>
> // 切换node版本
>
> nvm use 12.17.0

```bash
npm create vue@latest
```

>Vue.js - The Progressive JavaScript Framework
>
>✔ Project name: … vue3-demo
>✔ Add TypeScript? … No / Yes
>✔ Add JSX Support? … No / Yes
>✔ Add Vue Router for Single Page Application development? … No / Yes
>✔ Add Pinia for state management? … No / Yes
>✔ Add Vitest for Unit Testing? … No / Yes
>✔ Add an End-to-End Testing Solution? › No
>✔ Add ESLint for code quality? … No / Yes
>✔ Add Vue DevTools 7 extension for debugging? (experimental) … No / Yes

```bash
cd vue3-demo
npm install
npm run dev
```

vue3中常见的基础功能，请参考(https://cn.vuejs.org/guide/essentials/template-syntax.html)

### ref 和 reactive

在Vue 3中，`ref` 和 `reactive` 都是响应式系统的API，但它们的用途和行为有所不同：

1. **`ref`**
   - `ref` 用于创建一个响应式的引用对象。
   - 它接收一个参数，可以是任何值（包括对象、数组等），并返回一个包含该值的响应式引用对象。
   - 使用 `ref` 创建的响应式引用，可以通过 `.value` 属性访问其内部值。
   - `ref` 常用于声明性渲染中，例如在模板中绑定数据。

   示例：
   ```javascript
   import { ref } from 'vue';
   
   const count = ref(0); // 创建一个响应式引用
   console.log(count.value); // 访问响应式引用的值
   
   // 在模板中使用
   // <div>{{ count.value }}</div>
   ```

2. **`reactive`**
   
   - `reactive` 用于创建一个响应式的代理对象。
   - 它接收一个普通对象作为参数，并返回该对象的响应式代理。
   - 代理对象是可读写的，并且是只读的代理，这意味着你不能直接访问原始对象，只能通过代理对象访问和修改数据。
   - `reactive` 适用于更复杂的数据结构，如嵌套对象或数组。
   
   示例：
   ```javascript
   import { reactive } from 'vue';
   
   const state = reactive({ count: 0 }); // 创建一个响应式代理对象
   console.log(state.count); // 访问响应式代理对象的属性
   
   // 在模板中使用
   // <div>{{ state.count }}</div>
   ```

**区别总结：**

- `ref` 适合用于基本数据类型或简单的场景，提供了一个带有 `.value` 属性的响应式引用。
- `reactive` 适合用于复杂的数据结构，提供了一个完整的响应式代理对象，允许直接访问和修改属性。
- 使用 `ref` 时，你需要通过 `.value` 访问和修改内部值；而使用 `reactive` 时，你可以直接访问和修改代理对象的属性。
- 在Vue模板中，`ref` 创建的响应式引用通常需要通过 `.value` 来绑定，而 `reactive` 创建的响应式代理可以直接在模板中使用。

根据你的具体需求，你可以选择使用 `ref` 或 `reactive` 来创建和管理Vue 3中的响应式数据。

#### ref

使用基本数据类型或者对象

```vue
<script setup>
import { ref } from "vue";

const msg = ref("hello");

const obj = ref({
  a: 1,
  b: 2,
});

const click = () => {
  msg.value = "hello 1";
};

const click2 = () => {
  obj.value.a = "click a";
};
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h1 class="green">{{ obj.a }}</h1>
    <button @click="click">click me</button>
    <button @click="click2">click me 2</button>
  </div>
</template>
```

#### reactive

reactive支持引用类型，Array，Object，Map，Set

```vue
<script setup>
import { reactive } from "vue";

let person = reactive({
  name: "小满",
});

const click = () => {
  person.name = "大满";
};
</script>
```



#### toRef

toRef只能修改响应式对象的值并且视图发生变化，非响应式的值可以修改，但是视图没有变化

```vue
<template>
  <div>
    <button @click="change">按钮</button>
    {{ state }}
  </div>
</template>

<script setup lang="ts">
import { reactive, toRef } from "vue";

// 必须加上reactive，才能是响应式，否则toRef没有作用
const obj = reactive({
  foo: 1,
  bar: 1,
});

// bar 转化为响应式对象，相当于解构
const state = toRef(obj, "bar");

const change = () => {
  state.value++;
  console.log(obj, state);
};
</script>
```

#### toRefs

可以帮我们批量创建ref对象主要是方便我们解构使用

```vue
<script setup lang="ts">
import { reactive, toRefs } from 'vue'
const obj = reactive({
   foo: 1,
   bar: 1
})
 
let { foo, bar } = toRefs(obj)
 
foo.value++
console.log(foo, bar);
</script>
```

### 更多功能点

- 监听 https://cn.vuejs.org/guide/essentials/watchers.html
- 生命周期 https://cn.vuejs.org/api/composition-api-lifecycle.html
- 内置组件 https://cn.vuejs.org/guide/built-ins/transition.html

### 组合式 API 使用

在 Vue 应用的概念中，[“组合式函数”(Composables)](https://cn.vuejs.org/guide/reusability/composables.html) 是一个利用 Vue 的组合式 API 来封装和复用**有状态逻辑**的函数。

当构建前端应用时，我们常常需要复用公共任务的逻辑。例如为了在不同地方格式化时间，我们可能会抽取一个可复用的日期格式化函数。这个函数封装了**无状态的逻辑**：它在接收一些输入后立刻返回所期望的输出。复用无状态逻辑的库有很多，比如你可能已经用过的 [lodash](https://lodash.com/) 或是 [date-fns](https://date-fns.org/)。

```js
// mouse.js
import { ref, onMounted, onUnmounted } from 'vue'

// 按照惯例，组合式函数名以“use”开头
export function useMouse() {
  // 被组合式函数封装和管理的状态
  const x = ref(0)
  const y = ref(0)

  // 组合式函数可以随时更改其状态。
  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  // 一个组合式函数也可以挂靠在所属组件的生命周期上
  // 来启动和卸载副作用
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  // 通过返回值暴露所管理的状态
  return { x, y }
}
```

下面是它在组件中使用的方式：

```vue
<script setup>
import { useMouse } from './mouse.js'

const { x, y } = useMouse()
</script>

<template>Mouse position is at: {{ x }}, {{ y }}</template>
```


## vue router

[Vue Router](https://router.vuejs.org/zh/introduction.html) 是 [Vue.js](https://cn.vuejs.org/) 的官方路由。它与 Vue.js 核心深度集成，让用 Vue.js 构建单页应用变得轻而易举。功能包括：

- 嵌套路由映射
- 动态路由选择
- 模块化、基于组件的路由配置
- 路由参数、查询、通配符
- 展示由 Vue.js 的过渡系统提供的过渡效果
- 细致的导航控制
- 自动激活 CSS 类的链接
- HTML5 history 模式或 hash 模式
- 可定制的滚动行为
- URL 的正确编码

#### 路由的理解

![image-20231018144351536](assets/image-20231018144351536.png)

#### 安装 vue router

对于一个现有的使用 JavaScript 包管理器的项目，你可以从 npm registry 中安装 Vue Router：

```bash
npm install vue-router@4
```

#### 基本实现

1、路由配置`router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import News from '@/views/News.vue'
import About from '@/views/About.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/home',
            component: Home
        },
        {
            path: '/about',
            component: About
        },
        {
            path: '/news',
            component: News
        }
    ]
})
export default router
```

2、`main.js`中引入

```js
import router from './router/index'
app.use(router)

app.mount('#app')
```

3、`App.vue`中配置

```vue
<template>
  <div class="app">
    <h2 class="title">Vue路由测试</h2>
    <!-- 导航区 -->
    <div class="navigate">
      <RouterLink to="/home" active-class="active">首页</RouterLink>
      <RouterLink to="/news" active-class="active">新闻</RouterLink>
      <RouterLink to="/about" active-class="active">关于</RouterLink>
    </div>
    <!-- 展示区 -->
    <div class="main-content">
      <RouterView></RouterView>
    </div>
  </div>
</template>

<script lang="ts" setup name="App">
  import {RouterLink,RouterView} from 'vue-router'  
</script>
```

#### 两个注意点

> 1. 路由组件通常存放在`pages` 或 `views`文件夹，一般组件通常存放在`components`文件夹。
> 2. 通过点击导航，视觉效果上“消失” 了的路由组件，默认是被**卸载**掉的，需要的时候再去**挂载**。

- 路由组件：靠路由规则渲染出来的。`route:[{path:/demo,component:demo}]`
- 一般组件：亲手写出来的标签。`<demo/>`

#### 路由器工作模式

1. `history`模式

   > 优点：`URL`更加美观，不带有`#`，更接近传统的网站`URL`。
   >
   > 缺点：后期项目上线，需要服务端配合处理路径问题，否则刷新会有`404`错误。
   >
   > ```
   > const router = createRouter({
   > 	history:createWebHistory(), //history模式
   > 	/******/
   > })
   > ```
   >
   > 各版本：
   >
   > vue2——`mode:'history'`
   >
   > vue3——`history:createWebHistory()`
   >
   > React——`BrowserRouter`

2. `hash`模式

   > 优点：兼容性更好，因为不需要服务器端处理路径。
   >
   > 缺点：`URL`带有`#`不太美观，且在`SEO`优化方面相对较差。
   >
   > ```js
   > const router = createRouter({
   >   	history:createWebHashHistory(), //hash模式
   >   	/******/
   > })
   > ```

#### to的两种写法

```js
<!-- 第一种：to的字符串写法 -->
<router-link active-class="active" to="/home">主页</router-link>

<!-- 第二种：to的对象写法 -->
<router-link active-class="active" :to="{path:'/home'}">Home</router-link>
```

#### 命名路由

作用：可以简化路由跳转及传参（后面就讲）。

给路由规则命名：

```js
routes:[
  {
    name:'zhuye',
    path:'/home',
    component:Home
  },
  {
    name:'xinwen',
    path:'/news',
    component:News,
  },
  {
    name:'guanyu',
    path:'/about',
    component:About
  }
]
```

跳转路由：

```js
<!--简化前：需要写完整的路径（to的字符串写法） -->
<!--to写法(通过路径）-->
<router-link to="/news/detail">跳转</router-link>

<!--简化后：直接通过名字跳转（to的对象写法配合name属性） -->
<!--:to写法(通过名字）-->
<router-link :to="{name:'guanyu'}">跳转</router-link>
<!--:to写法(通过路径）-->
<router-link :to="{path:'/about'}">跳转</router-link>
```

#### 嵌套路由

1. 编写`News`的子路由：`Detail.vue`

2. 配置路由规则，使用`children`配置项：

   ```js
   const router = createRouter({
     history:createWebHistory(),
   	routes:[
   		{
   			name:'zhuye',
   			path:'/home',
   			component:Home
   		},
   		{
   			name:'xinwen',
   			path:'/news',
   			component:News,
   			children:[
   				{
   					name:'xiang',
   					path:'detail',
   					component:Detail
   				}
   			]
   		},
   		{
   			name:'guanyu',
   			path:'/about',
   			component:About
   		}
   	]
   })
   export default router
   ```

3. 跳转路由（记得要加完整路径）：

   ```js
   <router-link to="/news/detail">xxxx</router-link>
   <!-- 或 -->
   <router-link :to="{path:'/news/detail'}">xxxx</router-link>
   ```

4. 记得去`Home`组件中预留一个`<router-view>`

   ```vue
   <template>
     <div class="news">
       <nav class="news-list">
         <RouterLink v-for="news in newsList" :key="news.id" :to="{path:'/news/detail'}">
           {{news.name}}
         </RouterLink>
       </nav>
       <div class="news-detail">
         <RouterView/>
       </div>
     </div>
   </template>
   ```

#### 路由传参

### query参数

1. 传递参数

   ```js
   <!-- 跳转并携带query参数（to的字符串写法） -->
   <router-link to="/news/detail?a=1&b=2&content=欢迎你">
   	跳转
   </router-link>
   				
   <!-- 跳转并携带query参数（to的对象写法） -->
   <RouterLink 
     :to="{
       //name:'xiang', //用name也可以跳转
       path:'/news/detail',
       query:{
         id:news.id,
         title:news.title,
         content:news.content
       }
     }"
   >
     {{news.title}}
   </RouterLink>
   ```

2. 接收参数：

   ```js
   import {useRoute} from 'vue-router'
   const route = useRoute()
   // 打印query参数
   console.log(route.query)
   ```

### params参数

1. 传递参数

   ```js
   <!-- 跳转并携带params参数（to的字符串写法） -->
   <RouterLink :to="`/news/detail/001/新闻001/内容001`">{{news.title}}</RouterLink>
   				
   <!-- 跳转并携带params参数（to的对象写法） -->
   <RouterLink 
     :to="{
       name:'xiang', //用name跳转
       params:{
         id:news.id,
         title:news.title,
         content:news.title
       }
     }"
   >
     {{news.title}}
   </RouterLink>
   ```

2. 接收参数：

   ```js
   import {useRoute} from 'vue-router'
   const route = useRoute()
   // 打印params参数
   console.log(route.params)
   ```

> 备注1：传递`params`参数时，若使用`to`的对象写法，必须使用`name`配置项，不能用`path`。
>
> 备注2：传递`params`参数时，需要提前在规则中占位。

#### 路由的props配置

作用：让路由组件更方便的收到参数（可以将路由参数作为`props`传给组件）

```js
{
	name:'xiang',
	path:'detail/:id/:title/:content',
	component:Detail,

  // props的对象写法，作用：把对象中的每一组key-value作为props传给Detail组件
  // props:{a:1,b:2,c:3}, 

  // props的布尔值写法，作用：把收到了每一组params参数，作为props传给Detail组件
  // props:true
  
  // props的函数写法，作用：把返回的对象中每一组key-value作为props传给Detail组件
  props(route){
    return route.query
  }
}
```

#### replace属性

1. 作用：控制路由跳转时操作浏览器历史记录的模式。

2. 浏览器的历史记录有两种写入方式：分别为`push`和`replace`：

   - `push`是追加历史记录（默认值）。
   - `replace`是替换当前记录。

3. 开启`replace`模式：

   ```js
   <RouterLink replace .......>News</RouterLink>
   ```

#### 编程式导航

路由组件的两个重要的属性：`$route`和`$router`变成了两个`hooks`

```js
import {useRoute,useRouter} from 'vue-router'

const route = useRoute()
const router = useRouter()

console.log(route.query)
console.log(route.parmas)
console.log(router.push)
console.log(router.replace)
```

#### 重定向

1. 作用：将特定的路径，重新定向到已有路由。

2. 具体编码：

   ```js
   {
       path:'/',
       redirect:'/about'
   }
   ```


## vue pinia

[Pinia](https://pinia.web3doc.top/introduction.html) 是 Vue 的存储库，它允许您跨组件/页面共享状态。

### 安装

1、用你最喜欢的包管理器安装 `pinia`：

```bash
yarn add pinia
# 或者使用 npm
npm install pinia
```

2、新建`store/index.js`

```js
import { createPinia } from 'pinia'

const store = createPinia()
export default store
```

3、`main.js`中引入

```js
import store from './store'
const app = createApp(App)
app.use(store)
```

### 定义和使用store

1、定义store

在`store/modules`下新建`count.js`

```js
// 引入defineStore用于创建store
import { defineStore } from 'pinia'

// 定义并暴露一个store
export const useCountStore = defineStore('count', {
    // 动作
    actions: {},
    // 状态
    state() {
        return {
            count: 6
        }
    },
    // 计算
    getters: {}
})
```

2、使用store

在` views`下新建`TestStore.vue`

```vue
<template>
  <h2>当前count为：{{ countStore.count }}</h2>

  <div>
    <button @click="changeCount">change count</button>
  </div>
</template>

<script setup name="Count">
  // 引入对应的useXxxxxStore	
  import {useCountStore} from '@/store/modules/count'
  
  // 调用useXxxxxStore得到对应的store
  const countStore = useCountStore()

  const changeCount = () => {
    countStore.count++
  }
</script>
```

#### 修改store里的数据

1、第一种修改方式，直接修改

```js
const changeCount = () => {
  countStore.count++
}
```

2、第二种修改方式：批量修改

```js
countStore.$patch({
  count: 999
})
```

3、第三种修改方式：借助`action`修改（`action`中可以编写一些业务逻辑）

```js
// action {} 里面加入下面的方法
actions: {
    // action {} 里面加入下面的方法
    increment(value) {
        //操作countStore中的sum
        this.count += value
    },
    //减
    decrement(value) {
        this.count -= value
    }
}
```

并使用action里的方法

```js
countStore.increment(10)
```

### storeToRefs

- 借助`storeToRefs`将`store`中的数据转为`ref`对象，方便在模板中使用。
- 注意：`pinia`提供的`storeToRefs`只会将数据做转换，而`Vue`的`toRefs`会转换`store`中数据。

```js
import { storeToRefs } from 'pinia'

// 调用useXxxxxStore得到对应的store
const countStore = useCountStore();
const {count} = storeToRefs(countStore)
```

### getters

当`state`中的数据，需要经过处理后再使用时，可以使用`getters`配置。

```js
getters: {
    doubleCount: (state) => state.count * 2,
    tripleCount() {
        return this.count * 3
    }
}
```

在vue中使用

```vue
let { doubleCount, tripleCount } = storeToRefs(countStore);
<h2>当前 double count为：{{ doubleCount }}</h2>
<h2>当前 triple count为：{{ tripleCount }}</h2>
```

### 订阅状态

可以通过 store 的 `$subscribe()` 方法查看状态及其变化，类似于 Vuex 的 [subscribe 方法](https://vuex.vuejs.org/api/#subscribe)。 与常规的 `watch()` 相比，使用 `$subscribe()` 的优点是 *subscriptions* 只会在 *patches* 之后触发一次（例如，当使用上面的函数版本时）。

在`TestStore.vue`的script里添加以下订阅

```js
countStore.$subscribe((mutation, state) => {
  console.log(mutation, state)

  // 每当它发生变化时，将整个状态持久化到本地存储
  localStorage.setItem('count', JSON.stringify(state))
})
```

当count变化时，可以查看localStorage的数据变化情况。

### store组合式写法

在`store/modules`下新建`user.js`

```js
// 引入defineStore用于创建store
import { defineStore } from 'pinia'
import { ref, computed } from "vue";

// 定义并暴露一个store
export const useUserStore = defineStore('user', () => {
    const name = ref("zs")


    const computedName = computed(() => name.value + "computed");

    const changeName = () => {
        name.value = 'lisi'
    }
    return { name, computedName, changeName }
})
```

组合式在template里的使用

```vue
import { useUserStore } from "@/store/modules/user";

const userStore = useUserStore();

const { name, computedName } = storeToRefs(userStore);
const { changeName } = userStore;

<h2>当前 user name 为：{{ name }}</h2>
<h2>当前 user computed name 为：{{ computedName }}</h2>
<div>
  <button @click="changeName">change name</button>
</div>
```

### store的持久化

`pinia` 和 `vuex` 一样，数据是短时的，只要一刷新页面，数据就会恢复成初始状态（因为pinina的数据是存储在内存中的），为了避免这个问题，可以对其采用持久化保存方法, 使用官方推荐的插件([pinia-plugin-persistedstate](https://prazdevs.github.io/pinia-plugin-persistedstate/zh/guide/why.html))去实现持久化存储。
pinia的数据是存储在内存中的，`pinia-plugin-persistedstate`插件数据默认是存储在`localStorage`中。

当然，我们也可以不使用插件，比如 [VueUse](https://vueuse.org/) 的 `useLocalStorage`：

```js
import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'

defineStore('store', () => {
  const someState = useLocalStorage('stored-state', 'initialValue')

  return { someState }
})
```

>  为什么需要该插件？
>
> `pinia-plugin-persistedstate` 旨在通过一致的 API 为每个人和每个项目中的 Pinia Store 提供持久化存储。如果你希望保存一个完整的 Store，或者需要细粒化配置 storage 和序列化的方式，该插件都为你提供了相应的功能，并且可以在你想要持久化的 Store 上使用相同的配置。

#### 1、安装

```bash
npm install pinia-plugin-persistedstate
```

在`store/index.js`中引入。

```js
import { createPinia } from 'pinia'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const store = createPinia()

store.use(piniaPluginPersistedstate)
export default store
```

#### 2、所有 Store 都默认开启持久化存储

该配置将会使所有 Store 持久化存储，且必须配置 `persist: false` 显式禁用持久化。

```js
import { createPinia } from 'pinia'


import { createPersistedState } from 'pinia-plugin-persistedstate'

const store = createPinia()

// 全局配置所有store持久化
store.use(createPersistedState({
    auto: true,
}))
export default store
```

单独配置某一个store不持久化。

**选项式语法**

```js
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => {
    return {
      someState: '你好 pinia',
    }
  },
  persist: true,
})
```

**组合式语法**

```js
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => {
    return {
      someState: '你好 pinia',
    }
  },
  persist: true,
})
```

#### 3、默认保存

下面这种写法会将当前模块中的所有数据都进行持久化保存，默认保存在 [`localStorage`](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAPI%2FWindow%2FlocalStorage)中， `key` 为模块 `id`，刷新页面不需要手动读取数据，插件会自动读取

```js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: null,
    age: null,
    sex: null,
  }),
  
  persist: true, // true 表示开启持久化保存
})
```

#### 4、设置 key 、指定保存内容

你可以主动设置 `key` 名，也可以指定哪些数据保存，默认会保存当前模块全部数据。

```js
export const useUserStore = defineStore('storeUser', {
  state: () => ({
    name: null,
    age: null,
    sex: null,
    save: { 
        me: 'saved',
        notMe: 'not-saved',
    },
  }),
  
  persist: { 
      key: 'storeUser', 
      paths: ['save.me', 'saveMeToo'],
  },
})
```

该 store 中, 数据将被持久化存储在 `localStorage` 中的 `storeUser` key 中。同时只有 `save.me` 和 `name` 被持久化，而其他的state不会被持久化。

你甚至可以对不同数据设置不同的本地存储方式。

```js
export const useUserStore = defineStore('storeUser', {
  state: () => ({
    name: null,
    age: null,
    sex: null,
  }),
  
  persist: [  
    {  
      paths: ['name'],  
      storage: localStorage,  
    },  
    {  
      paths: ['age'],  
      storage: sessionStorage,  
    },  
  ]
  
})
```

上述例子中， name 的值将保存在 localStorage 中，而 age 的值将保留在 sessionStorage 中，sex 则不会持久化。

#### 5、保存到 cookie

保存到 `cookie` 中当然也是可以的，不过需要手动添加 `cookie` 的保存方式，同样，此处也是推荐使用插件 [js-cookie](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fjs-cookie%2Fjs-cookie) 来完成。

```bash
npm install js-cookie
```

```js
import Cookies from 'js-cookie'

// 手动添加cookie
const cookiesStorage: Storage = {
  setItem (key, state) {
    // 设置有效期 3 天，不设置默认同 sessionStorage 有效期一致
    return Cookies.set(key, state.accessToken, { expires: 3 }) 
  },
  getItem (key) {
    return JSON.stringify({
      accessToken: Cookies.get(key),
    })
  },
}

export const useUserStore = defineStore('storeUser', {
  state: () => ({
    name: null,
    age: null,
    sex: null,
    accessToken: 'xxxxxxxxx',
  }),
  persist: {
    storage: cookiesStorage, // 使用手动添加的cookie
    paths: ['accessToken'] // cookie 一般用来保存 token
  },
})
```
## vite
`vite` 是新一代前端构建工具，官网地址：[https://vitejs.cn](https://gitee.com/link?target=https%3A%2F%2Fvitejs.cn%2F)，`vite`的优势如下：
- 轻量快速的热重载（`HMR`），能实现极速的服务启动。
- 对 `TypeScript`、`JSX`、`CSS` 等支持开箱即用。
- 真正的按需编译，不再等待整个应用编译完成。
- `webpack`构建 与 `vite`构建对比图如下：

  ![webpack构建](assets/1683167182037-71c78210-8217-4e7d-9a83-e463035efbbe.png)

  ![vite构建](assets/1683167204081-582dc237-72bc-499e-9589-2cdfd452e62f.png)

总结：
- `Vite` 项目中，`index.html` 是项目的入口文件，在项目最外层。
- 加载`index.html`后，`Vite` 解析 `<script type="module" src="xxx">` 指向的`JavaScript`。
- `Vue3`**中是通过 **`createApp` 函数创建一个应用实例。
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vite App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

`vite`的配置文件在`vite.config.js`中。

### 配置alias

```js
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
  }
}
```

### 配置server

```js
server: {
  host: 'localhost',
  port: 8888
}
```

参考server端配置：https://cn.vitejs.dev/config/server-options

### 环境变量

Vite 在一个特殊的 **`import.meta.env`** 对象上暴露环境变量，这些变量在构建时会被静态地替换掉。这里有一些在所有情况下都可以使用的内建变量：

- **`import.meta.env.MODE`**: 应用运行的[模式](https://cn.vitejs.dev/guide/env-and-mode.html#modes)。
- **`import.meta.env.BASE_URL`**: 部署应用时的基本 URL。他由[`base` 配置项](https://cn.vitejs.dev/config/shared-options.html#base)决定。
- **`import.meta.env.PROD`**: 应用是否运行在生产环境（使用 `NODE_ENV='production'` 运行开发服务器或构建应用时使用 `NODE_ENV='production'` ）。
- **`import.meta.env.DEV`**: 应用是否运行在开发环境 (永远与 `import.meta.env.PROD`相反)。
- **`import.meta.env.SSR`**: 应用是否运行在 [server](https://cn.vitejs.dev/guide/ssr.html#conditional-logic) 上。

#### `.env` 文件[](https://cn.vitejs.dev/guide/env-and-mode#env-files)

Vite 使用 [dotenv](https://github.com/motdotla/dotenv) 从你的 [环境目录](https://cn.vitejs.dev/config/shared-options.html#envdir) 中的下列文件加载额外的环境变量：

```
.env                # 所有情况下都会加载
.env.local          # 所有情况下都会加载，但会被 git 忽略
.env.[mode]         # 只在指定模式下加载
.env.[mode].local   # 只在指定模式下加载，但会被 git 忽略
```

为了防止意外地将一些环境变量泄漏到客户端，只有以 `VITE_` 为前缀的变量才会暴露给经过 vite 处理的代码。例如下面这些环境变量：

```env
VITE_SOME_KEY=123
DB_PASSWORD=foobar
VITE_API_PORT=9001
```

我们直接在package.json中配置命令 **"test": "vite --mode test"**

新建`.env.test`配置文件。

```env
VITE_SOME_KEY=123-test
DB_PASSWORD=foobar
VITE_API_PORT=9000
```

重新启动程序，会看到**VITE_API_PORT**的值是9000。


## mock api

### 安装

```bash
npm i vite-plugin-mock -D
npm i mockjs
```

### 配置vite.config.js

```js
import { viteMockServe } from 'vite-plugin-mock'

import vue from '@vitejs/plugin-vue'

export default ({ command }) => {
  let prodMock = true
  return {
    plugins: [
      vue(),
      viteMockServe({
        mockPath: 'mock',
        enable: true,
      }),
    ],
  }
}
```

在项目目录新建mock文件夹。

创建`test.js`

```js
// test.js 仅做示例: 通过GET请求返回一个名字数组
export default [
    {
      url: "/api/test",
      method: "get",
      response: () => {
        return {
          code: 200,
          message: "ok",
          data: ["hello", "world"]
        };
      }
    }
  ];
```



参考: https://github.com/vbenjs/vite-plugin-mock

## test

==官方测试文档==：https://cn.vuejs.org/guide/scaling-up/testing.html

## Vue3组件库

- [Ant Design Vue](https://antdv.com/docs/vue/introduce-cn/)
- [Vant4](https://vant-ui.github.io/vant/#/zh-CN)
- [element-plus](https://element-plus.org/zh-CN/component/overview.html)
- [Element3](https://github.com/hug-sun/element3)
- [naive-ui](https://github.com/tusen-ai/naive-ui)
- [quasar](https://github.com/quasarframework/quasar)
- [arco.design](https://arco.design/vue/docs/start)
- [vuetify](https://github.com/vuetifyjs/vuetify)
- [nutui](https://nutui.jd.com/#/)

## Vue3 工具、插件

- [vueuse](https://vueuse.org/): 组合式API工具类
- [vue-cropper](https://vue-cropper.vercel.app/#/guide): vue3图片裁剪库

## 参考文档

- https://gitee.com/marina-37/vue3_vite_ts/blob/master/ReadMe.md#1-vue3%E7%AE%80%E4%BB%8B
- https://github.com/chengpeiquan/learning-vue3/blob/main/docs/guide.md
- [vue3相关资料](https://vue3js.cn/)


