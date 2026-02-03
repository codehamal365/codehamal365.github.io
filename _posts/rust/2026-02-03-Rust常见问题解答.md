---
title: Rust 常见问题解答
categories:
  - Rust
tags:
  - Rust
  - FAQ
  - 问题解答
---

# Rust 常见问题解答

> 集中解答学习 Rust 过程中的常见问题

---

## 📋 目录

- [基础问题](#基础问题)
- [所有权系统](#所有权系统)
- [错误处理](#错误处理)
- [并发编程](#并发编程)
- [高级特性](#高级特性)
- [性能问题](#性能问题)
- [工具链](#工具链)
- [最佳实践](#最佳实践)

---

## 基础问题

### Q1: Rust 是什么？为什么选择 Rust？

**A:** Rust 是一门系统编程语言，具有以下特点：

- **内存安全**：编译时防止内存错误，无需垃圾回收
- **并发安全**：所有权系统防止数据竞争
- **高性能**：接近 C/C++ 的性能
- **开发者友好**：优秀的编译器错误提示

**适合场景**：
- 系统编程（操作系统、驱动程序）
- Web 服务（高性能后端）
- 命令行工具
- 嵌入式开发
- 游戏开发
- 区块链

### Q2: Rust 和 C/C++ 有什么区别？

**A:**

| 特性 | Rust | C/C++ |
|------|------|-------|
| 内存管理 | 所有权系统 | 手动管理/智能指针 |
| 安全性 | 编译时保证 | 运行时检查 |
| 并发 | Fearless concurrency | 需要手动同步 |
| 学习曲线 | 陡峭 | 中等 |
| 生态系统 | 现代化 | 成熟但复杂 |
| 性能 | 接近 C/C++ | 接近 Rust |

### Q3: Rust 的学习曲线如何？

**A:** Rust 的学习曲线确实比较陡峭，主要难点在于：

1. **所有权系统**：需要改变编程思维
2. **生命周期**：需要理解引用的生命周期
3. **错误处理**：Result 类型的使用

**建议**：
- 从基础开始，不要跳过概念
- 多写代码，多练习
- 阅读官方书籍
- 参与社区讨论

### Q4: 需要 C/C++ 背景吗？

**A:** 不需要。Rust 可以从零开始学习，但了解以下概念有帮助：

- 基本的编程概念（变量、函数、控制流）
- 内存管理的基本概念（栈、堆）
- 系统编程的基本概念

### Q5: Rust 适合初学者吗？

**A:** 适合，但需要耐心。Rust 的编译器错误信息非常友好，会指导你如何修复问题。建议：

1. 从 Rustlings 开始练习
2. 阅读官方书籍
3. 构建小项目
4. 参与社区

---

## 所有权系统

### Q6: 什么是所有权？为什么需要它？

**A:** 所有权是 Rust 的核心特性，用于管理内存和防止数据竞争。

**规则**：
1. Rust 中的每个值都有一个所有者
2. 一次只能有一个所有者
3. 当所有者离开作用域，值将被丢弃

**好处**：
- 无需垃圾回收
- 编译时防止内存错误
- 保证并发安全

### Q7: 为什么我的变量"移动"后就不能用了？

**A:** 这是所有权转移（move）的正常行为。

```rust
let s1 = String::from("hello");
let s2 = s1;  // s1 的所有权转移到 s2
// println!("{}", s1);  // 错误！s1 已经无效
```

**解决方法**：
- 使用克隆：`let s2 = s1.clone();`
- 使用引用：`let s2 = &s1;`
- 重新设计代码结构

### Q8: 借用和引用有什么区别？

**A:**

- **引用**：指向值的指针，不拥有值
- **借用**：使用引用的过程

```rust
let s = String::from("hello");
let len = calculate_length(&s);  // 借用 s
println!("Length of '{}' is {}", s, len);  // s 仍然有效
```

### Q9: 为什么不能同时有多个可变引用？

**A:** 这是 Rust 的安全保证机制。规则：

1. 同一作用域内只能有一个可变引用
2. 不可变引用和可变引用不能同时存在

```rust
let mut s = String::from("hello");
let r1 = &mut s;
// let r2 = &mut s;  // 错误！不能同时有多个可变引用
```

**好处**：防止数据竞争和悬垂指针。

### Q10: 生命周期是什么？为什么需要它？

**A:** 生命周期是 Rust 确保引用有效的机制。

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

**为什么需要**：
- 防止悬垂引用
- 确保引用在使用时有效
- 编译时检查

### Q11: 生命周期省略规则是什么？

**A:** Rust 编译器自动推断生命周期的规则：

1. 每个引用参数都有一个生命周期参数
2. 如果只有一个输入生命周期参数，那么它被赋予所有输出生命周期参数
3. 如果有多个输入生命周期参数，但其中一个是 `&self` 或 `&mut self`，那么 `self` 的生命周期被赋予所有输出生命周期参数

```rust
// 省略前
fn first_word<'a>(s: &'a str) -> &'a str {
    s.split_whitespace().next().unwrap()
}

// 省略后
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap()
}
```

---

## 错误处理

### Q12: panic! 和 Result 有什么区别？

**A:**

- **panic!**：不可恢复错误，程序会终止
- **Result**：可恢复错误，程序可以继续运行

```rust
// panic!
panic!("Something went wrong!");

// Result
let f = File::open("hello.txt");
let f: Result<File, std::io::Error> = match f {
    Ok(file) => file,
    Err(error) => panic!("Problem opening file: {:?}", error),
};
```

**使用场景**：
- panic!：测试、原型开发、不可恢复的错误
- Result：生产环境、可恢复的错误

### Q13: ? 操作符是什么？如何使用？

**A:** `?` 操作符是错误传播的语法糖。

```rust
fn read_file() -> Result<String, std::io::Error> {
    let mut file = File::open("hello.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

**工作原理**：
- 如果是 `Ok(value)`，返回 `value`
- 如果是 `Err(error)`，提前返回 `Err(error)`

### Q14: 如何自定义错误类型？

**A:**

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

### Q15: 如何处理多个错误类型？

**A:** 使用 `Box<dyn Error>` 或自定义错误枚举。

```rust
use std::error::Error;

fn process() -> Result<(), Box<dyn Error>> {
    let data = std::fs::read_to_string("config.txt")?;
    let parsed: serde_json::Value = serde_json::from_str(&data)?;
    println!("{:?}", parsed);
    Ok(())
}
```

---

## 并发编程

### Q16: Rust 如何保证并发安全？

**A:** 通过所有权系统和类型系统：

1. **所有权**：确保数据只有一个所有者
2. **借用规则**：防止数据竞争
3. **Send 和 Sync trait**：标记类型是否可以在线程间传递

```rust
// Send: 可以在线程间传递所有权
// Sync: 可以在线程间共享引用
```

### Q17: 线程和异步有什么区别？

**A:**

| 特性 | 线程 | 异步 |
|------|------|------|
| 并发模型 | 抢占式 | 协作式 |
| 内存开销 | 大（每个线程 ~2MB） | 小（任务 ~几百字节） |
| 上下文切换 | 操作系统级 | 用户态 |
| 适用场景 | CPU 密集型 | I/O 密集型 |
| 编程模型 | 多线程 | 单线程多任务 |

### Q18: 什么时候使用线程，什么时候使用异步？

**A:**

**使用线程**：
- CPU 密集型任务
- 需要真正的并行
- 简单的并发模型

**使用异步**：
- I/O 密集型任务（网络、文件）
- 需要高并发
- 资源受限的环境

### Q19: 如何避免死锁？

**A:**

1. **锁顺序**：总是按相同顺序获取锁
2. **超时**：使用带超时的锁
3. **避免嵌套锁**：尽量减少锁的持有时间
4. **使用无锁数据结构**：如 `crossbeam`

```rust
use std::sync::{Mutex, Arc};
use std::thread;
use std::time::Duration;

// 好的做法：按顺序获取锁
let lock1 = Arc::new(Mutex::new(0));
let lock2 = Arc::new(Mutex::new(0));

let lock1_clone = Arc::clone(&lock1);
let lock2_clone = Arc::clone(&lock2);

thread::spawn(move || {
    let _guard1 = lock1_clone.lock().unwrap();
    thread::sleep(Duration::from_millis(10));
    let _guard2 = lock2_clone.lock().unwrap();
    // 处理数据
});
```

### Q20: Arc 和 Rc 有什么区别？

**A:**

- **Rc**：引用计数，单线程安全
- **Arc**：原子引用计数，多线程安全

```rust
use std::rc::Rc;
use std::sync::Arc;

// 单线程
let rc = Rc::new(vec![1, 2, 3]);
let rc_clone = Rc::clone(&rc);

// 多线程
let arc = Arc::new(vec![1, 2, 3]);
let arc_clone = Arc::clone(&arc);
```

**选择**：
- 单线程：使用 `Rc`
- 多线程：使用 `Arc`

---

## 高级特性

### Q21: Traits 是什么？有什么用？

**A:** Traits 是 Rust 的接口系统，用于定义共享行为。

```rust
trait Summary {
    fn summarize(&self) -> String;
}

struct NewsArticle {
    headline: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}", self.headline)
    }
}
```

**用途**：
- 定义接口
- 代码复用
- 多态

### Q22: 泛型和 Traits 有什么关系？

**A:** 泛型用于参数化类型，Traits 用于约束泛型。

```rust
// 泛型函数
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    // ...
}

// 多个 trait bound
fn notify<T: Summary + Display>(item: &T) {
    // ...
}

// where 子句
fn notify_where<T, U>(t: &T, u: &U)
where
    T: Summary,
    U: Display,
{
    // ...
}
```

### Q23: 什么是关联类型？

**A:** 关联类型是 Trait 中的类型占位符。

```rust
trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}

struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}
```

### Q24: 宏是什么？什么时候使用？

**A:** 宏是 Rust 的元编程工具，用于在编译时生成代码。

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

**使用场景**：
- 减少样板代码
- 实现领域特定语言 (DSL)
- 编译时计算

### Q25: 如何选择宏和函数？

**A:**

| 特性 | 函数 | 宏 |
|------|------|----|
| 代码生成 | 运行时 | 编译时 |
| 类型检查 | 严格 | 宽松 |
| 调试 | 容易 | 困难 |
| 性能 | 运行时开销 | 无运行时开销 |
| 可读性 | 高 | 低 |

**选择**：
- 优先使用函数
- 宏用于需要元编程的场景
- 避免过度使用宏

---

## 性能问题

### Q26: Rust 的性能如何？

**A:** Rust 的性能接近 C/C++，通常在：

- **编译后性能**：接近 C/C++，比 Go/Python 快 10-100 倍
- **编译速度**：比 C++ 快，但比 Go 慢
- **内存占用**：比带 GC 的语言小

**影响因素**：
- 优化级别（debug/release）
- 内存布局
- 算法选择

### Q27: 如何优化 Rust 代码性能？

**A:**

1. **使用 release 构建**
   ```bash
   cargo build --release
   ```

2. **使用性能分析工具**
   ```bash
   cargo install cargo-flamegraph
   cargo flamegraph
   ```

3. **优化内存布局**
   ```rust
   // 使用 repr(C) 保证内存布局
   #[repr(C)]
   struct Point {
       x: f64,
       y: f64,
   }
   ```

4. **避免不必要的克隆**
   ```rust
   // 不好
   fn process(s: String) -> String {
       s.clone()
   }

   // 好
   fn process(s: &str) -> String {
       s.to_uppercase()
   }
   ```

5. **使用迭代器**
   ```rust
   // 不好
   let mut sum = 0;
   for &x in &numbers {
       sum += x;
   }

   // 好
   let sum: i32 = numbers.iter().sum();
   ```

### Q28: 为什么我的 Rust 程序比 C++ 慢？

**A:** 可能的原因：

1. **没有使用 release 构建**
   ```bash
   cargo build --release  # 忘记 --release
   ```

2. **不必要的边界检查**
   ```rust
   // 使用 get_unchecked 避免边界检查（unsafe）
   unsafe {
       let value = *vec.get_unchecked(i);
   }
   ```

3. **内存分配过多**
   ```rust
   // 使用 Cow 避免不必要的分配
   use std::borrow::Cow;
   let s: Cow<str> = if condition {
       Cow::Owned(String::from("hello"))
   } else {
       Cow::Borrowed("hello")
   };
   ```

4. **算法问题**
   - 检查算法复杂度
   - 使用合适的数据结构

### Q29: Rust 的内存占用如何？

**A:** Rust 的内存占用通常比带 GC 的语言小：

- **栈分配**：无额外开销
- **堆分配**：需要显式使用 `Box`、`Vec` 等
- **零成本抽象**：无运行时开销

**优化技巧**：
- 使用 `&str` 而不是 `String`
- 使用 `Cow` 避免不必要的克隆
- 使用 `Box` 处理大对象

### Q30: 如何减少二进制文件大小？

**A:**

1. **使用 strip**
   ```bash
   strip target/release/myapp
   ```

2. **使用 LTO (Link Time Optimization)**
   ```toml
   # Cargo.toml
   [profile.release]
   lto = true
   ```

3. **使用 panic = "abort"**
   ```toml
   # Cargo.toml
   [profile.release]
   panic = "abort"
   ```

4. **使用 cargo-bloat**
   ```bash
   cargo install cargo-bloat
   cargo bloat --release
   ```

---

## 工具链

### Q31: Cargo 是什么？如何使用？

**A:** Cargo 是 Rust 的包管理器和构建工具。

**常用命令**：
```bash
# 创建新项目
cargo new myapp
cargo new --lib mylib

# 构建项目
cargo build          # debug 构建
cargo build --release # release 构建

# 运行项目
cargo run

# 运行测试
cargo test

# 生成文档
cargo doc

# 更新依赖
cargo update

# 检查代码（不编译）
cargo check
```

### Q32: 如何管理依赖？

**A:** 在 `Cargo.toml` 中管理依赖。

```toml
[dependencies]
# 最新版本
serde = "1.0"

# 精确版本
serde = "=1.0.152"

# 范围版本
serde = ">=1.0, <2.0"

# Git 依赖
serde = { git = "https://github.com/serde-rs/serde", branch = "main" }

# 路径依赖
mylib = { path = "../mylib" }

# 可选依赖
optional_feature = { version = "1.0", optional = true }
```

### Q33: 如何处理版本冲突？

**A:**

1. **使用 cargo tree 查看依赖树**
   ```bash
   cargo tree
   ```

2. **使用 cargo update 更新依赖**
   ```bash
   cargo update
   ```

3. **使用 features 管理可选依赖**
   ```toml
   [features]
   default = ["std"]
   std = []
   ```

4. **使用 cargo deny 检查许可证和版本**
   ```bash
   cargo install cargo-deny
   cargo deny check
   ```

### Q34: 如何调试 Rust 代码？

**A:**

1. **使用 println!**
   ```rust
   println!("x = {:?}", x);
   ```

2. **使用 dbg!**
   ```rust
   let x = 5;
   let y = dbg!(x * 2) + 1;
   ```

3. **使用调试器 (gdb/lldb)**
   ```bash
   cargo build
   gdb target/debug/myapp
   ```

4. **使用 rust-lldb**
   ```bash
   rust-lldb target/debug/myapp
   ```

5. **使用 IDE 支持**
   - VS Code + rust-analyzer
   - IntelliJ Rust

### Q35: 如何格式化代码？

**A:** 使用 rustfmt。

```bash
# 格式化代码
cargo fmt

# 检查格式
cargo fmt -- --check

# 格式化特定文件
cargo fmt -- path/to/file.rs
```

**配置**：在 `.rustfmt.toml` 中配置。

### Q36: 如何检查代码质量？

**A:** 使用 clippy。

```bash
# 运行 clippy
cargo clippy

# 修复建议
cargo clippy --fix

# 严格模式
cargo clippy -- -D warnings
```

**常见建议**：
- 使用 `iter().sum()` 代替循环
- 使用 `&str` 代替 `&String`
- 避免不必要的 `clone()`

---

## 最佳实践

### Q37: Rust 的代码风格是什么？

**A:**

1. **命名规范**
   - 变量：`snake_case`
   - 函数：`snake_case`
   - 类型：`PascalCase`
   - 常量：`SCREAMING_SNAKE_CASE`
   - Traits：`PascalCase`

2. **文件组织**
   ```
   src/
   ├── main.rs          # 二进制入口
   ├── lib.rs           # 库入口
   ├── mod1.rs          # 模块
   ├── mod2/
   │   ├── mod.rs       # 子模块
   │   └── submod.rs
   └── utils/
       ├── mod.rs
       └── helpers.rs
   ```

3. **错误处理**
   - 优先使用 `Result` 而不是 `panic!`
   - 使用 `?` 操作符传播错误
   - 自定义错误类型

### Q38: 什么时候使用 panic!？

**A:**

**应该使用 panic!**：
- 不可恢复的错误（如内存分配失败）
- 编程错误（如违反不变量）
- 测试代码

**不应该使用 panic!**：
- 用户输入错误
- 网络错误
- 文件系统错误
- 可恢复的错误

### Q39: 如何处理用户输入？

**A:**

```rust
use std::io::{self, Write};

fn get_input(prompt: &str) -> Result<String, io::Error> {
    print!("{}", prompt);
    io::stdout().flush()?;

    let mut input = String::new();
    io::stdin().read_line(&mut input)?;
    Ok(input.trim().to_string())
}

fn main() -> Result<(), io::Error> {
    let name = get_input("Enter your name: ")?;
    println!("Hello, {}!", name);
    Ok(())
}
```

### Q40: 如何处理配置文件？

**A:**

```rust
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    host: String,
    port: u16,
    database: String,
}

fn load_config(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = load_config("config.json")?;
    println!("Config: {:?}", config);
    Ok(())
}
```

### Q41: 如何处理日志？

**A:** 使用 `log` crate。

```rust
use log::{info, warn, error};

fn main() {
    env_logger::init();

    info!("Starting application");
    warn!("This is a warning");
    error!("This is an error");
}
```

### Q42: 如何编写测试？

**A:**

```rust
// 单元测试
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

// 集成测试
// tests/integration_test.rs
use my_crate::add;

#[test]
fn test_add_integration() {
    assert_eq!(add(2, 3), 5);
}
```

### Q43: 如何处理配置？

**A:**

```rust
use config::{Config, File, FileFormat};

#[derive(Debug, serde::Deserialize)]
struct Settings {
    host: String,
    port: u16,
}

fn load_settings() -> Result<Settings, config::ConfigError> {
    let mut config = Config::default();
    config.merge(File::new("config.toml", FileFormat::Toml))?;
    config.try_into()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let settings = load_settings()?;
    println!("Settings: {:?}", settings);
    Ok(())
}
```

### Q44: 如何处理数据库？

**A:** 使用 `sqlx` 或 `diesel`。

```rust
use sqlx::postgres::PgPoolOptions;

#[derive(Debug, sqlx::FromRow)]
struct User {
    id: i32,
    username: String,
    email: String,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect("postgres://user:password@localhost/dbname")
        .await?;

    let users: Vec<User> = sqlx::query_as::<_, User>("SELECT id, username, email FROM users")
        .fetch_all(&pool)
        .await?;

    for user in users {
        println!("{:?}", user);
    }

    Ok(())
}
```

### Q45: 如何处理 HTTP 请求？

**A:** 使用 `reqwest`。

```rust
use reqwest;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let response = reqwest::get("https://httpbin.org/get").await?;
    let body = response.text().await?;
    println!("Body: {}", body);
    Ok(())
}
```

### Q46: 如何处理 JSON？

**A:** 使用 `serde` 和 `serde_json`。

```rust
use serde::{Deserialize, Serialize};
use serde_json;

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: u32,
    username: String,
    email: String,
}

fn main() {
    let user = User {
        id: 1,
        username: String::from("john"),
        email: String::from("john@example.com"),
    };

    // 序列化
    let json = serde_json::to_string(&user).unwrap();
    println!("JSON: {}", json);

    // 反序列化
    let user: User = serde_json::from_str(&json).unwrap();
    println!("User: {:?}", user);
}
```

### Q47: 如何处理日期时间？

**A:** 使用 `chrono`。

```rust
use chrono::{DateTime, Utc, Local};

fn main() {
    // 当前时间 (UTC)
    let now_utc = Utc::now();
    println!("UTC: {}", now_utc);

    // 当前时间 (本地)
    let now_local = Local::now();
    println!("Local: {}", now_local);

    // 格式化
    let formatted = now_utc.format("%Y-%m-%d %H:%M:%S").to_string();
    println!("Formatted: {}", formatted);
}
```

### Q48: 如何处理命令行参数？

**A:** 使用 `clap`。

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Input file
    #[arg(short, long)]
    input: String,

    /// Output file
    #[arg(short, long)]
    output: Option<String>,

    /// Verbose mode
    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let args = Args::parse();
    println!("Input: {}", args.input);
}
```

### Q49: 如何处理环境变量？

**A:**

```rust
use std::env;

fn main() {
    // 获取环境变量
    let path = env::var("PATH").unwrap_or_else(|_| String::from("Not found"));
    println!("PATH: {}", path);

    // 设置环境变量（仅当前进程）
    env::set_var("MY_VAR", "value");

    // 检查环境变量
    if env::var("DEBUG").is_ok() {
        println!("Debug mode enabled");
    }
}
```

### Q50: 如何处理文件系统？

**A:**

```rust
use std::fs;
use std::io::{self, Write};

// 读取文件
fn read_file(path: &str) -> Result<String, io::Error> {
    fs::read_to_string(path)
}

// 写入文件
fn write_file(path: &str, content: &str) -> Result<(), io::Error> {
    let mut file = fs::File::create(path)?;
    file.write_all(content.as_bytes())?;
    Ok(())
}

// 创建目录
fn create_dir(path: &str) -> Result<(), io::Error> {
    fs::create_dir_all(path)?;
    Ok(())
}

// 列出目录
fn list_dir(path: &str) -> Result<Vec<String>, io::Error> {
    let entries = fs::read_dir(path)?;
    let paths: Vec<String> = entries
        .filter_map(|entry| entry.ok())
        .map(|entry| entry.path().display().to_string())
        .collect();
    Ok(paths)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 读取文件
    let content = read_file("Cargo.toml")?;
    println!("File content: {}", content);

    // 写入文件
    write_file("test.txt", "Hello, Rust!")?;

    // 创建目录
    create_dir("test_dir")?;

    // 列出目录
    let paths = list_dir(".")?;
    for path in paths {
        println!("{}", path);
    }

    Ok(())
}
```

---

## 总结

### 常见问题分类

1. **基础问题**：安装、语法、学习曲线
2. **所有权系统**：移动、借用、生命周期
3. **错误处理**：panic、Result、? 操作符
4. **并发编程**：线程、异步、锁
5. **高级特性**：Traits、泛型、宏
6. **性能问题**：优化、内存、二进制大小
7. **工具链**：Cargo、调试、格式化
8. **最佳实践**：代码风格、错误处理、测试

### 学习建议

1. **从基础开始**：不要跳过所有权系统
2. **多写代码**：实践是最好的老师
3. **阅读文档**：官方文档非常详细
4. **参与社区**：提问和回答问题
5. **持续学习**：Rust 在快速发展

### 推荐资源

- [Rust 官方文档](https://doc.rust-lang.org/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rustlings](https://github.com/rust-lang/rustlings)
- [Rust 社区](https://www.rust-lang.org/community)

---

**记住：遇到问题时，先查文档，再问社区，最后自己思考！** 🦀

**祝你 Rust 学习之旅愉快！** 🚀