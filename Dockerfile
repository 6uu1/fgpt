# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim-bookworm

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY app.py .

# 暴露应用程序端口
EXPOSE 5000

# 定义环境变量，Webshare.io 代理列表 URL 将通过部署平台设置
ENV WEBSHARE_PROXY_URL=""

# 运行应用程序
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


