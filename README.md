# 网易云音乐歌单批量下载工具 - NetEase-Playlist-Downloader

🎵 一款支持JS逆向加密的网易云音乐歌单批量下载工具 | 仅供学习研究使用 🎵
## 🔗 项目链接

- **GitHub仓库**: [-NetEase-Playlist-Downloader](https://github.com/LCZcoding/-NetEase-Playlist-Downloader)
## 🔔注意事项
- 本项目不可以在没有vip账号登录的状态下爬取vip才能播放的音乐，所有的音乐下载的格式均为mp3
- 本项目仅用于学习研究，不得用于商业用途。

## 📋 项目简介

本项目是一个基于Python开发的网易云音乐歌单批量下载工具。通过模拟网易云音乐的API请求，利用JS逆向技术破解加密算法，实现对指定歌单内所有音乐的批量下载功能。

### 主要特性

- ✅ **批量下载** - 支持一键下载整个歌单的所有音乐
- ✅ **JS逆向加密** - 实现网易云音乐的API加密算法
- ✅ **智能文件名处理** - 自动清理文件名中的非法字符
- ✅ **异常处理机制** - 完善的错误处理和重试机制
- ✅ **防反爬策略** - 包含请求间隔，避免被服务器限制
- ✅ **自动保存** - 音乐文件自动保存至桌面的Music文件夹

## 🛠️ 技术栈

- **语言**: Python 3.11+
- **核心库**: 
  - `requests` - HTTP请求处理
  - `PyExecJS` - JavaScript代码执行
  - `pathlib` - 现代化路径处理
- **加密算法**: AES/CBC模式加密
- **反爬措施**: 请求间隔、User-Agent伪装

## 📦 依赖安装

在使用前，请先安装必要的依赖包：

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install requests==2.32.0 PyExecJS>=1.5.1
```

## ⚙️ 配置说明

### 1. 获取Cookie
1. 登录网易云音乐网页版 (https://music.163.com)
2. 打开浏览器开发者工具 (F12)
3. 访问任意页面，查看Network标签页
4. 复制Request Headers中的Cookie值

### 2. 获取歌单ID
- 网易云歌单链接格式如：`https://music.163.com/playlist?id=XXXXXXXX`
- 其中`XXXXXXXX`即为歌单ID

### 3. 修改配置
编辑 `main.py` 文件，修改以下变量：

```python
# 你的Cookie
cookie = 'YOUR_COOKIE'

# 你的歌单链接ID
link = 'https://music.163.com/playlist?id=YOUR_PLAYLIST_ID'
```

## 🚀 使用方法

1. **克隆项目**
   ```bash
   git clone https://github.com/your-repo/-NetEase-Playlist-Downloader.git
   cd -NetEase-Playlist-Downloader
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置参数**
   - 编辑 `main.py` 中的 `cookie` 和 `link` 参数

4. **运行程序**
   ```bash
   python main.py
   ```

5. **等待完成**
   - 程序会自动下载歌单中的所有音乐
   - 下载的音乐将保存到 `桌面/Music` 文件夹

## 🔧 代码结构
```text
-NetEase-Playlist-Downloader/ 
│ 
├── main.py # 主程序入口 
├── NetEaseCloudEncryption.js # 网易云加密算法JS代码 
├── requirements.txt # 项目依赖 
├── README.md # 项目说明文档 
└── LICENSE # 许可证
```


### 核心功能模块

- **main.py**:
  - 歌单页面解析与音乐信息提取
  - JS加密函数调用与API请求
  - 文件名清理与保存
  - 异常处理与日志输出

- **NetEaseCloudEncryption.js**:
  - 网易云音乐API加密算法
  - AES加密实现
  - RSA密钥加密

## 📁 输出说明

- 所有下载的音乐文件将以 `.mp3` 格式保存
- 文件自动保存至 `桌面/Music` 目录
- 文件名为歌曲原始名称（已清理非法字符）

## ⚠️ 注意事项

1. **仅限学习用途** - 请勿用于商业或其他违法用途
2. **遵守版权法规** - 尊重音乐版权，合理使用
3. **网络环境** - 确保网络连接稳定
4. **Cookie时效性** - Cookie可能会过期，需要定期更新

## 🔒 安全声明

- 本项目不会上传或泄露您的任何个人信息
- 所有数据仅在本地处理
- 请妥善保管您的Cookie信息，不要分享给他人

## 🐛 常见问题

### Q: 下载过程中出现403错误怎么办？
A: 检查Cookie是否正确设置，或Cookie是否已过期，重新获取新的Cookie。

### Q: 为什么某些歌曲无法下载？
A: VIP歌曲、付费歌曲或已下架歌曲无法下载，程序会自动跳过并提示。

### Q: 文件名包含特殊字符怎么办？
A: 程序会自动清理文件名中的非法字符，确保文件正常保存。

### Q: 如何提高下载成功率？
A: 保持稳定的网络连接，避免频繁请求，适当调整请求间隔时间。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进本项目！

## 📄 许可证

本项目采用 [MIT License](./LICENSE)，仅供学习交流使用。

## 📞 联系方式

如果您有任何问题或建议，请通过GitHub Issues联系。

---

> **免责声明**: 本工具仅供学习研究使用，请遵守相关法律法规，尊重音乐版权。使用本工具产生的法律责任由使用者自行承担。