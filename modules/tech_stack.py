import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_tech_stack_prompt(requirement_spec, complexity_level, preferred_stack=""):
    """生成技术栈提示词"""
    return f"""请作为资深技术架构师，基于以下需求规格说明书，生成技术栈与环境预设文档 (Tech_Stack.md)。

## 输入：Requirement_Spec.md

{requirement_spec}

## 复杂度评估

复杂度级别: {complexity_level}
{"首选技术栈: " + preferred_stack if preferred_stack else ""}

## 输出要求

请生成完整的 Tech_Stack.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 01_Requirement_Spec.md
- 文档状态: 草案/已批准

### 2. 技术选型总览
- 架构风格（单体/微服务/Serverless等）
- 技术栈概览图
- 选型理由简述

### 3. 开发环境
#### 3.1 编程语言
- 语言名称及版本（如 Python 3.11, Node.js 18, Java 17）
- 选择理由
- 版本特性说明

#### 3.2 框架与运行时
- 前端框架（如 Next.js 14, React 18, Vue 3）
- 后端框架（如 FastAPI, Express, Spring Boot）
- 运行时环境（如 Node.js, Python VM, JVM）

#### 3.3 开发工具
- IDE推荐
- 代码规范工具（Linter, Formatter）
- 版本控制（Git工作流程）

### 4. 核心依赖库清单
按类别列出所有核心依赖：

#### 4.1 前端依赖
| 库名 | 版本 | 用途 | 安装命令 |
|------|------|------|----------|
| 示例 | ^1.0.0 | UI组件 | npm install xxx |

#### 4.2 后端依赖
| 库名 | 版本 | 用途 | 安装命令 |
|------|------|------|----------|
| 示例 | ^1.0.0 | 数据库ORM | pip install xxx |

#### 4.3 基础设施依赖
- 数据库
- 缓存
- 消息队列
- 搜索引擎

### 5. 目录结构规范
提供推荐的目录结构：

```
project-root/
├── docs/                   # 文档
├── src/                    # 源代码
│   ├── frontend/          # 前端代码
│   ├── backend/           # 后端代码
│   └── shared/            # 共享代码
├── tests/                  # 测试
├── scripts/                # 脚本
├── config/                 # 配置文件
└── README.md
```

并说明每个目录的用途和文件命名规范。

### 6. 环境配置
#### 6.1 开发环境
- 最低硬件要求
- 操作系统要求
- 必要软件清单
- 环境变量模板

#### 6.2 生产环境
- 服务器配置建议
- 容器化方案（Dockerfile示例）
- 部署架构图

#### 6.3 CI/CD配置
- 推荐的CI/CD工具
- 基础流水线配置

### 7. 技术约束与规范
- 编码规范（命名约定、代码风格）
- 提交信息规范
- 分支管理策略
- 代码审查清单

### 8. 风险评估与备选方案
- 技术风险识别
- 备选技术栈
- 降级方案

### 9. 版本锁定策略
- 依赖版本管理策略
- 升级流程
- 兼容性保证

## 格式要求
- 使用标准Markdown格式
- 使用表格展示依赖清单
- 使用代码块展示配置示例
- 确保技术栈轻量化，符合复杂度评估
- **告诉Trae必须在什么约束下工作，防止混用不同版本的语法**

请直接输出Markdown格式的文档内容：
"""

def show_tech_stack():
    """显示技术栈界面"""
    st.title("🛠️ 03. 技术栈与环境预设 (Tech_Stack.md)")
    st.markdown("---")
    
    st.info("""
    **告诉Trae必须在什么约束下工作，防止混用不同版本的语法。**
    
    **输入**: Requirement_Spec.md + 业务复杂度评估
    **输出**: 语言、框架版本、核心依赖库清单、目录结构规范
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取需求文档
    input_method = st.radio(
        "选择Requirement_Spec.md输入方式",
        ["从当前会话获取", "手动粘贴"],
        horizontal=True
    )
    
    if input_method == "从当前会话获取":
        if st.session_state.requirement_spec:
            requirement_spec = st.session_state.requirement_spec
            with st.expander("查看已加载的Requirement_Spec.md"):
                st.markdown(requirement_spec[:2000] + "..." if len(requirement_spec) > 2000 else requirement_spec)
        else:
            st.warning("当前会话没有Requirement_Spec.md，请先生成或选择手动粘贴")
            requirement_spec = ""
    else:
        requirement_spec = st.text_area(
            "粘贴Requirement_Spec.md内容",
            placeholder="请粘贴01_Requirement_Spec.md的完整内容...",
            height=200
        )
    
    # 复杂度评估
    st.subheader("📊 业务复杂度评估")
    
    col1, col2 = st.columns(2)
    with col1:
        complexity_level = st.select_slider(
            "选择复杂度级别",
            options=["极简", "简单", "中等", "复杂", "极复杂"],
            value="中等",
            help="评估业务逻辑的复杂程度"
        )
    with col2:
        preferred_stack = st.text_input(
            "首选技术栈（可选）",
            placeholder="例如：Python + React, Java + Vue",
            help="如果有偏好的技术栈，可以在此指定"
        )
    
    # 复杂度说明
    complexity_desc = {
        "极简": "适合MVP验证，单页应用或简单脚本",
        "简单": "小型项目，单体架构即可满足",
        "中等": "中型项目，可能需要前后端分离",
        "复杂": "大型项目，需要微服务或模块化架构",
        "极复杂": "企业级应用，需要完整的分布式架构"
    }
    st.caption(f"💡 {complexity_desc[complexity_level]}")
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成技术栈文档", type="primary", use_container_width=True):
        if not requirement_spec:
            st.error("请提供Requirement_Spec.md内容！")
            return
        
        with st.spinner("正在生成技术栈文档，请稍候..."):
            prompt = generate_tech_stack_prompt(requirement_spec, complexity_level, preferred_stack)
            content, error = LLMClient.generate_text(prompt, temperature=0.3)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.tech_stack = content
            st.success("✅ 技术栈文档生成完成！")
    
    # 显示结果
    if st.session_state.tech_stack:
        display_result(st.session_state.tech_stack, "03_Tech_Stack.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 复杂度评估指南
        
        | 级别 | 适用场景 | 推荐架构 |
        |------|----------|----------|
        | 极简 | 个人工具、脚本 | 单文件/简单脚本 |
        | 简单 | 小型工具、原型 | 单体应用 |
        | 中等 | 中小型产品 | 前后端分离 |
        | 复杂 | 大型产品、多模块 | 微服务/模块化 |
        | 极复杂 | 企业级应用 | 分布式架构 |
        
        ### 技术栈选择原则
        
        1. **轻量化**: 在满足需求的前提下，尽量减少依赖
        2. **成熟稳定**: 优先选择社区活跃、文档完善的技术
        3. **团队熟悉**: 考虑团队现有技术栈
        4. **生态丰富**: 选择有丰富第三方库的技术
        
        ### 版本约束的重要性
        
        **本文档是Trae开发的约束条件**，必须明确：
        - ✅ 具体的版本号（如 Node.js 18.17.0）
        - ✅ 依赖的精确版本（如 React ^18.2.0）
        - ✅ 语法标准（如 ES2022, Python 3.11+）
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **数据架构与模型** 文档
        """)

