import streamlit as st
from utils import init_session_state

st.set_page_config(
    page_title="CodeGuide - AI软件开发助手",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()

# 导入所有模块
from modules.requirement_spec import show_requirement_spec
from modules.business_logic import show_business_logic
from modules.tech_stack import show_tech_stack
from modules.data_model import show_data_model
from modules.api_contract import show_api_contract
from modules.ui_component import show_ui_component
from modules.implementation_steps import show_implementation_steps
from modules.qa_spec import show_qa_spec
from modules.software_copyright_manual import show_software_copyright_manual
from modules.ui_screenshot_generator import show_ui_screenshot_generator
from modules.settings import show_settings

def main():
    # 侧边栏导航
    with st.sidebar:
        st.title("🚀 CodeGuide")
        st.markdown("---")
        
        # 导航菜单 - 按1-10顺序排列，中文命名
        st.markdown("### 📑 导航菜单")
        
        nav_items = [
            ("1️⃣ 需求定义", "requirement_spec"),
            ("2️⃣ 业务逻辑", "business_logic"),
            ("3️⃣ 技术栈", "tech_stack"),
            ("4️⃣ 数据模型", "data_model"),
            ("5️⃣ 接口契约", "api_contract"),
            ("6️⃣ 界面规范", "ui_component"),
            ("7️⃣ 开发任务", "implementation_steps"),
            ("8️⃣ 测试规范", "qa_spec"),
            ("9️⃣ 软著手册", "software_copyright_manual"),
            ("🔟 截图生成", "ui_screenshot_generator"),
        ]
        
        for label, state_key in nav_items:
            has_content = bool(st.session_state.get(state_key, ""))
            icon = "✅" if has_content else ""
            
            if st.button(f"{label} {icon}", use_container_width=True, key=f"nav_{state_key}"):
                st.session_state.current_page = state_key
                st.rerun()
        
        st.markdown("---")
        
        # 系统设置按钮
        if st.button("⚙️ 系统设置", use_container_width=True, key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        
        st.markdown("---")
        st.caption("v1.0 | CodeGuide")
    
    # 主内容区 - 根据当前页面显示不同内容
    current_page = st.session_state.get("current_page", "home")
    
    if current_page == "home":
        show_home()
    elif current_page == "requirement_spec":
        show_requirement_spec()
    elif current_page == "business_logic":
        show_business_logic()
    elif current_page == "tech_stack":
        show_tech_stack()
    elif current_page == "data_model":
        show_data_model()
    elif current_page == "api_contract":
        show_api_contract()
    elif current_page == "ui_component":
        show_ui_component()
    elif current_page == "implementation_steps":
        show_implementation_steps()
    elif current_page == "qa_spec":
        show_qa_spec()
    elif current_page == "software_copyright_manual":
        show_software_copyright_manual()
    elif current_page == "ui_screenshot_generator":
        show_ui_screenshot_generator()
    elif current_page == "settings":
        show_settings()

def show_home():
    """显示首页"""
    st.title("🚀 CodeGuide")
    st.markdown("---")
    
    st.markdown("""
    ## 欢迎使用CodeGuide
    
    本系统帮助您通过AI生成完整的软件开发文档体系。
    
    ### 📋 系统功能
    
    | 模块 | 功能描述 | 输出文档 |
    |------|----------|----------|
    | **1️⃣ 需求定义** | 分析软件创意，生成结构化需求 | Requirement_Spec.md |
    | **2️⃣ 业务逻辑** | 设计业务流程和状态机 | Business_Logic.md |
    | **3️⃣ 技术栈** | 确定技术选型和环境 | Tech_Stack.md |
    | **4️⃣ 数据模型** | 设计数据库Schema | Data_Model.md |
    | **5️⃣ 接口契约** | 定义API接口规范 | API_Contract.md |
    | **6️⃣ 界面规范** | 设计UI系统和组件 | UI_Component.md |
    | **7️⃣ 开发任务** | 生成开发步骤指令 | Implementation_Steps.md |
    | **8️⃣ 测试规范** | 制定测试策略 | QA_Spec.md |
    | **9️⃣ 软著手册** | 生成软著申请文档 | Software_Copyright_Manual.md |
    | **🔟 截图生成** | 生成界面截图素材 | PNG图片 |
    
    ### 🚀 快速开始
    
    1. **配置API**: 先在左侧导航点击"⚙️ 系统设置"配置OpenAI格式的API
    2. **按序生成**: 按照1-10的顺序生成各文档（后面的文档依赖前面的）
    3. **导出使用**: 每个文档都支持复制和下载为.md文件
    
    ### 💡 使用建议
    
    - **第一步**: 先生成"需求定义"文档，这是所有后续文档的基础
    - **顺序执行**: 建议按顺序生成，确保文档间的一致性
    - **迭代优化**: 可以多次生成，逐步完善文档内容
    - **人工审核**: AI生成的内容需要人工审核和调整
    
    ### ⚠️ 注意事项
    
    1. **API配置**: 使用前必须在设置中配置API密钥
    2. **文档依赖**: 后面的文档依赖前面的文档内容
    3. **数据保存**: 文档保存在当前会话中，刷新页面会丢失
    4. **及时导出**: 建议生成后立即下载保存
    """)
    
    # 快捷操作按钮
    st.markdown("---")
    st.subheader("⚡ 快捷操作")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚙️ 前往设置", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
    
    with col2:
        if st.button("📋 开始需求定义", use_container_width=True):
            st.session_state.current_page = "requirement_spec"
            st.rerun()
    
    with col3:
        if st.button("📖 生成软著手册", use_container_width=True):
            st.session_state.current_page = "software_copyright_manual"
            st.rerun()

if __name__ == "__main__":
    main()
