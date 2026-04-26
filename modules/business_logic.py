import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_business_logic_prompt(requirement_spec):
    """生成业务逻辑提示词"""
    return f"""请作为资深软件架构师，基于以下需求规格说明书，生成业务逻辑与状态机文档 (Business_Logic.md)。

## 输入：Requirement_Spec.md

{requirement_spec}

## 输出要求

请生成完整的 Business_Logic.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 01_Requirement_Spec.md
- 文档状态: 草案/已批准

### 2. 核心业务领域
- 领域概述
- 领域边界定义
- 核心领域对象

### 3. 业务流程图 (Mermaid语法)
为每个核心业务流程提供Mermaid流程图，包括：
- 流程名称
- 流程描述
- Mermaid流程图代码（使用标准flowchart TD语法）
- 流程步骤说明（编号必须与流程图对应）

**重要**: 业务步骤编号必须与后续API接口对应，例如：
- BL-001: 用户注册流程
- BL-002: 订单创建流程

### 4. 状态机定义
为每个有状态的业务对象提供状态机：
- 对象名称
- 状态列表
- 状态转换图 (Mermaid stateDiagram-v2)
- 转换条件说明
- 触发事件列表

### 5. 全局状态管理
- 全局状态分类
- 状态存储策略
- 状态同步机制
- 缓存策略

### 6. 关键算法伪代码
为核心业务逻辑提供伪代码，包括：
- 算法名称
- 输入/输出定义
- 伪代码（使用类Python语法）
- 复杂度分析
- 边界条件处理

### 7. 业务规则清单
- 规则ID（如 BR-001）
- 规则描述
- 规则类型（验证/计算/流程控制）
- 适用场景
- 优先级

### 8. 业务事件定义
- 事件ID（如 EVT-001）
- 事件名称
- 事件触发条件
- 事件处理器
- 关联的业务流程

### 9. 一致性检查点
- 与需求文档的对应关系表
- 业务步骤与API的映射关系（预留）

## 格式要求
- 使用标准Markdown格式
- Mermaid图表使用代码块包裹，标注语言为mermaid
- 伪代码使用代码块包裹，标注语言为python
- 使用表格展示结构化数据
- 确保业务闭环，每个流程都有明确的开始和结束

请直接输出Markdown格式的文档内容：
"""

def show_business_logic():
    """显示业务逻辑界面"""
    st.title("⚙️ 02. 业务逻辑与状态机 (Business_Logic.md)")
    st.markdown("---")
    
    st.info("""
    **在写代码前，先让AI确认业务闭环。**
    
    **输入**: Requirement_Spec.md
    **输出**: 核心业务流程图（Mermaid语法）、全局状态管理、关键算法伪代码
    
    **一致性点**: 业务步骤编号必须与后续API接口对应
    """)
    
    # 输入区域
    st.subheader("📝 输入Requirement_Spec.md")
    
    # 提供两种方式：粘贴或从session state获取
    input_method = st.radio(
        "选择输入方式",
        ["从当前会话获取", "手动粘贴"],
        horizontal=True
    )
    
    if input_method == "从当前会话获取":
        if st.session_state.requirement_spec:
            requirement_spec = st.session_state.requirement_spec
            with st.expander("查看已加载的Requirement_Spec.md"):
                st.markdown(requirement_spec)
        else:
            st.warning("当前会话没有Requirement_Spec.md，请先生成或选择手动粘贴")
            requirement_spec = ""
    else:
        requirement_spec = st.text_area(
            "粘贴Requirement_Spec.md内容",
            placeholder="请粘贴01_Requirement_Spec.md的完整内容...",
            height=300
        )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成业务逻辑文档", type="primary", use_container_width=True):
        if not requirement_spec:
            st.error("请提供Requirement_Spec.md内容！")
            return
        
        with st.spinner("正在生成业务逻辑文档，请稍候..."):
            prompt = generate_business_logic_prompt(requirement_spec)
            content, error = LLMClient.generate_text(prompt, temperature=0.5)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.business_logic = content
            st.success("✅ 业务逻辑文档生成完成！")
    
    # 显示结果
    if st.session_state.business_logic:
        display_result(st.session_state.business_logic, "02_Business_Logic.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 文档说明
        
        本文档是业务层面的核心设计，确保：
        1. **业务闭环**: 每个流程都有明确的开始和结束
        2. **状态清晰**: 所有状态转换都有明确的条件和触发器
        3. **算法可行**: 核心算法经过伪代码验证
        
        ### Mermaid图表
        
        生成的Mermaid图表可以在以下工具中预览：
        - [Mermaid Live Editor](https://mermaid.live/)
        - GitHub/GitLab Markdown
        - VS Code + Mermaid插件
        
        ### 一致性要求
        
        **重要**: 本文档中的业务步骤编号（如 BL-001）必须与后续API接口对应：
        - BL-001 → API: POST /api/v1/users/register
        - BL-002 → API: POST /api/v1/orders/create
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **技术栈与环境预设** 文档
        """)

