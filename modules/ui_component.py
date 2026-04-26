import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_ui_component_prompt(requirement_spec, tech_stack, design_preference=""):
    """生成UI组件规范提示词"""
    return f"""请作为资深UI/UX设计师和前端架构师，基于以下需求规格和技术栈，生成UI/UX表现组件规范文档 (UI_Component.md)。

## 输入：Requirement_Spec.md

{requirement_spec}

## 输入：Tech_Stack.md

{tech_stack}

## 设计偏好
{design_preference if design_preference else "根据需求自动选择合适的设计风格"}

## 输出要求

请生成完整的 UI_Component.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 01_Requirement_Spec.md, 03_Tech_Stack.md
- 文档状态: 草案/已批准

### 2. 设计系统概述
- 设计理念
- 设计原则
- 目标用户体验
- 响应式策略

### 3. 页面路由表
完整的页面路由定义：

| 路由ID | 路径 | 页面名称 | 功能描述 | 权限要求 | 布局类型 |
|--------|------|----------|----------|----------|----------|
| R-001 | / | 首页 | 产品展示 | 公开 | MainLayout |
| R-002 | /login | 登录页 | 用户登录 | 公开 | AuthLayout |
| R-003 | /dashboard | 仪表盘 | 数据概览 | 需登录 | MainLayout |

### 4. 组件层级结构
提供组件树状结构：

```
App
├── Layouts
│   ├── MainLayout
│   │   ├── Header
│   │   ├── Sidebar
│   │   └── Footer
│   └── AuthLayout
├── Pages
│   ├── Home
│   │   ├── HeroSection
│   │   ├── FeatureList
│   │   └── CTASection
│   └── Dashboard
│       ├── StatsCard
│       └── ChartWidget
└── Shared
    ├── Button
    ├── Input
    └── Modal
```

### 5. 设计令牌 (Design Tokens)
#### 5.1 色彩系统
**主色调**:
| 名称 | 色值 | 用途 |
|------|------|------|
| primary-50 | #E3F2FD | 浅色背景 |
| primary-500 | #2196F3 | 主按钮 |
| primary-700 | #1976D2 | 悬停状态 |

**中性色**:
| 名称 | 色值 | 用途 |
|------|------|------|
| gray-50 | #FAFAFA | 页面背景 |
| gray-900 | #212121 | 主要文字 |

**功能色**:
| 名称 | 色值 | 用途 |
|------|------|------|
| success | #4CAF50 | 成功状态 |
| warning | #FF9800 | 警告状态 |
| error | #F44336 | 错误状态 |

#### 5.2 字体系统
| 级别 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| H1 | 32px | 700 | 1.2 | 页面标题 |
| H2 | 24px | 600 | 1.3 | 区块标题 |
| Body | 16px | 400 | 1.5 | 正文 |
| Caption | 12px | 400 | 1.4 | 辅助文字 |

#### 5.3 间距系统
| 名称 | 值 | 用途 |
|------|-----|------|
| xs | 4px | 紧凑间距 |
| sm | 8px | 小组件间距 |
| md | 16px | 默认间距 |
| lg | 24px | 大区块间距 |
| xl | 32px | 页面间距 |

#### 5.4 圆角与阴影
| 名称 | 值 | 用途 |
|------|-----|------|
| radius-sm | 4px | 小按钮 |
| radius-md | 8px | 卡片 |
| shadow-sm | 0 1px 2px rgba(0,0,0,0.05) | 轻微阴影 |
| shadow-md | 0 4px 6px rgba(0,0,0,0.1) | 卡片阴影 |

### 6. 组件规范
为每个核心组件提供详细规范：

#### 6.1 Button组件
**组件ID**: COMP-001
**组件名称**: Button
**用途**: 触发操作

**Props定义**:
| 属性 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| variant | 'primary'|'secondary'|'text' | 否 | 'primary' | 按钮样式 |
| size | 'sm'|'md'|'lg' | 否 | 'md' | 按钮尺寸 |
| disabled | boolean | 否 | false | 是否禁用 |
| onClick | function | 否 | - | 点击回调 |
| children | ReactNode | 是 | - | 按钮内容 |

**样式规范**:
- Primary: bg-primary-500, text-white, hover:bg-primary-700
- Secondary: bg-gray-100, text-gray-900, border
- Size sm: px-3 py-1.5 text-sm
- Size md: px-4 py-2 text-base

**使用示例**:
```tsx
<Button variant="primary" size="md" onClick={{handleSubmit}}>
  提交
</Button>
```

#### 6.2 Input组件
**组件ID**: COMP-002
**组件名称**: Input
**用途**: 文本输入

**Props定义**:
| 属性 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| type | string | 否 | 'text' | 输入类型 |
| placeholder | string | 否 | - | 占位符 |
| value | string | 否 | - | 值 |
| onChange | function | 否 | - | 变化回调 |
| error | string | 否 | - | 错误信息 |

**样式规范**:
- 默认: border-gray-300, focus:border-primary-500
- 错误: border-error, text-error

### 7. 页面详细设计
为每个主要页面提供线框图级别的描述：

#### 7.1 首页 (/)
**布局结构**:
- Header (固定顶部)
  - Logo (左侧)
  - 导航菜单 (中间)
  - 登录/注册按钮 (右侧)
- Hero区域 (全宽)
  - 标题
  - 副标题
  - CTA按钮
- Features区域
  - 3列网格展示特性
- Footer

**交互说明**:
- 导航菜单悬停效果
- CTA按钮点击跳转
- 特性卡片悬停动画

### 8. Mock数据需求
**重要**: 明确标注所有Mock数据，后期需要替换

| 数据项 | 数据类型 | 示例值 | 替换来源 | 标注 |
|--------|----------|--------|----------|------|
| user.name | string | "张三" | API: GET /api/v1/user | [MOCK] |
| stats.total | number | 1234 | API: GET /api/v1/stats | [MOCK] |
| chart.data | array | [10,20,30] | API: GET /api/v1/chart | [MOCK] |

### 9. 响应式断点
| 断点名 | 宽度 | 布局调整 |
|--------|------|----------|
| mobile | < 640px | 单列布局 |
| tablet | 640px - 1024px | 双列布局 |
| desktop | > 1024px | 完整布局 |

### 10. 动画与过渡
| 动画名 | 时长 | 缓动函数 | 用途 |
|--------|------|----------|------|
| fadeIn | 200ms | ease-out | 淡入 |
| slideUp | 300ms | cubic-bezier | 上滑 |
| pulse | 1s | ease-in-out | 脉冲提示 |

### 11. 图标系统
- 图标库选择
- 图标命名规范
- 常用图标清单

### 12. 图片资源规范
- 图片格式要求
- 尺寸规范
- 压缩标准
- 命名规范

## 格式要求
- 使用标准Markdown格式
- 使用表格展示结构化数据
- 使用代码块展示组件代码示例
- **将视觉需求转化为Trae可理解的组件层级**
- **Mock数据必须明确标注，便于后期替换**

请直接输出Markdown格式的文档内容：
"""

def show_ui_component():
    """显示UI组件规范界面"""
    st.title("🎨 06. UI/UX表现组件规范 (UI_Component.md)")
    st.markdown("---")
    
    st.info("""
    **将视觉需求转化为Trae可理解的组件层级。**
    
    **输入**: Requirement_Spec.md + 交互逻辑
    **输出**: 页面路由表、组件拆解图、配色与字号规范、Mock数据需求
    
    **注意**: Mock数据要明确标注，后期要替换
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取需求文档
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Requirement_Spec.md**")
        req_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="req_input_ui",
            horizontal=True
        )
        
        if req_input_method == "从当前会话获取":
            if st.session_state.requirement_spec:
                requirement_spec = st.session_state.requirement_spec
                with st.expander("查看已加载内容"):
                    st.markdown(requirement_spec[:1500] + "..." if len(requirement_spec) > 1500 else requirement_spec)
            else:
                st.warning("当前会话没有Requirement_Spec.md")
                requirement_spec = ""
        else:
            requirement_spec = st.text_area(
                "粘贴Requirement_Spec.md",
                placeholder="请粘贴01_Requirement_Spec.md的完整内容...",
                height=150,
                key="req_paste_ui"
            )
    
    with col2:
        st.markdown("**Tech_Stack.md**")
        ts_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="ts_input_ui",
            horizontal=True
        )
        
        if ts_input_method == "从当前会话获取":
            if st.session_state.tech_stack:
                tech_stack = st.session_state.tech_stack
                with st.expander("查看已加载内容"):
                    st.markdown(tech_stack[:1000] + "..." if len(tech_stack) > 1000 else tech_stack)
            else:
                st.warning("当前会话没有Tech_Stack.md")
                tech_stack = ""
        else:
            tech_stack = st.text_area(
                "粘贴Tech_Stack.md",
                placeholder="请粘贴03_Tech_Stack.md内容...",
                height=150,
                key="ts_paste_ui"
            )
    
    # 设计偏好
    st.subheader("🎨 设计偏好（可选）")
    design_preference = st.text_area(
        "指定设计风格",
        placeholder="例如：\n- 设计风格：现代简约/商务正式/活泼年轻\n- 主色调：蓝色系\n- 参考产品：Notion, Figma, 或 Ant Design",
        height=80
    )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成UI组件规范", type="primary", use_container_width=True):
        if not requirement_spec or not tech_stack:
            st.error("请提供Requirement_Spec.md和Tech_Stack.md内容！")
            return
        
        with st.spinner("正在生成UI组件规范，请稍候..."):
            prompt = generate_ui_component_prompt(requirement_spec, tech_stack, design_preference)
            content, error = LLMClient.generate_text(prompt, temperature=0.5)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.ui_component = content
            st.success("✅ UI组件规范生成完成！")
    
    # 显示结果
    if st.session_state.ui_component:
        display_result(st.session_state.ui_component, "06_UI_Component.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 组件设计原则
        
        1. **原子化设计**: 从原子（颜色、字体）到分子（按钮、输入框）再到组织（表单、卡片）
        2. **一致性**: 相同功能的组件保持一致的视觉和交互
        3. **可复用性**: 组件应该足够通用，能在多个场景复用
        4. **可访问性**: 考虑色盲用户、键盘导航等
        
        ### Mock数据标注
        
        **重要**: 所有Mock数据必须明确标注 `[MOCK]`，便于后期查找替换：
        
        ```tsx
        // ❌ 错误 - 无法识别是Mock数据
        const user = {{ name: "张三" }};
        
        // ✅ 正确 - 明确标注
        const user = {{ name: "张三" }}; // [MOCK] 替换为 API: GET /api/v1/user
        ```
        
        ### 设计令牌 (Design Tokens)
        
        设计令牌是设计系统的核心，包括：
        - **颜色**: 主色、中性色、功能色
        - **字体**: 字体家族、字号、字重、行高
        - **间距**: 基础间距单位（通常是4px或8px）
        - **圆角**: 组件圆角大小
        - **阴影**: 不同层级的阴影
        
        ### 响应式设计
        
        移动端优先的设计策略：
        1. 先设计移动端布局
        2. 逐步扩展到平板和桌面
        3. 使用相对单位（rem, %）
        4. 关键断点: 640px, 1024px, 1280px
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **任务拆解指令集** 文档
        """)

