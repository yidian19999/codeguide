# CodeGuide 部署指南

## 项目简介

CodeGuide 是一个基于 Streamlit 的 AI 辅助软件开发规则生成系统。

## 部署方案对比

| 方案 | 适用场景 | 难度 | 成本 |
|------|---------|------|------|
| **方案一：腾讯云 CloudBase** | 推荐！支持容器部署 | ⭐⭐ | 按量计费 |
| **方案二：腾讯云轻量服务器** | 长期运行，固定IP | ⭐⭐ | 固定月费 |
| **方案三：EdgeOne Pages** | 仅适合静态前端 | ⭐ | 免费额度 |

---

## 方案一：腾讯云 CloudBase（推荐）

CloudBase 支持容器化部署 Streamlit 应用，是最适合的方案。

### 1. 准备工作

```bash
# 安装腾讯云 CLI
npm install -g @cloudbase/cli

# 登录
cloudbase login
```

### 2. 构建并推送镜像

```bash
cd d:\cursorfiles\softwarecopyright

# 登录腾讯云容器镜像服务（TCR）
docker login ccr.ccs.tencentyun.com --username=您的腾讯云账号ID

# 构建镜像
docker build -t codeguide:latest .

# 标记镜像（替换为您的命名空间）
docker tag codeguide:latest ccr.ccs.tencentyun.com/您的命名空间/codeguide:v1.0

# 推送镜像
docker push ccr.ccs.tencentyun.com/您的命名空间/codeguide:v1.0
```

### 3. CloudBase 控制台部署

1. 登录 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
2. 创建新环境
3. 进入「云服务」→「容器服务」
4. 点击「新建服务」
5. 选择「镜像部署」
6. 填写镜像地址：`ccr.ccs.tencentyun.com/您的命名空间/codeguide:v1.0`
7. 配置：
   - 端口：8501
   - 实例规格：0.5核 1GB（起步）
   - 自动扩缩容：开启
8. 点击「创建」

### 4. 配置自定义域名（可选）

1. 在 CloudBase 控制台进入「环境」→「访问服务」
2. 点击「添加域名」
3. 按指引配置 DNS 解析

---

## 方案二：腾讯云轻量应用服务器

适合需要长期运行、固定 IP 的场景。

### 1. 购买服务器

1. 登录 [轻量服务器控制台](https://console.cloud.tencent.com/lighthouse)
2. 创建实例，选择：
   - 地域：靠近用户的地区
   - 镜像：Docker 基础镜像
   - 配置：2核 4GB（推荐）
3. 完成购买

### 2. 部署应用

```bash
# SSH 连接到服务器
ssh root@您的服务器IP

# 安装 Docker（如未安装）
curl -fsSL https://get.docker.com | sh

# 克隆项目
git clone https://github.com/您的用户名/codeguide.git
cd codeguide

# 构建并运行
docker build -t codeguide:latest .
docker run -d \
  --name codeguide \
  -p 8501:8501 \
  --restart always \
  codeguide:latest

# 查看运行状态
docker logs -f codeguide
```

### 3. 配置 Nginx 反向代理（可选）

```bash
# 安装 Nginx
apt-get update && apt-get install -y nginx

# 配置 Nginx
cat > /etc/nginx/sites-available/codeguide << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/codeguide /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 4. 配置 HTTPS（可选）

```bash
# 安装 certbot
apt-get install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com
```

---

## 方案三：EdgeOne Pages（仅适合静态页面）

⚠️ **注意**：EdgeOne Pages 主要用于静态网站部署，不支持 Python/Streamlit 运行时。此方案仅适合部署 Streamlit 的静态导出版本（功能受限）。

### 1. 安装 EdgeOne CLI

```bash
npm install -g edgeone
```

### 2. 初始化项目

```bash
cd d:\cursorfiles\softwarecopyright
edgeone login
edgeone pages init
```

### 3. 部署

```bash
edgeone pages deploy -n codeguide
```

---

## 本地测试 Docker 部署

在正式部署前，建议先在本地测试：

```bash
cd d:\cursorfiles\softwarecopyright

# 构建镜像
docker build -t codeguide:latest .

# 运行容器
docker run -p 8501:8501 codeguide:latest

# 访问 http://localhost:8501 测试
```

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `STREAMLIT_SERVER_PORT` | 服务端口 | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | 监听地址 | 0.0.0.0 |
| `STREAMLIT_SERVER_HEADLESS` | 无头模式 | true |

### 持久化存储

由于容器是无状态的，配置文件 `config.json` 不会被持久化。建议：

1. **方案一**：使用云数据库（如 MongoDB、MySQL）存储配置
2. **方案二**：使用对象存储（COS）保存配置文件
3. **方案三**：部署后在界面中重新配置 API

---

## 故障排查

### 容器无法启动

```bash
# 查看日志
docker logs codeguide

# 检查端口占用
netstat -tlnp | grep 8501
```

### 应用访问慢

1. 检查服务器带宽
2. 开启 CDN 加速（CloudBase 默认开启）
3. 升级服务器配置

### API 调用失败

1. 确认 API Key 已配置
2. 检查服务器是否能访问外网
3. 查看应用日志

---

## 参考链接

- [腾讯云 CloudBase 文档](https://cloud.tencent.com/document/product/876)
- [腾讯云轻量服务器文档](https://cloud.tencent.com/document/product/1207)
- [腾讯云容器镜像服务](https://cloud.tencent.com/document/product/1141)
- [Streamlit 部署文档](https://docs.streamlit.io/deploy)

---

## 推荐方案总结

**新手推荐**：方案一（CloudBase）
- 无需管理服务器
- 自动扩缩容
- 按量付费，成本低

**长期使用**：方案二（轻量服务器）
- 固定 IP，适合绑定域名
- 完全控制环境
- 成本可控
