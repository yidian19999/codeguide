import streamlit as st
import base64
from io import BytesIO

def copy_to_clipboard(text):
    """生成复制到剪贴板的HTML组件"""
    # 使用JavaScript实现复制功能
    copy_js = f"""
    <script>
    function copyToClipboard_{hash(text) & 0xFFFFFFFF}(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert('已复制到剪贴板！');
        }}, function(err) {{
            alert('复制失败: ' + err);
        }});
    }}
    </script>
    <button onclick="copyToClipboard_{hash(text) & 0xFFFFFFFF}(`{text.replace('`', '\\`')}`)" 
            style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; 
                   border-radius: 4px; cursor: pointer; margin: 5px 0;">
        📋 复制内容
    </button>
    """
    st.components.v1.html(copy_js, height=50)

def download_md_file(content, filename):
    """生成下载Markdown文件的链接"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'''
    <a href="data:text/markdown;base64,{b64}" download="{filename}" 
       style="background-color: #2196F3; color: white; text-decoration: none; 
              padding: 8px 16px; border-radius: 4px; display: inline-block; margin: 5px 0;">
        📥 下载 {filename}
    </a>
    '''
    st.markdown(href, unsafe_allow_html=True)

def display_result(content, filename):
    """显示结果，带复制和下载功能"""
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"📋 复制 {filename} 内容", key=f"copy_{filename}"):
            st.session_state[f"copy_text_{filename}"] = content
            st.success("内容已准备复制！")
            
    with col2:
        download_md_file(content, filename)
    
    # 显示内容预览
    with st.expander("📄 内容预览", expanded=True):
        st.markdown(content)
    
    return content

def init_session_state():
    """初始化session state"""
    if "requirement_spec" not in st.session_state:
        st.session_state.requirement_spec = ""
    if "business_logic" not in st.session_state:
        st.session_state.business_logic = ""
    if "tech_stack" not in st.session_state:
        st.session_state.tech_stack = ""
    if "data_model" not in st.session_state:
        st.session_state.data_model = ""
    if "api_contract" not in st.session_state:
        st.session_state.api_contract = ""
    if "ui_component" not in st.session_state:
        st.session_state.ui_component = ""
    if "implementation_steps" not in st.session_state:
        st.session_state.implementation_steps = ""
    if "qa_spec" not in st.session_state:
        st.session_state.qa_spec = ""
    if "software_copyright_manual" not in st.session_state:
        st.session_state.software_copyright_manual = ""
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
