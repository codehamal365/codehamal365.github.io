---
title: Rust 快速参考手册
categories:
  - Rust
tags:
  - Rust
  - Cheatsheet
  - 速查
---

# Rust 快速参考手册

> 常用语法和概念速查表

---

## 📋 目录

- [基础语法](#基础语法)
- [数据类型](#数据类型)
- [函数](#函数)
- [控制流](#控制流)
- [所有权](#所有权)
- [错误处理](#错误处理)
- [并发](#并发)
- [高级特性](#高级特性)

---

## 基础语法

### Hello World

```rust
fn main() {
    println!("Hello, Rust!");
}
```

### 变量与可变性

```rust
// 不可变变量
let x = 5;

// 可变变量
let mut y = 10;
y = 20;

// 常量
const MAX_POINTS: u32 = 100_000;

// 重新绑定
let z = 5;
let z = z + 1;  // shadowing
```

### 注释

```rust
// 单行注释

/* 多行注释 */

/// 文档注释
/// # Examples
/// ```
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## 数据类型

### 标量类型

| 类型 | 范围 | 示例 |
|------|------|------|
| `i8` | -128 ~ 127 | `let x: i8 = -128;` |
| `u8` | 0 ~ 255 | `let x: u8 = 255;` |
| `i32` | -2^31 ~ 2^31-1 | `let x: i32 = 2_147_483_647;` |
| `u32` | 0 ~ 2^32-1 | `let x: u32 = 4_294_967_295;` |
| `i64` | -2^63 ~ 2^63-1 | `let x: i64 = 9_223_372_036_854_775_807;` |
| `u64` | 0 ~ 2^64-1 | `let x: u64 = 18_446_744_073_709_551_615;` |
| `f32` | 单精度浮点数 | `let x: f32 = 3.14;` |
| `f64` | 双精度浮点数 | `let x: f64 = 3.141592653589793;` |
| `bool` | true/false | `let x: bool = true;` |
| `char` | Unicode 标量值 | `let x: char = 'A';` |

### 复合类型

```rust
// 元组
let tup: (i32, f64, u8) = (500, 6.4, 1);
let (x, y, z) = tup;
let five_hundred = tup.0;

// 数组
let a: [i32; 5] = [1, 2, 3, 4, 5];
let first = a[0];
let b = [3; 5];  // [3, 3, 3, 3, 3]

// 字符串切片
let s: &str = "Hello";
let s2: &'static str = "Static lifetime";

// String 类型
let mut s = String::from("hello");
s.push_str(", world!");
```

### 结构体

```rust
// 命名字段结构体
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// 元组结构体
struct Color(i32, i32, i32);
struct Point(i32, i32);

// 单元结构体
struct AlwaysEqual;

// 示例
let user1 = User {
    username: String::from("someusername123"),
    email: String::from("someone@example.com"),
    sign_in_count: 1,
    active: true,
};
```

### 枚举

```rust
enum IpAddrKind {
    V4,
    V6,
}

enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

// 带数据的枚举
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

// 方法实现
impl Message {
    fn call(&self) {
        // 方法体
    }
}
```

### Option 和 Result

```rust
// Option<T> - 可能有值的类型
let some_number: Option<i32> = Some(5);
let absent_number: Option<i32> = None;

// Result<T, E> - 可能出错的类型
use std::fs::File;
let f = File::open("hello.txt");
let f: Result<File, std::io::Error> = match f {
    Ok(file) => file,
    Err(error) => panic!("Problem opening file: {:?}", error),
};
```

---

## 函数

### 基本函数

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b  // 无需 return
}

// 多个语句
fn add_with_log(a: i32, b: i32) -> i32 {
    println!("Adding {} and {}", a, b);
    a + b
}
```

### 函数参数

```rust
// 不可变引用
fn calculate_length(s: &String) -> usize {
    s.len()
}

// 可变引用
fn change(some_string: &mut String) {
    some_string.push_str(", world");
}

// 所有权转移
fn takes_ownership(some_string: String) {
    println!("{}", some_string);
}  // some_string 被丢弃
```

### 闭包

```rust
// 基本闭包
let add_one = |x: i32| x + 1;
assert_eq!(2, add_one(1));

// 捕获环境
let y = 10;
let closure = |x| x + y;

// 闭包类型推断
let example_closure = |x| x;
let s = example_closure(String::from("hello"));
// let n = example_closure(5);  // 错误！类型不匹配
```

---

## 控制流

### if 表达式

```rust
let number = 6;

if number % 4 == 0 {
    println!("number 能被 4 整除");
} else if number % 3 == 0 {
    println!("number 能被 3 整除");
} else {
    println!("number 不能被 4 或 3 整除");
}

// if 是表达式
let condition = true;
let value = if condition { 5 } else { 6 };
```

### 循环

```rust
// loop 循环
let mut counter = 0;
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
};

// while 循环
let mut number = 3;
while number != 0 {
    println!("{}!", number);
    number -= 1;
}

// for 循环
let a = [10, 20, 30, 40, 50];
for element in a {
    println!("the value is: {}", element);
}

// 范围循环
for number in 1..4 {
    println!("{}", number);
}
```

### match 表达式

```rust
let dice_roll = 9;
match dice_roll {
    1 => println!("Snake eyes!"),
    2 => println!("Two!"),
    3 => println!("Three!"),
    4 => println!("Four!"),
    5 => println!("Five!"),
    6 => println!("Six!"),
    _ => println!("Other number"),
}

// 解构
let point = (3, 5);
match point {
    (0, 0) => println!("Origin point"),
    (x, 0) => println!("On x-axis at {}", x),
    (0, y) => println!("On y-axis at {}", y),
    (x, y) => println!("At ({}, {})", x, y),
}

// if let 简化
let some_value = Some(5);
if let Some(x) = some_value {
    println!("Got value: {}", x);
}
```

---

## 所有权

### 所有权规则

1. Rust 中的每个值都有一个所有者
2. 一次只能有一个所有者
3. 当所有者离开作用域，值将被丢弃

```rust
// 移动
let s1 = String::from("hello");
let s2 = s1;  // s1 不再有效

// 克隆
let s1 = String::from("hello");
let s2 = s1.clone();  // s1 仍然有效
```

### 借用

```rust
// 不可变引用
let s = String::from("hello");
let len = calculate_length(&s);  // 不转移所有权

// 可变引用
let mut s = String::from("hello");
change(&mut s);  // 需要 mut 关键字

// 规则：
// 1. 同一作用域内只能有一个可变引用
// 2. 不可变引用和可变引用不能同时存在
```

### 生命周期

```rust
// 显式生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 结构体生命周期
struct ImportantExcerpt<'a> {
    part: &'a str,
}

// 静态生命周期
fn static_lifetime(s: &'static str) {
    println!("{}", s);
}
```

---

## 错误处理

### panic! vs Result

```rust
// panic! - 不可恢复错误
panic!("crash and burn");

// Result - 可恢复错误
use std::fs::File;
let f = File::open("hello.txt");
let f: Result<File, std::io::Error> = match f {
    Ok(file) => file,
    Err(error) => panic!("Problem opening file: {:?}", error),
};
```

### ? 操作符

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file() -> Result<String, io::Error> {
    let mut file = File::open("hello.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

### 自定义错误

```rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
struct AppError {
    message: String,
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "AppError: {}", self.message)
    }
}

impl Error for AppError {}

impl From<std::io::Error> for AppError {
    fn from(error: std::io::Error) -> Self {
        AppError {
            message: error.to_string(),
        }
    }
}
```

---

## 并发

### 线程

```rust
use std::thread;
use std::time::Duration;

let handle = thread::spawn(|| {
    for i in 1..5 {
        println!("Hi number {} from the spawned thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
});

handle.join().unwrap();
```

### 消息传递

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send(String::from("hi")).unwrap();
});

let received = rx.recv().unwrap();
println!("Got: {}", received);
```

### 共享状态

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

### 异步

```rust
use std::future::Future;

async fn fetch_data() -> String {
    // 异步操作
    String::from("Data")
}

#[tokio::main]
async fn main() {
    let data = fetch_data().await;
    println!("Fetched: {}", data);
}
```

---

## 高级特性

### Traits

```rust
// 定义 trait
trait Summary {
    fn summarize(&self) -> String;
}

// 实现 trait
struct NewsArticle {
    headline: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}", self.headline)
    }
}

// trait 作为参数
fn notify(item: &impl Summary) {
    println!("{}", item.summarize());
}

// trait bound
fn notify_bound<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}
```

### 泛型

```rust
// 泛型函数
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// 泛型结构体
struct Point<T> {
    x: T,
    y: T,
}

// 方法中的泛型
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

### 宏

```rust
// 声明宏
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

// 使用
let v = vec![1, 2, 3];
```

### 生命周期高级

```rust
// 静态生命周期
static STATIC_STRING: &str = "I have a static lifetime";

// 生命周期省略规则
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap()
}
```

---

## 模块系统

### 模块定义

```rust
// src/lib.rs
pub mod network {
    pub mod http {
        pub fn get(url: &str) -> String {
            format!("GET {}", url)
        }
    }
}

// 使用
use network::http::get;
```

### 可见性

```rust
mod private_module {
    fn private_function() {
        println!("private");
    }

    pub fn public_function() {
        println!("public");
    }
}
```

---

## 测试

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    #[should_panic]
    fn test_panic() {
        panic!("This test should panic");
    }

    #[test]
    fn test_result() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err(String::from("Math is broken"))
        }
    }
}
```

---

## 常用 Crate

| Crate | 用途 | 示例 |
|-------|------|------|
| `serde` | 序列化/反序列化 | `#[derive(Serialize, Deserialize)]` |
| `tokio` | 异步运行时 | `#[tokio::main]` |
| `clap` | 命令行解析 | `#[derive(Parser)]` |
| `reqwest` | HTTP 客户端 | `reqwest::get(url).await?` |
| `sqlx` | 数据库操作 | `sqlx::query("SELECT * FROM users")` |
| `rand` | 随机数 | `rand::random::<i32>()` |
| `regex` | 正则表达式 | `Regex::new(r"^\d{4}-\d{2}-\d{2}$")` |
| `chrono` | 日期时间 | `Utc::now()` |
| `rayon` | 并行计算 | `numbers.par_iter().sum()` |
| `crossbeam` | 无锁并发 | `crossbeam::channel::unbounded()` |

---

## 性能提示

### 避免不必要的克隆

```rust
// 不好
fn process(s: String) -> String {
    s.clone()  // 不必要的克隆
}

// 好
fn process(s: &str) -> String {
    s.to_uppercase()  // 直接处理
}
```

### 使用迭代器

```rust
// 不好
let mut sum = 0;
for &x in &numbers {
    sum += x;
}

// 好
let sum: i32 = numbers.iter().sum();
```

### 使用 Cow

```rust
use std::borrow::Cow;

fn process_or_keep<'a>(input: &'a str, uppercase: bool) -> Cow<'a, str> {
    if uppercase {
        Cow::Owned(input.to_uppercase())
    } else {
        Cow::Borrowed(input)
    }
}
```

---

## 常见错误

### 1. 所有权错误

```rust
let s = String::from("hello");
let s2 = s;
// println!("{}", s);  // 错误！s 已经移动
```

### 2. 可变引用错误

```rust
let mut s = String::from("hello");
let r1 = &mut s;
// let r2 = &mut s;  // 错误！不能同时有多个可变引用
```

### 3. 生命周期错误

```rust
fn dangling() -> &String {
    let s = String::from("hello");
    &s  // 错误！返回局部变量的引用
}
```

### 4. 类型推断错误

```rust
let v = vec![1, 2, 3];
// let x = v[0];  // 错误！需要指定类型
```

---

## 调试技巧

### 打印调试

```rust
println!("x = {:?}", x);  // Debug trait
println!("x = {:#?}", x);  // 格式化输出
```

### 使用 dbg!

```rust
let x = 5;
let y = dbg!(x * 2) + 1;
// 输出: [src/main.rs:2] x * 2 = 10
```

### 使用 assert

```rust
assert!(x > 0);
assert_eq!(x, 5);
assert_ne!(x, 10);
```

---

## 总结

### 核心概念
1. **所有权** - 所有者、借用、生命周期
2. **类型系统** - 静态类型、泛型、Traits
3. **错误处理** - Result、panic、? 操作符
4. **并发** - 线程、消息传递、共享状态

### 最佳实践
1. 使用 `clippy` 检查代码
2. 编写测试
3. 使用文档注释
4. 避免不必要的克隆
5. 使用迭代器而不是循环

### 学习路径
1. 基础语法 → 2. 所有权 → 3. 错误处理 → 4. 并发 → 5. 高级特性

---

**保持练习，Rust 会越来越简单！** 🦀