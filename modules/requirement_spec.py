import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_requirement_prompt(software_name, original_idea, target_users, core_features):
    """生成需求定义提示词"""
    return f"""请作为资深软件架构师，基于以下信息生成结构化的需求规格说明书 (Requirement_Spec.md)。

## 输入信息

**软件名称**: {software_name}

**原始创意/愿景**: 
{original_idea}

**目标用户群体**: 
{target_users}

**核心功能描述**: 
{core_features}

## 输出要求

请生成完整的 Requirement_Spec.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 创建日期: 当前日期
- 文档状态: 草案/已批准

### 2. 项目概述
- 项目背景
- 项目目标
- 项目范围（包含/不包含）

### 3. 用户角色定义
列出所有用户角色，每个角色包含：
- 角色名称
- 角色描述
- 主要职责
- 使用频率

### 4. 功能需求清单
按模块组织功能，每个功能包含：
- 功能ID（如 F-001, F-002）
- 功能名称
- 功能描述
- 优先级（高/中/低）
- 关联用户角色
- 验收标准

### 5. 非功能需求
- 性能要求
- 安全要求
- 可用性要求
- 可扩展性要求
- 兼容性要求

### 6. 核心用例
提供3-5个核心用例，每个用例包含：
- 用例ID
- 用例名称
- 参与者
- 前置条件
- 主流程（步骤编号）
- 备选流程
- 后置条件

### 7. 术语表
定义项目中使用的专业术语

### 8. 参考资料

## 格式要求
- 使用标准Markdown格式
- 使用表格展示结构化数据
- 使用编号列表表示步骤
- 确保内容详细、专业、可执行
- 这是所有后续文档的"宪法"，必须准确完整

请直接输出Markdown格式的文档内容：
"""

def show_requirement_spec():
    """显示需求定义界面"""
    st.title("📋 01. 需求定义 (Requirement_Spec.md)")
    st.markdown("---")
    
    st.info("""
    **这是所有后续文档的"宪法"**，确保AI不偏离初衷。
    
    **输入**: 软件名称和原始创意
    **输出**: 结构化的功能清单、用户角色、核心用例
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    software_name = st.text_input(
        "软件名称 *",
        placeholder="例如：智能库存管理系统",
        help="您的软件产品名称"
    )
    
    original_idea = st.text_area(
        "原始创意/愿景 *",
        placeholder="描述您的软件创意，包括要解决什么问题、为谁解决、如何创造价值...",
        height=120,
        help="详细描述您的软件创意和愿景"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        target_users = st.text_area(
            "目标用户群体 *",
            placeholder="例如：\n- 中小企业仓库管理员\n- 电商运营人员\n- 供应链经理",
            height=100,
            help="描述您的目标用户"
        )
    with col2:
        core_features = st.text_area(
            "核心功能描述 *",
            placeholder="例如：\n- 库存实时监控\n- 自动补货提醒\n- 多仓库管理\n- 数据报表分析",
            height=100,
            help="列出核心功能点"
        )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成需求规格说明书", type="primary", use_container_width=True):
        if not all([software_name, original_idea, target_users, core_features]):
            st.error("请填写所有必填字段！")
            return
        
        with st.spinner("正在生成需求规格说明书，请稍候..."):
            prompt = generate_requirement_prompt(software_name, original_idea, target_users, core_features)
            content, error = LLMClient.generate_text(prompt)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.requirement_spec = content
            st.success("✅ 需求规格说明书生成完成！")
    
    # 显示结果
    if st.session_state.requirement_spec:
        display_result(st.session_state.requirement_spec, "01_Requirement_Spec.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 填写建议
        
        1. **软件名称**: 简洁明了，体现产品核心价值
        2. **原始创意**: 
           - 描述要解决的核心问题
           - 说明目标用户群体
           - 阐述产品的独特价值
        3. **目标用户**: 尽可能详细，包括用户特征、使用场景
        4. **核心功能**: 列出最重要的3-7个功能点
        
        ### 输出说明
        
        生成的文档将包含：
        - ✅ 完整的用户角色定义
        - ✅ 结构化的功能需求清单
        - ✅ 详细的用例描述
        - ✅ 非功能性需求
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **业务逻辑与状态机** 文档
        """)

