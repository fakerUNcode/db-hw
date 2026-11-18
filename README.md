# 缓冲区页面置换机制：LRU 与 LFU 交互演示平台

## 部署与运行说明

### 1. 获取项目

```bash
git clone https://github.com/fakerUNcode/db-hw.git
cd db-hw
```

### 2. 启动演示（三选一）

| 方式 | 适用平台 | 操作说明 |
| :--- | :--- | :--- |
| **方式一：一键脚本（推荐）** | Windows | 进入 `演示文稿` 目录，双击 **`start-windows.bat`**，浏览器将自动打开演示页面 |
| | macOS / Linux | 终端执行 `bash 演示文稿/start-mac-linux.sh`（macOS 可先 `chmod +x` 后运行） |
| **方式二：本地 HTTP 服务** | 全平台 | 在 `演示文稿` 目录执行 `python -m http.server 8642`，浏览器访问 `http://127.0.0.1:8642/index.html` |
| **方式三：直接打开** | 全平台 | 使用任意现代浏览器直接打开 `演示文稿/index.html`（零外部网络依赖，完全离线可用） |

### 3. 端口与停止说明

- **默认端口**：脚本默认监听 `127.0.0.1:8642`。如端口被占用，可传入自定义端口号：
  - Windows：`start-windows.bat 9000`
  - macOS / Linux：`bash 演示文稿/start-mac-linux.sh 9000`
- **停止服务**：在运行脚本的终端窗口按 `Ctrl + C`（或直接关闭窗口）。
- **环境依赖**：一键脚本及方式二依赖 Python 3（仅用于启动内置 HTTP 服务）；若无 Python 环境，直接使用方式三即可。
