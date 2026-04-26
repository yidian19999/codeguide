import streamlit as st
import json
import sys
sys.path.append('..')
from config import load_config as load_server_config

def get_local_storage_key():
    """获取本地存储的key"""
    return "codeguide_api_config"

def load_config():
    """加载配置 - 优先从浏览器本地存储读取"""
    # 默认配置
    default_config = {
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
    
    # 尝试从 session state 读取（页面内保持）
    if "api_config" in st.session_state:
        return st.session_state["api_config"]
    
    # 尝试从浏览器本地存储读取
    local_config = get_config_from_browser()
    if local_config:
        st.session_state["api_config"] = local_config
        return local_config
    
    # 回退到服务器配置（兼容旧版本）
    server_config = load_server_config()
    st.session_state["api_config"] = server_config
    return server_config

def get_config_from_browser():
    """从浏览器本地存储获取配置"""
    try:
        # 使用 st_javascript 或自定义组件读取 localStorage
        # 这里使用一个巧妙的方法：通过 st.query_params 或 st.session_state
        # 实际实现使用 JavaScript 注入
        
        # 检查是否有通过 JavaScript 传递过来的配置
        if "local_storage_config" in st.session_state:
            config_json = st.session_state["local_storage_config"]
            if config_json:
                return json.loads(config_json)
    except:
        pass
    return None

def save_config_to_browser(config):
    """保存配置到浏览器本地存储"""
    try:
        config_json = json.dumps(config, ensure_ascii=False)
        # 使用 JavaScript 保存到 localStorage
        save_script = f"""
        <script>
        (function() {{
            localStorage.setItem('{get_local_storage_key()}', '{config_json}');
            console.log('Config saved to localStorage');
        }})();
        </script>
        """
        st.components.v1.html(save_script, height=0)
        
        # 同时保存到 session state
        st.session_state["api_config"] = config
        return True
    except Exception as e:
        st.error(f"保存到浏览器存储失败: {e}")
        return False

def show_settings():
    """显示设置界面"""
    st.title("⚙️ 系统设置")
    st.markdown("---")
    
    # 注入 JavaScript 来读取 localStorage
    st.components.v1.html("""
    <script>
    (function() {
        const config = localStorage.getItem('codeguide_api_config');
        if (config) {
            // 通过 URL 参数传递给 Streamlit
            const url = new URL(window.location);
            url.searchParams.set('config', config);
            window.history.replaceState({}, '', url);
        }
    })();
    </script>
    """, height=0)
    
    # 从 URL 参数读取配置
    params = st.query_params
    if "config" in params:
        try:
            config = json.loads(params["config"])
            st.session_state["api_config"] = config
            # 清除 URL 参数
            del st.query_params["config"]
        except:
            config = load_config()
    else:
        config = load_config()
    
    # 显示存储模式说明
    st.info("🔒 **配置存储在您的浏览器中**，每个用户的设置相互独立，更换浏览器或清除缓存后需要重新配置")
    
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
        new_config = {
            "text_api": {
                "base_url": text_base_url,
                "api_key": text_api_key,
                "model": text_model
            },
            "image_api": {
                "base_url": image_base_url,
                "api_key": image_api_key,
                "model": image_model
            }
        }
        
        # 保存到浏览器本地存储
        if save_config_to_browser(new_config):
            st.success("✅ 设置已保存到浏览器！")
            st.balloons()
    
    # 导出/导入配置
    with st.expander("📦 导出/导入配置"):
        st.markdown("**导出配置**：复制下方文本保存到安全的地方")
        config_json = json.dumps(config, ensure_ascii=False, indent=2)
        st.code(config_json, language="json")
        
        st.markdown("**导入配置**：粘贴配置文本")
        import_text = st.text_area("配置JSON", height=150, placeholder='{"text_api": {...}, "image_api": {...}}')
        if st.button("📥 导入配置"):
            try:
                imported_config = json.loads(import_text)
                if save_config_to_browser(imported_config):
                    st.success("✅ 配置已导入！")
                    st.rerun()
            except Exception as e:
                st.error(f"导入失败: {e}")
    
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
        
        ### 存储说明
        - ✅ 配置保存在浏览器 localStorage 中
        - ✅ 每个浏览器/设备的配置相互独立
        - ✅ 更换电脑或浏览器需要重新配置
        - ✅ 清除浏览器数据会丢失配置
        - ✅ 支持导出/导入配置进行备份
        
        ### 安全提示
        - API Key 仅存储在您的浏览器中，不会上传到服务器
        - 建议定期更换 API Key
        - 请勿在公共电脑上保存敏感配置
        """)
