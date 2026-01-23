---
title: Git命令清单 
categories:
  - Git
tags:
  - Git commands
---



# Git命令清单

Git 是一个分布式版本控制系统，由 Linus Torvalds 创建，用于跟踪文件的变化、管理项目版本历史，并支持多人协作开发。它允许开发者在本地工作，同时与远程仓库同步。

一般来说，日常使用只要记住下图6个命令，就可以了。但是熟练使用，恐怕要记住60～100个命令。

![Git commands workflow](/assets/git/202203191455284.png)

下面是常用 的Git 命令清单。几个专用名词的译名如下：

- Workspace：工作区
- Index / Stage：暂存区
- Repository：仓库区（或本地仓库）
- Remote：远程仓库

## 一、新建代码库

这部分命令用于初始化新的 Git 仓库或从远程服务器克隆现有项目。初始化后，你可以开始添加文件和提交。

~~~bash
# 在当前目录新建一个Git代码库
$ git init

# 新建一个目录，将其初始化为Git代码库
$ git init [project-name]

# 下载一个项目和它的整个代码历史
$ git clone [url]
~~~

### 示例
- 创建新项目：`git init myproject`
- 克隆 GitHub 仓库：`git clone https://github.com/octocat/Hello-World.git`

## 二、配置

Git的设置文件为`.gitconfig`，它可以在用户主目录下（全局配置），也可以在项目目录下（项目配置）。全局配置影响所有 Git 项目，而项目配置仅对当前仓库有效。用户信息用于标识每次提交的作者。

~~~bash
# 显示当前的Git配置
$ git config --list

# 编辑Git配置文件
$ git config -e [--global]

# 设置提交代码时的用户信息
$ git config [--global] user.name "[name]"
$ git config [--global] user.email "[email address]"

# 设置默认编辑器
$ git config [--global] core.editor "vim"

# 设置默认合并工具
$ git config [--global] merge.tool "meld"
~~~

### 示例
- 设置全局用户名：`git config --global user.name "John Doe"`
- 查看全局配置：`git config --global --list`

## 三、增加/删除文件

暂存区（Index）是 Git 中的一个中间区域，用于准备下次提交的文件。使用 `git add` 将文件添加到暂存区，`git rm` 删除文件，`git mv` 重命名文件。

~~~bash
# 添加指定文件到暂存区
$ git add [file1] [file2] ...

# 添加指定目录到暂存区，包括子目录
$ git add [dir]

# 添加当前目录的所有文件到暂存区
$ git add .

# 添加每个变化前，都会要求确认
# 对于同一个文件的多处变化，可以实现分次提交
$ git add -p

# 删除工作区文件，并且将这次删除放入暂存区
$ git rm [file1] [file2] ...

# 停止追踪指定文件，但该文件会保留在工作区
$ git rm --cached [file]

# 改名文件，并且将这个改名放入暂存区
$ git mv [file-original] [file-renamed]
~~~

### 示例
- 添加所有 .java 文件：`git add *.java`
- 交互式添加：`git add -p`（允许选择哪些变更添加到暂存区）
- 移除文件但保留本地：`git rm --cached config.secret`

## 四、代码提交

提交是将暂存区的文件保存到本地仓库的历史记录中。每次提交都有一个唯一的哈希值和提交信息。使用 `git commit --amend` 可以修改上一次提交。

~~~bash
# 提交暂存区到仓库区
$ git commit -m [message]

# 提交暂存区的指定文件到仓库区
$ git commit [file1] [file2] ... -m [message]

# 提交工作区自上次commit之后的变化，直接到仓库区
$ git commit -a

# 提交时显示所有diff信息
$ git commit -v

# 使用一次新的commit，替代上一次提交
# 如果代码没有任何新变化，则用来改写上一次commit的提交信息
$ git commit --amend -m [message]

# 重做上一次commit，并包括指定文件的新变化
$ git commit --amend [file1] [file2] ...
~~~

### 示例
- 提交所有暂存文件：`git commit -m "Add new feature"`
- 跳过暂存直接提交修改的文件：`git commit -a -m "Fix bug"`
- 修改上一次提交信息：`git commit --amend -m "Updated message"`

## 五、分支

分支允许你在不同的开发线上工作，而不影响主分支。常用分支策略包括 Git Flow、GitHub Flow 等。`git merge` 用于合并分支，`git rebase` 可以重写历史（未列出，但常用）。

~~~bash
# 列出所有本地分支
$ git branch

# 列出所有远程分支
$ git branch -r

# 列出所有本地分支和远程分支
$ git branch -a

# 新建一个分支，但依然停留在当前分支
$ git branch [branch-name]

# 新建一个分支，并切换到该分支
$ git checkout -b [branch]

# 新建一个分支，指向指定commit
$ git branch [branch] [commit]

# 新建一个分支，与指定的远程分支建立追踪关系
$ git branch --track [branch] [remote-branch]

# 切换到指定分支，并更新工作区
$ git checkout [branch-name]

# 切换到上一个分支
$ git checkout -

# 建立追踪关系，在现有分支与指定的远程分支之间
$ git branch --set-upstream [branch] [remote-branch]

# 合并指定分支到当前分支
$ git merge [branch]

# 选择一个commit，合并进当前分支
$ git cherry-pick [commit]

# 删除分支
$ git branch -d [branch-name]

# 删除远程分支
$ git push origin --delete [branch-name]
$ git branch -dr [remote/branch]
~~~

### 示例
- 创建并切换到新分支：`git checkout -b feature/new-feature`
- 合并分支：`git merge develop`（在主分支上执行）
- 删除已合并的分支：`git branch -d feature/old-feature`

## 六、标签

标签（Tag）用于标记重要的提交点，如版本发布。标签可以是轻量级的（lightweight）或带注释的（annotated）。带注释的标签包含更多信息。

~~~bash
# 列出所有tag
$ git tag

# 新建一个tag在当前commit
$ git tag [tag]

# 新建一个tag在指定commit
$ git tag [tag] [commit]

# 新建带注释的tag
$ git tag -a [tag] -m [message]

# 删除本地tag
$ git tag -d [tag]

# 删除远程tag
$ git push origin :refs/tags/[tagName]

# 查看tag信息
$ git show [tag]

# 提交指定tag
$ git push [remote] [tag]

# 提交所有tag
$ git push [remote] --tags

# 新建一个分支，指向某个tag
$ git checkout -b [branch] [tag]
~~~

### 示例
- 创建带注释的标签：`git tag -a v1.0 -m "Release version 1.0"`
- 推送标签到远程：`git push origin v1.0`
- 查看标签详情：`git show v1.0`

## 七、查看信息

Git 提供了丰富的命令来查看仓库状态、历史和差异。`git log` 用于查看提交历史，`git diff` 显示文件变化，`git status` 检查当前状态。

~~~bash
# 显示有变更的文件
$ git status

# 显示当前分支的版本历史
$ git log

# 显示commit历史，以及每次commit发生变更的文件
$ git log --stat

# 搜索提交历史，根据关键词
$ git log -S [keyword]

# 显示某个commit之后的所有变动，每个commit占据一行
$ git log [tag] HEAD --pretty=format:%s

# 显示某个commit之后的所有变动，其"提交说明"必须符合搜索条件
$ git log [tag] HEAD --grep feature

# 显示某个文件的版本历史，包括文件改名
$ git log --follow [file]
$ git whatchanged [file]

# 显示指定文件相关的每一次diff
$ git log -p [file]

# 显示过去5次提交
$ git log -5 --pretty --oneline

# 显示所有提交过的用户，按提交次数排序
$ git shortlog -sn

# 显示指定文件是什么人在什么时间修改过
$ git blame [file]

# 显示暂存区和工作区的差异
$ git diff

# 显示暂存区和上一个commit的差异
$ git diff --cached [file]

# 显示工作区与当前分支最新commit之间的差异
$ git diff HEAD

# 显示两次提交之间的差异
$ git diff [first-branch]...[second-branch]

# 显示今天你写了多少行代码
$ git diff --shortstat "@{0 day ago}"

# 显示某次提交的元数据和内容变化
$ git show [commit]

# 显示某次提交发生变化的文件
$ git show --name-only [commit]

# 显示某次提交时，某个文件的内容
$ git show [commit]:[filename]

# 显示当前分支的最近几次提交
$ git reflog
~~~

### 示例
- 查看简洁日志：`git log --oneline -10`
- 查看文件变更：`git diff HEAD~1`
- 查看谁修改了某行：`git blame file.txt`

## 八、远程同步

远程仓库允许团队协作。`git fetch` 下载远程变更但不合并，`git pull` 下载并合并，`git push` 上传本地提交。

~~~bash
# 下载远程仓库的所有变动
$ git fetch [remote]

# 显示所有远程仓库
$ git remote -v

# 显示某个远程仓库的信息
$ git remote show [remote]

# 增加一个新的远程仓库，并命名
$ git remote add [shortname] [url]

# 取回远程仓库的变化，并与本地分支合并
$ git pull [remote] [branch]

# 上传本地指定分支到远程仓库
$ git push [remote] [branch]

# 强行推送当前分支到远程仓库，即使有冲突
$ git push [remote] --force

# 推送所有分支到远程仓库
$ git push [remote] --all
~~~

### 示例
- 添加远程仓库：`git remote add origin https://github.com/user/repo.git`
- 拉取最新更改：`git pull origin main`
- 推送分支：`git push origin feature-branch`

## 九、撤销

Git 提供了多种撤销操作。`git reset` 移动 HEAD 指针，`git revert` 创建新提交撤销旧的，`git stash` 临时保存未提交更改。

~~~bash
# 恢复暂存区的指定文件到工作区
$ git checkout [file]

# 恢复某个commit的指定文件到暂存区和工作区
$ git checkout [commit] [file]

# 恢复暂存区的所有文件到工作区
$ git checkout .

# 重置暂存区的指定文件，与上一次commit保持一致，但工作区不变
$ git reset [file]

# 重置暂存区与工作区，与上一次commit保持一致
$ git reset --hard

# 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
$ git reset [commit]

# 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
$ git reset --hard [commit]

# 重置当前HEAD为指定commit，但保持暂存区和工作区不变
$ git reset --keep [commit]

# 新建一个commit，用来撤销指定commit
# 后者的所有变化都将被前者抵消，并且应用到当前分支
$ git revert [commit]

# 暂时将未提交的变化移除，稍后再移入
$ git stash
$ git stash pop

# 列出所有stash
$ git stash list

# 应用指定的stash
$ git stash apply [stash@{n}]
~~~

### 示例
- 撤销最后一次提交但保留文件：`git reset --soft HEAD~1`
- 撤销提交并删除更改：`git reset --hard HEAD~1`
- 临时保存工作：`git stash`（稍后 `git stash pop` 恢复）

## 十、其他

~~~bash
# 生成一个可供发布的压缩包
$ git archive

# 显示Git版本
$ git --version

# 显示帮助信息
$ git help [command]

# 清理未跟踪的文件
$ git clean -f

# 压缩Git仓库
$ git gc
~~~

### 示例
- 生成 tar 包：`git archive --format=tar --output=project.tar HEAD`
- 清理仓库：`git gc --prune=now`

## 十一、Git 最佳实践和提示

- **提交信息**：使用清晰的提交信息，如 "Fix bug in login module" 而不是 "fix"。
- **分支命名**：使用描述性名称，如 `feature/add-user-auth`。
- **定期推送**：避免本地更改丢失。
- **使用 .gitignore**：忽略不需要版本控制的文件，如日志、临时文件。
- **学习资源**：参考 [Pro Git 书籍](https://git-scm.com/book) 或官方文档。

### 常见问题解决
- **忘记添加文件**：使用 `git commit --amend` 添加遗漏文件。
- **冲突解决**：编辑冲突文件，标记为解决后 `git add`，然后 `git commit`。
- **恢复删除的分支**：使用 `git reflog` 找到哈希，然后 `git checkout -b branch hash`。

