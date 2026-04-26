import streamlit as st
import sys
sys.path.append('..')
from config import load_config, save_config

def show_settings():
    """显示设置界面"""
    st.title("⚙️ 系统设置")
    st.markdown("---")
    
    config = load_config()
    
    # 文本生成API设置
    st.header("📝 文本生成API配置 (OpenAI格式)")
    st.info("用于生成需求文档、业务逻辑、技术规范等文字内容")
    
    col1, col2 = st.columns(2)
    with col1:
        text_base_url = st.text_input(
            "Base URL",
            value=config["text_api"].get("base_url", ""),
            placeholder="https://api.openai.com/v1",
            help="API基础URL，如使用OpenAI官方API则填写 https://api.openai.com/v1"
        )
    with col2:
        text_model = st.text_input(
            "模型名称",
            value=config["text_api"].get("model", "gpt-4"),
            placeholder="gpt-4",
            help="如: gpt-4, gpt-3.5-turbo, claude-3-opus-20240229 等"
        )
    
    text_api_key = st.text_input(
        "API Key",
        value=config["text_api"].get("api_key", ""),
        type="password",
        placeholder="sk-...",
        help="您的API密钥"
    )
    
    st.markdown("---")
    
    # 图像生成API设置
    st.header("🎨 图像生成API配置 (OpenAI格式)")
    st.info("用于生成UI界面截图、设计图等图像内容")
    
    col1, col2 = st.columns(2)
    with col1:
        image_base_url = st.text_input(
            "Base URL",
            value=config["image_api"].get("base_url", ""),
            placeholder="https://api.openai.com/v1",
            key="image_base_url",
            help="API基础URL，可以与文本API不同"
        )
    with col2:
        image_model = st.text_input(
            "模型名称",
            value=config["image_api"].get("model", "dall-e-3"),
            placeholder="dall-e-3",
            key="image_model",
            help="如: dall-e-3, dall-e-2 等"
        )
    
    image_api_key = st.text_input(
        "API Key",
        value=config["image_api"].get("api_key", ""),
        type="password",
        placeholder="sk-...",
        key="image_api_key",
        help="您的API密钥，可以与文本API不同"
    )
    
    st.markdown("---")
    
    # 保存按钮
    if st.button("💾 保存设置", type="primary", use_container_width=True):
        config["text_api"] = {
            "base_url": text_base_url,
            "api_key": text_api_key,
            "model": text_model
        }
        config["image_api"] = {
            "base_url": image_base_url,
            "api_key": image_api_key,
            "model": image_model
        }
        save_config(config)
        st.success("✅ 设置已保存！")
    
    # 使用说明
    with st.expander("📖 配置说明"):
        st.markdown("""
        ### 支持的API提供商
        
        1. **OpenAI官方**
           - Base URL: `https://api.openai.com/v1`
           - 文本模型: `gpt-4`, `gpt-3.5-turbo`
           - 图像模型: `dall-e-3`, `dall-e-2`
        
        2. **Azure OpenAI**
           - Base URL: `https://{your-resource}.openai.azure.com/openai/deployments/{deployment-id}`
           - 需要添加api-version参数
        
        3. **第三方代理服务**
           - 如: `https://api.xxx.com/v1`
           - 请根据服务商文档填写
        
        4. **本地部署 (Ollama等)**
           - Base URL: `http://localhost:11434/v1`
           - 注意：本地模型可能不支持图像生成
        
        ### 安全提示
        - API Key仅存储在本地config.json文件中
        - 请勿将config.json提交到代码仓库
        - 建议为不同用途使用不同的API Key
        """)

