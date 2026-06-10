# Product Detail Page Maker

根据商品实拍图和信息表，生成：

- 1 张商品头图；
- 6 张详情页切片；
- 1 张完整详情页。

生图固定使用 `gpt-image-2`。

## 安装 Codex

### Codex App

适合不熟悉终端的成员，支持 Mac 和 Windows。

下载：<https://developers.openai.com/codex/app>

安装后使用 ChatGPT 账号登录。

### Codex 终端版

Mac：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

安装后运行 `codex login` 完成登录。

## 安装 Skill

任选一种方式。

### 方式一：Trae Solo + GitHub，推荐新手

在 Trae Solo 中发送：

```text
请安装并配置这个仓库：
https://github.com/Yuu2427/product-detail-page-maker

请安装为全局 Skill，并自动安装正常运行所需的内容。
不要修改 SKILL.md 中的业务规则。
最后只告诉我是否安装成功，以及是否需要重启应用。
```

### 方式二：终端安装

适合电脑已有 Node.js、npx 和 Git 的成员。

```bash
npx skills add github:Yuu2427/product-detail-page-maker --global --agent codex --yes
```

安装后在 Codex 中发送：

```text
请检查刚安装的 ecommerce-gpt-image2-pdp-high-fidelity Skill，
自动安装正常运行所需的内容。
最后只告诉我是否可以正常使用。
```

### 方式三：本地文件夹 + Trae Solo

将完整 Skill 文件夹发给对方，让对方用 Trae Solo 打开并发送：

```text
请将当前文件夹安装为全局 Skill，并自动安装正常运行所需的内容。
不要修改 SKILL.md 中的业务规则。
最后只告诉我是否安装成功，以及是否需要重启应用。
```

安装完成后，重启 Codex 或 Trae Solo。

## 使用

请查看 [`使用说明.md`](使用说明.md)。
