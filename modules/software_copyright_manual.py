import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_manual_prompt(requirement_spec, ui_component, tech_stack, software_name, version):
    """生成软著用户手册提示词"""
    return f"""请作为技术文档工程师，基于以下设计文档，生成符合软著申请标准的《用户手册》(Software_Copyright_Manual.md)。

## 输入信息

**软件名称**: {software_name}
**版本号**: {version}

## 输入：Requirement_Spec.md

{requirement_spec}

## 输入：UI_Component.md

{ui_component}

## 输入：Tech_Stack.md

{tech_stack}

## 输出要求

请生成完整的 Software_Copyright_Manual.md 文档，严格按照以下结构：

---

# {software_name} 用户手册

**版本**: {version}
**编写日期**: 当前日期

---

## 目录

1. 引言
2. 软件环境
3. 功能说明
4. 安装与初始化
5. 操作指南
6. 常见问题

---

## 1. 引言

### 1.1 编写目的
本文档旨在为用户提供[软件名称]的详细使用说明，帮助用户快速了解软件功能并正确使用。

### 1.2 软件概述
[软件名称]是一款[软件类型]软件，主要功能包括：
- [核心功能1]
- [核心功能2]
- [核心功能3]

### 1.3 参考资料
- 需求规格说明书
- 技术架构文档
- 接口设计文档

### 1.4 术语定义
| 术语 | 定义 |
|------|------|
| [术语1] | [定义说明] |
| [术语2] | [定义说明] |

---

## 2. 软件环境

### 2.1 硬件环境
| 项目 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | [配置] | [配置] |
| 内存 | [配置] | [配置] |
| 硬盘 | [配置] | [配置] |
| 显示器 | [配置] | [配置] |

### 2.2 软件环境
| 项目 | 版本要求 |
|------|----------|
| 操作系统 | [Windows 10+/macOS 12+/Ubuntu 20.04+] |
| 浏览器 | [Chrome 90+, Firefox 88+, Safari 14+] |
| 运行时 | [Node.js 18+, Python 3.11+, Java 17+] |
| 数据库 | [PostgreSQL 15+, MySQL 8.0+] |

### 2.3 网络环境
- [网络要求说明]

---

## 3. 功能说明

### 3.1 功能模块总览

| 模块名称 | 功能描述 | 适用用户 |
|----------|----------|----------|
| [模块1] | [描述] | [用户角色] |
| [模块2] | [描述] | [用户角色] |

### 3.2 详细功能说明

#### 3.2.1 [功能模块1名称]

**功能描述**: [详细描述该功能的作用]

**功能特点**:
- [特点1]
- [特点2]
- [特点3]

**输入/输出**:
- 输入: [输入项说明]
- 输出: [输出项说明]

**处理流程**:
1. [步骤1]
2. [步骤2]
3. [步骤3]

---

## 4. 安装与初始化

### 4.1 软件获取
[说明如何获取软件安装包]

### 4.2 安装步骤

#### 4.2.1 环境准备
```bash
# 安装依赖命令示例
npm install
# 或
pip install -r requirements.txt
```

#### 4.2.2 软件安装
1. [安装步骤1]
2. [安装步骤2]
3. [安装步骤3]

#### 4.2.3 数据库初始化
```sql
-- 数据库初始化脚本示例
CREATE DATABASE [数据库名];
```

### 4.3 初始配置
1. [配置项1]: [说明]
2. [配置项2]: [说明]

### 4.4 启动软件
```bash
# 启动命令示例
npm run start
# 或
python app.py
```

---

## 5. 操作指南

### 5.1 登录/启动

#### 5.1.1 启动软件
[插入截图位置标记]
> [Insert Screenshot: 软件启动界面]

**操作步骤**:
1. 双击运行程序
2. 等待加载完成
3. 进入登录界面

#### 5.1.2 用户登录
[插入截图位置标记]
> [Insert Screenshot: 登录界面]

**操作步骤**:
1. 在用户名输入框输入用户名
2. 在密码输入框输入密码
3. 点击"登录"按钮
4. 系统将验证用户信息并进入主界面

**注意事项**:
- 用户名和密码区分大小写
- 连续5次登录失败将锁定账户15分钟

---

### 5.2 [主要功能模块1]操作

#### 5.2.1 进入[功能模块]
[插入截图位置标记]
> [Insert Screenshot: 功能模块入口界面]

用户在主界面点击[菜单/按钮]，系统将显示[功能模块]页面。

#### 5.2.2 [子功能1]操作
[插入截图位置标记]
> [Insert Screenshot: 子功能1操作界面]

**操作步骤**:
1. [步骤1描述]
   - 系统在[XX页面]显示[XX内容]
   - 用户可以看到[XX信息]

2. [步骤2描述]
   - 用户点击[XX按钮]
   - 系统将执行[XX业务逻辑]
   - 界面将[XX变化]

3. [步骤3描述]
   - 操作完成后，系统显示[XX提示]
   - 数据已[XX处理]

**预期结果**: [描述正确操作后的结果]

#### 5.2.3 [子功能2]操作
[插入截图位置标记]
> [Insert Screenshot: 子功能2操作界面]

**操作步骤**:
1. [步骤1]
2. [步骤2]
3. [步骤3]

---

### 5.3 [主要功能模块2]操作

#### 5.3.1 功能入口
[插入截图位置标记]
> [Insert Screenshot: 功能入口界面]

#### 5.3.2 详细操作
[插入截图位置标记]
> [Insert Screenshot: 详细操作界面]

**操作步骤**:
1. [步骤1]
   - 用户在[XX页面]点击[XX按钮]
   - 系统执行[XX业务逻辑]

2. [步骤2]
   - 系统显示[XX结果]
   - 用户可以[XX操作]

---

### 5.4 退出系统

#### 5.4.1 正常退出
[插入截图位置标记]
> [Insert Screenshot: 退出确认界面]

**操作步骤**:
1. 点击右上角[退出/注销]按钮
2. 系统弹出确认对话框
3. 点击"确认"按钮
4. 系统保存当前状态并退出

#### 5.4.2 异常处理
- 如遇系统无响应，可使用任务管理器强制关闭
- 异常关闭后，系统将在下次启动时恢复数据

---

## 6. 常见问题

### Q1: [常见问题1]
**问题描述**: [描述]

**解决方法**: [解决步骤]

### Q2: [常见问题2]
**问题描述**: [描述]

**解决方法**: [解决步骤]

### Q3: 如何联系技术支持？
**解答**: [联系方式]

---

## 附录

### 附录A: 快捷键列表
| 快捷键 | 功能 |
|--------|------|
| Ctrl+S | 保存 |
| Ctrl+F | 搜索 |
| F1 | 帮助 |

### 附录B: 错误代码说明
| 错误代码 | 说明 | 解决方法 |
|----------|------|----------|
| E001 | [说明] | [解决方法] |

---

**文档结束**

---

## 软著手册必备要点检查清单

生成文档后，请确保满足以下要求：

✅ **文档页数**: 建议15-30页（根据软件复杂度调整）
✅ **界面真实**: 截图位置标记清晰，后期替换真实截图
✅ **环境参数**: 明确技术栈运行要求
✅ **术语一致**: 功能名称与代码注释、需求文档统一
✅ **逻辑闭环**: 包含从登录到主要业务完成再到退出的完整流程

请直接输出Markdown格式的文档内容：
"""

def show_software_copyright_manual():
    """显示软著用户手册界面"""
    st.title("📖 09. 软著用户手册 (Software_Copyright_Manual.md)")
    st.markdown("---")
    
    st.info("""
    **符合软著申请标准的《用户手册》**
    
    **输入**: 所有设计文档 + 软件信息
    **输出**: 完整的用户手册，预留截图位置
    
    **避坑指南**:
    - 文档页数：15-30页
    - 截图不出现"Mock数据"字样
    - 术语与代码注释统一
    - 包含完整业务流程
    """)
    
    # 输入区域
    st.subheader("📝 软件基本信息")
    
    col1, col2 = st.columns(2)
    with col1:
        software_name = st.text_input(
            "软件名称 *",
            placeholder="例如：智能库存管理系统V1.0",
            value="智能管理系统V1.0"
        )
    with col2:
        version = st.text_input(
            "版本号 *",
            placeholder="例如：V1.0",
            value="V1.0"
        )
    
    st.markdown("---")
    
    st.subheader("📄 输入设计文档")
    
    # 获取文档
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Requirement_Spec.md**")
        if st.session_state.requirement_spec:
            st.success("✅ 已加载")
            req_spec = st.session_state.requirement_spec
        else:
            st.warning("⚠️ 使用示例")
            req_spec = "需求规格文档示例内容"
    
    with col2:
        st.markdown("**UI_Component.md**")
        if st.session_state.ui_component:
            st.success("✅ 已加载")
            ui_comp = st.session_state.ui_component
        else:
            st.warning("⚠️ 使用示例")
            ui_comp = "UI组件规范文档示例内容"
    
    with col3:
        st.markdown("**Tech_Stack.md**")
        if st.session_state.tech_stack:
            st.success("✅ 已加载")
            tech = st.session_state.tech_stack
        else:
            st.warning("⚠️ 使用示例")
            tech = "技术栈文档示例内容"
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成软著用户手册", type="primary", use_container_width=True):
        with st.spinner("正在生成用户手册，请稍候..."):
            prompt = generate_manual_prompt(req_spec, ui_comp, tech, software_name, version)
            content, error = LLMClient.generate_text(prompt, temperature=0.5)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.software_copyright_manual = content
            st.success("✅ 软著用户手册生成完成！")
    
    # 显示结果
    if st.session_state.software_copyright_manual:
        display_result(st.session_state.software_copyright_manual, "09_Software_Copyright_Manual.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 软著申请流程
        
        1. **生成手册**: 使用本工具生成手册框架
        2. **运行程序**: 启动Trae开发好的软件
        3. **截图补全**: 按照手册中的`[Insert Screenshot]`标记截取真实界面
        4. **替换内容**: 将截图插入到对应位置，替换Mock数据
        5. **导出提交**: 导出为PDF或Word格式提交
        
        ### 截图要求
        
        **必须注意**:
        - ✅ 使用真实或模拟真实的业务数据
        - ❌ 不要出现"test_user_001"等测试数据
        - ❌ 不要出现"Mock数据"等字样
        - ✅ 截图清晰，界面完整
        
        ### 文档结构说明
        
        标准软著手册包含：
        1. **引言**: 编写目的、软件概述、术语定义
        2. **软件环境**: 硬件、软件、网络要求
        3. **功能说明**: 按模块详细说明
        4. **安装与初始化**: 安装步骤、初始配置
        5. **操作指南**: 核心操作流程（最重要）
        6. **常见问题**: FAQ
        
        ### 操作指南编写要点
        
        每个操作必须包含：
        - 界面截图
        - 操作步骤（编号）
        - 系统响应说明
        - 预期结果
        
        示例格式：
        ```
        1. 用户在登录页面输入用户名和密码
           - 系统在输入框显示输入内容
           - 密码显示为掩码
        
        2. 用户点击"登录"按钮
           - 系统验证用户信息
           - 验证通过后跳转到主界面
        ```
        
        ### 术语一致性检查
        
        确保以下文档中的术语一致：
        - 用户手册中的功能名称
        - 代码中的注释
        - 需求文档中的描述
        
        例如：
        - ✅ 统一使用"库存管理"（不要混用"仓储管理"）
        - ✅ 统一使用"订单"（不要混用"单据"）
        
        ### 下一步
        
        生成完成后：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 运行实际程序截图
        4. 替换所有`[Insert Screenshot]`标记
        5. 导出为PDF提交软著申请
        """)

