#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import requests
from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

# 从环境变量获取 Webshare.io 代理列表 URL
WEBSHARE_PROXY_URL = os.environ.get("WEBSHARE_PROXY_URL")

proxy_list = []

def fetch_proxies():
    """获取并解析 Webshare.io 代理列表"""
    global proxy_list
    if not WEBSHARE_PROXY_URL:
        print("未设置 WEBSHARE_PROXY_URL 环境变量，不使用代理。")
        return

    try:
        response = requests.get(WEBSHARE_PROXY_URL)
        response.raise_for_status()  # 如果请求失败则抛出异常
        proxy_list = response.text.strip().split("\n")
        print(f"成功获取 {len(proxy_list)} 个代理。")
    except requests.exceptions.RequestException as e:
        print(f"获取代理列表失败: {e}")

def get_random_proxy():
    """从代理池中随机选择一个代理"""
    if not proxy_list:
        return None

    proxy_str = random.choice(proxy_list)
    parts = proxy_str.split(":")
    if len(parts) == 4:
        ip, port, username, password = parts
        return f"http://{username}:{password}@{ip}:{port}"
    else:
        return f"http://{proxy_str}" # 兼容无认证的代理

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """处理聊天补全请求"""
    data = request.get_json()
    model = data.get("model", "gpt-4o")
    messages = data.get("messages")

    if not messages:
        return jsonify({"error": "messages 字段是必需的"}), 400

    proxy = get_random_proxy()
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        client = Client(proxies=proxies)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return jsonify(response.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    fetch_proxies()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


