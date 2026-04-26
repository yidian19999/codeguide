import os
import json
from pathlib import Path

CONFIG_FILE = Path("config.json")

def load_config():
    """加载配置文件 - 服务器端配置作为默认值"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "text_api": {
            "base_url": "",
            "api_key": "",
            "model": "gpt-4"
        },
        "image_api": {
            "base_url": "",
            "api_key": "",
            "model": "dall-e-3"
        }
    }

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_text_api_config():
    """获取文本生成API配置 - 优先从 session state 读取"""
    import streamlit as st
    
    # 优先从 session state 读取（浏览器存储的配置）
    if "api_config" in st.session_state:
        return st.session_state["api_config"].get("text_api", {})
    
    # 回退到服务器配置
    config = load_config()
    return config.get("text_api", {})

def get_image_api_config():
    """获取图像生成API配置 - 优先从 session state 读取"""
    import streamlit as st
    
    # 优先从 session state 读取（浏览器存储的配置）
    if "api_config" in st.session_state:
        return st.session_state["api_config"].get("image_api", {})
    
    # 回退到服务器配置
    config = load_config()
    return config.get("image_api", {})
