import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_implementation_prompt(all_docs_summary):
    """生成任务拆解提示词"""
    return f"""请作为资深技术项目经理，基于以下所有设计文档，生成任务拆解指令集 (Implementation_Steps.md)。

## 输入：所有设计文档摘要

{all_docs_summary}

## 输出要求

请生成完整的 Implementation_Steps.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 01-06所有文档
- 文档状态: 草案/已批准
- 预估总工期: （根据复杂度评估）

### 2. 项目里程碑
定义项目的主要里程碑：

| 里程碑 | 目标 | 交付物 | 预计工期 |
|--------|------|--------|----------|
| M1 | 环境搭建 | 可运行的基础框架 | 1-2天 |
| M2 | 核心功能 | 主要业务流程跑通 | 1-2周 |
| M3 | 功能完善 | 所有功能开发完成 | 2-4周 |
| M4 | 测试优化 | 通过所有测试用例 | 1周 |
| M5 | 部署上线 | 生产环境可用 | 2-3天 |

### 3. 详细任务拆解
为每个步骤提供Trae可直接执行的Prompt指令：

#### Step 1: 项目初始化
**任务ID**: STEP-001
**任务名称**: 初始化项目结构
**预计耗时**: 2-4小时
**依赖**: 无
**输入文档**: 03_Tech_Stack.md

**Prompt指令**:
```
请根据03_Tech_Stack.md中的技术栈和目录结构规范，初始化项目：

1. 创建项目根目录和子目录结构
2. 初始化包管理器（npm/pnpm/poetry等）
3. 安装核心依赖
4. 配置开发环境（ESLint, Prettier, 等）
5. 创建基础的配置文件
6. 编写README.md包含启动说明

要求：
- 严格遵循03_Tech_Stack.md中的目录结构
- 使用指定的版本号安装依赖
- 确保`npm run dev`或等效命令可以正常启动
```

**验收标准**:
- [ ] 项目目录结构符合规范
- [ ] 依赖安装无错误
- [ ] 开发服务器可以正常启动
- [ ] README包含清晰的启动说明

#### Step 2: 数据库设计与初始化
**任务ID**: STEP-002
**任务名称**: 实现数据模型
**预计耗时**: 4-8小时
**依赖**: STEP-001
**输入文档**: 04_Data_Model.md

**Prompt指令**:
```
请根据04_Data_Model.md实现数据模型：

1. 创建数据库Schema（SQL文件或迁移文件）
2. 实现ORM模型类
3. 实现数据校验逻辑
4. 创建初始数据迁移脚本
5. 编写数据库连接配置

要求：
- 严格遵循Data_Model.md中的字段定义
- 实现所有约束（NOT NULL, UNIQUE, 外键等）
- 包含数据库索引优化
- 提供数据库初始化脚本
```

**验收标准**:
- [ ] 数据库表结构与文档一致
- [ ] ORM模型可以正常CRUD
- [ ] 数据校验规则生效
- [ ] 迁移脚本可以正常执行

#### Step 3: 后端基础架构
**任务ID**: STEP-003
**任务名称**: 搭建后端基础框架
**预计耗时**: 4-8小时
**依赖**: STEP-001, STEP-002
**输入文档**: 03_Tech_Stack.md, 05_API_Contract.md

**Prompt指令**:
```
请搭建后端基础架构：

1. 创建应用入口文件
2. 配置路由系统
3. 实现中间件（日志、错误处理、CORS等）
4. 实现认证中间件（JWT/Session）
5. 创建统一的响应格式封装
6. 配置数据库连接池

要求：
- 遵循05_API_Contract.md中的响应格式
- 实现全局错误处理
- 包含请求日志记录
```

**验收标准**:
- [ ] 服务器可以正常启动
- [ ] 中间件工作正常
- [ ] 错误处理机制生效
- [ ] 响应格式符合规范

#### Step 4: 实现API接口
**任务ID**: STEP-004
**任务名称**: 实现核心业务API
**预计耗时**: 1-2周
**依赖**: STEP-003
**输入文档**: 05_API_Contract.md, 02_Business_Logic.md

**Prompt指令**:
```
请根据05_API_Contract.md实现所有API接口：

按模块逐个实现：
1. 用户模块API（注册、登录、用户信息）
2. [其他模块]...

每个API需要：
- 实现请求参数校验
- 实现业务逻辑
- 实现响应格式化
- 添加错误处理
- 编写接口注释

要求：
- 严格遵循API_Contract.md中的定义
- 业务逻辑与02_Business_Logic.md对应
- 包含输入验证和错误处理
```

**验收标准**:
- [ ] 所有API可以正常调用
- [ ] 请求响应符合契约
- [ ] 错误处理完善
- [ ] 通过Postman测试

#### Step 5: 前端基础架构
**任务ID**: STEP-005
**任务名称**: 搭建前端基础框架
**预计耗时**: 4-8小时
**依赖**: STEP-001
**输入文档**: 03_Tech_Stack.md, 06_UI_Component.md

**Prompt指令**:
```
请搭建前端基础架构：

1. 配置路由系统（与06_UI_Component.md中的路由表对应）
2. 创建布局组件（MainLayout, AuthLayout）
3. 配置状态管理（Redux/Vuex/Pinia等）
4. 配置HTTP客户端（axios/fetch）
5. 实现认证状态管理
6. 创建基础工具函数

要求：
- 路由与UI_Component.md中的路由表一致
- 实现路由守卫（认证检查）
- 配置API基础URL
```

**验收标准**:
- [ ] 路由系统工作正常
- [ ] 布局组件正确渲染
- [ ] 状态管理可用
- [ ] 可以正常调用后端API

#### Step 6: 实现UI组件
**任务ID**: STEP-006
**任务名称**: 实现基础UI组件
**预计耗时**: 1-3天
**依赖**: STEP-005
**输入文档**: 06_UI_Component.md

**Prompt指令**:
```
请根据06_UI_Component.md实现基础UI组件：

1. 配置设计令牌（颜色、字体、间距）
2. 实现原子组件（Button, Input, Card等）
3. 实现布局组件（Header, Sidebar, Footer）
4. 实现复合组件（Form, Modal, Table等）
5. 配置组件文档

要求：
- 严格遵循设计令牌规范
- 组件Props与文档一致
- 支持所有文档中定义的变体
- 包含基础交互效果
```

**验收标准**:
- [ ] 所有组件可以正常渲染
- [ ] 组件样式符合规范
- [ ] 组件交互正常
- [ ] Props类型正确

#### Step 7: 实现页面
**任务ID**: STEP-007
**任务名称**: 实现所有页面
**预计耗时**: 1-2周
**依赖**: STEP-006
**输入文档**: 06_UI_Component.md, 05_API_Contract.md

**Prompt指令**:
```
请根据06_UI_Component.md实现所有页面：

按优先级逐个实现页面：
1. 登录/注册页面
2. 首页/仪表盘
3. [其他页面]...

每个页面需要：
- 实现页面布局
- 集成UI组件
- 实现页面逻辑
- 连接后端API（使用Mock数据）
- 处理加载和错误状态

要求：
- 页面结构与UI_Component.md一致
- 使用已实现的UI组件
- 替换所有[MOCK]标注的数据为真实API调用
```

**验收标准**:
- [ ] 所有页面可以正常访问
- [ ] 页面布局符合设计
- [ ] 页面交互正常
- [ ] 数据流正确

#### Step 8: 集成与联调
**任务ID**: STEP-008
**任务名称**: 前后端集成
**预计耗时**: 2-3天
**依赖**: STEP-004, STEP-007
**输入文档**: 05_API_Contract.md

**Prompt指令**:
```
请完成前后端集成：

1. 联调所有API接口
2. 处理跨域问题
3. 优化数据加载性能
4. 实现错误提示和重试机制
5. 完善加载状态

要求：
- 所有API调用正常
- 错误处理完善
- 用户体验流畅
```

**验收标准**:
- [ ] 前后端通信正常
- [ ] 所有功能流程跑通
- [ ] 错误处理完善
- [ ] 性能达标

#### Step 9: 测试
**任务ID**: STEP-009
**任务名称**: 编写并执行测试
**预计耗时**: 3-5天
**依赖**: STEP-008
**输入文档**: 08_QA_Spec.md

**Prompt指令**:
```
请根据08_QA_Spec.md实现测试：

1. 编写单元测试
2. 编写集成测试
3. 执行测试用例
4. 修复发现的问题
5. 生成测试报告

要求：
- 核心功能覆盖率>80%
- 所有测试用例通过
- 无严重Bug
```

**验收标准**:
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 覆盖率达标
- [ ] 无P0/P1级Bug

#### Step 10: 部署准备
**任务ID**: STEP-010
**任务名称**: 部署配置
**预计耗时**: 1-2天
**依赖**: STEP-009
**输入文档**: 03_Tech_Stack.md

**Prompt指令**:
```
请完成部署准备：

1. 创建生产环境配置
2. 编写Dockerfile
3. 配置CI/CD流水线
4. 准备部署脚本
5. 编写部署文档

要求：
- 配置环境变量分离
- 优化构建产物
- 确保可一键部署
```

**验收标准**:
- [ ] 可以构建生产包
- [ ] Docker镜像可运行
- [ ] 部署文档完整
- [ ] 生产环境配置正确

### 4. 依赖关系图
使用Mermaid语法展示任务依赖关系：

```mermaid
gantt
    title 项目任务甘特图
    dateFormat  YYYY-MM-DD
    section 基础
    项目初始化       :done, step1, 2024-01-01, 1d
    数据库设计       :done, step2, after step1, 1d
    section 后端
    后端架构         :step3, after step2, 1d
    API实现          :step4, after step3, 5d
    section 前端
    前端架构         :step5, after step1, 1d
    UI组件           :step6, after step5, 2d
    页面实现         :step7, after step6, 5d
    section 收尾
    集成联调         :step8, after step4, 2d
    测试             :step9, after step8, 3d
    部署             :step10, after step9, 1d
```

### 5. 风险提示
列出可能的风险和应对措施：

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 第三方API不稳定 | 高 | 中 | 准备Mock数据和降级方案 |
| 性能瓶颈 | 中 | 中 | 提前进行压力测试 |

### 6. 给Trae的使用说明
**执行指挥棒。避免一次性给Trae太多信息，分批次加载MD完成开发。**

使用方式：
1. 每次只给Trae一个Step的Prompt
2. 等待Trae完成并验证
3. 确认无误后再进行下一个Step
4. 如遇到错误，参考对应文档进行修正

## 格式要求
- 使用标准Markdown格式
- 每个Step的Prompt必须可直接复制给Trae使用
- 包含明确的验收标准
- 提供依赖关系图
- **这是执行指挥棒，必须清晰可执行**

请直接输出Markdown格式的文档内容：
"""

def show_implementation_steps():
    """显示任务拆解界面"""
    st.title("📋 07. 任务拆解指令集 (Implementation_Steps.md)")
    st.markdown("---")
    
    st.info("""
    **执行指挥棒。避免一次性给Trae太多信息，分批次加载MD完成开发。**
    
    **输入**: 以上所有MD文档
    **输出**: 给Trae的分步骤Prompt指令
    
    **逻辑**: Step 1: 初始化项目结构；Step 2: 实现Auth模块...
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取所有文档
    docs_available = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**可用文档**")
        if st.session_state.requirement_spec:
            st.success("✅ 01_Requirement_Spec.md")
            docs_available.append("需求规格")
        else:
            st.error("❌ 01_Requirement_Spec.md")
        
        if st.session_state.business_logic:
            st.success("✅ 02_Business_Logic.md")
            docs_available.append("业务逻辑")
        else:
            st.error("❌ 02_Business_Logic.md")
        
        if st.session_state.tech_stack:
            st.success("✅ 03_Tech_Stack.md")
            docs_available.append("技术栈")
        else:
            st.error("❌ 03_Tech_Stack.md")
    
    with col2:
        st.markdown("**可用文档**")
        if st.session_state.data_model:
            st.success("✅ 04_Data_Model.md")
            docs_available.append("数据模型")
        else:
            st.error("❌ 04_Data_Model.md")
        
        if st.session_state.api_contract:
            st.success("✅ 05_API_Contract.md")
            docs_available.append("接口契约")
        else:
            st.error("❌ 05_API_Contract.md")
        
        if st.session_state.ui_component:
            st.success("✅ 06_UI_Component.md")
            docs_available.append("UI组件")
        else:
            st.error("❌ 06_UI_Component.md")
    
    # 构建文档摘要
    all_docs_summary = f"""
已生成文档: {', '.join(docs_available)}

各文档关键信息摘要：

1. **需求规格**: 
   - 包含功能需求清单和核心用例
   - 定义了用户角色和业务流程

2. **业务逻辑**:
   - 包含业务流程图和状态机
   - 定义了核心业务规则

3. **技术栈**:
   - 确定了编程语言和框架
   - 定义了目录结构和依赖

4. **数据模型**:
   - 包含数据库Schema设计
   - 定义了实体类和字段约束

5. **接口契约**:
   - 包含详细的API定义
   - 定义了请求响应格式

6. **UI组件**:
   - 包含页面路由和组件规范
   - 定义了设计系统和Mock数据
"""
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成任务拆解指令集", type="primary", use_container_width=True):
        if len(docs_available) < 3:
            st.warning("建议先生成更多设计文档以获得更好的任务拆解效果，但也可以继续生成基础版本。")
        
        with st.spinner("正在生成任务拆解指令集，请稍候..."):
            prompt = generate_implementation_prompt(all_docs_summary)
            content, error = LLMClient.generate_text(prompt, temperature=0.4)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.implementation_steps = content
            st.success("✅ 任务拆解指令集生成完成！")
    
    # 显示结果
    if st.session_state.implementation_steps:
        display_result(st.session_state.implementation_steps, "07_Implementation_Steps.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 分步执行策略
        
        **重要**: 不要一次性给Trae所有步骤！按以下方式执行：
        
        1. **一次一个Step**: 每次只复制一个Step的Prompt给Trae
        2. **验证再下一步**: 确认当前Step完成并验收通过
        3. **有问题回头**: 如果遇到问题，参考对应的设计文档修正
        4. **保持耐心**: 大型项目可能需要多次迭代
        
        ### Step结构说明
        
        每个Step包含：
        - **任务ID和名称**: 唯一标识
        - **预计耗时**: 参考时间
        - **依赖**: 必须先完成的Step
        - **输入文档**: 需要参考的MD文件
        - **Prompt指令**: 可直接复制给Trae的指令
        - **验收标准**: 完成 checklist
        
        ### 与Trae协作流程
        
        ```
        你: 复制Step 1的Prompt → Trae
        Trae: 执行并返回结果
        你: 验证验收标准
        你: 复制Step 2的Prompt → Trae
        ...
        ```
        
        ### 应对问题
        
        如果Trae执行出错：
        1. 检查输入文档是否清晰
        2. 提供更具体的约束
        3. 将大Step拆分为更小的Step
        4. 必要时人工介入调整
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 开始按Step指导Trae开发
        4. 继续生成 **测试用例与验收准则** 文档
        """)

