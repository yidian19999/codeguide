import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_api_contract_prompt(data_model, business_logic, api_style="REST"):
    """生成接口契约提示词"""
    return f"""请作为资深API架构师，基于以下数据模型和业务逻辑，生成接口契约文档 (API_Contract.md)。

## 输入：Data_Model.md

{data_model}

## 输入：Business_Logic.md（参考）

{business_logic}

## API风格
{api_style}

## 输出要求

请生成完整的 API_Contract.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 04_Data_Model.md, 02_Business_Logic.md
- 文档状态: 草案/已批准
- API版本: v1

### 2. API设计规范
- API风格（RESTful/GraphQL/gRPC）
- 基础URL格式
- 认证方式
- 请求/响应格式标准
- 字符编码: UTF-8

### 3. 接口清单总览
提供所有接口的汇总表：

| 接口ID | 方法 | 路径 | 功能描述 | 关联业务步骤 |
|--------|------|------|----------|--------------|
| API-001 | POST | /api/v1/users | 创建用户 | BL-001 |
| API-002 | GET | /api/v1/users/{{id}} | 获取用户详情 | BL-002 |

### 4. 详细接口定义
为每个接口提供详细定义：

#### 4.1 接口基本信息
**接口ID**: API-001
**接口名称**: 创建用户
**请求方法**: POST
**请求路径**: /api/v1/users
**功能描述**: 创建新用户账号
**关联业务**: BL-001 用户注册流程
**权限要求**: 公开 / 需认证 / 需特定角色

#### 4.2 请求参数
**Path参数**: 无

**Query参数**: 无

**Header参数**:
| 参数名 | 必填 | 类型 | 说明 |
|--------|------|------|------|
| Content-Type | 是 | string | application/json |
| Authorization | 否 | string | Bearer {{token}} |

**Body参数**:
| 参数名 | 必填 | 类型 | 约束 | 说明 |
|--------|------|------|------|------|
| username | 是 | string | 3-50字符 | 用户名 |
| email | 是 | string | 邮箱格式 | 邮箱地址 |
| password | 是 | string | 8-32字符 | 密码 |

**请求示例**:
```json
{{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}}
```

#### 4.3 响应定义
**成功响应 (200 OK)**:
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 用户ID |
| username | string | 用户名 |
| email | string | 邮箱 |
| created_at | string | 创建时间(ISO8601) |

**成功响应示例**:
```json
{{
  "code": 200,
  "message": "success",
  "data": {{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  }}
}}
```

**错误响应**:
| 状态码 | 错误码 | 说明 |
|--------|--------|------|
| 400 | INVALID_PARAMS | 参数校验失败 |
| 409 | USER_EXISTS | 用户已存在 |

**错误响应示例**:
```json
{{
  "code": 400,
  "message": "参数校验失败",
  "errors": [
    {{
      "field": "email",
      "message": "邮箱格式不正确"
    }}
  ]
}}
```

### 5. 错误码定义
全局错误码表：

| 错误码 | HTTP状态码 | 错误信息 | 说明 |
|--------|-----------|----------|------|
| SUCCESS | 200 | 成功 | 请求成功 |
| INVALID_PARAMS | 400 | 参数错误 | 请求参数校验失败 |
| UNAUTHORIZED | 401 | 未授权 | 缺少认证信息 |
| FORBIDDEN | 403 | 禁止访问 | 权限不足 |
| NOT_FOUND | 404 | 资源不存在 | 请求的资源不存在 |
| INTERNAL_ERROR | 500 | 服务器内部错误 | 系统异常 |

业务错误码表：
| 错误码 | HTTP状态码 | 错误信息 | 说明 |
|--------|-----------|----------|------|
| USER_EXISTS | 409 | 用户已存在 | 用户名或邮箱已注册 |
| USER_NOT_FOUND | 404 | 用户不存在 | 用户ID无效 |

### 6. 认证与授权
- 认证方式说明（JWT/OAuth2/Session）
- Token获取接口
- Token刷新机制
- 权限范围定义

### 7. 分页与过滤规范
- 分页参数标准
- 排序参数标准
- 过滤条件格式
- 示例

### 8. 限流与配额
- 限流策略
- 配额限制
- 限流响应头

### 9. API版本管理
- 版本策略
- 兼容性保证
- 弃用流程

### 10. 一致性检查点
- 与数据模型字段的对应关系
- 与业务逻辑的映射关系
- 字段命名一致性检查

## 格式要求
- 使用标准Markdown格式
- 使用表格展示参数定义
- 使用代码块展示JSON示例
- 确保请求/响应字段与Data_Model.md中的字段名完全一致
- **前后端解耦的关键文档，必须详细准确**

请直接输出Markdown格式的文档内容：
"""

def show_api_contract():
    """显示接口契约界面"""
    st.title("🔌 05. 接口契约 (API_Contract.md)")
    st.markdown("---")
    
    st.info("""
    **前后端解耦的关键。**
    
    **输入**: Data_Model.md
    **输出**: 详细的API端点、输入输出JSON示例、错误码定义
    
    **逻辑**: 拿到这个MD后，Trae可以同时生成前后端代码
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取数据模型文档
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Data_Model.md**")
        dm_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="dm_input",
            horizontal=True
        )
        
        if dm_input_method == "从当前会话获取":
            if st.session_state.data_model:
                data_model = st.session_state.data_model
                with st.expander("查看已加载内容"):
                    st.markdown(data_model[:1500] + "..." if len(data_model) > 1500 else data_model)
            else:
                st.warning("当前会话没有Data_Model.md")
                data_model = ""
        else:
            data_model = st.text_area(
                "粘贴Data_Model.md",
                placeholder="请粘贴04_Data_Model.md的完整内容...",
                height=150,
                key="dm_paste"
            )
    
    with col2:
        st.markdown("**Business_Logic.md (参考)**")
        bl_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴", "跳过"],
            key="bl_input_api",
            horizontal=True
        )
        
        if bl_input_method == "跳过":
            business_logic = "参考业务逻辑文档"
        elif bl_input_method == "从当前会话获取":
            if st.session_state.business_logic:
                business_logic = st.session_state.business_logic
                with st.expander("查看已加载内容"):
                    st.markdown(business_logic[:1000] + "..." if len(business_logic) > 1000 else business_logic)
            else:
                st.warning("当前会话没有Business_Logic.md")
                business_logic = ""
        else:
            business_logic = st.text_area(
                "粘贴Business_Logic.md",
                placeholder="请粘贴02_Business_Logic.md内容...",
                height=150,
                key="bl_paste_api"
            )
    
    # API风格选择
    st.subheader("🔧 API配置")
    col1, col2 = st.columns(2)
    with col1:
        api_style = st.selectbox(
            "API风格",
            ["RESTful", "GraphQL", "gRPC", "RESTful + GraphQL"],
            help="选择API设计风格"
        )
    with col2:
        auth_type = st.selectbox(
            "认证方式",
            ["JWT", "OAuth2", "Session", "API Key", "无认证"],
            help="选择认证机制"
        )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成接口契约文档", type="primary", use_container_width=True):
        if not data_model:
            st.error("请提供Data_Model.md内容！")
            return
        
        with st.spinner("正在生成接口契约文档，请稍候..."):
            prompt = generate_api_contract_prompt(data_model, business_logic, api_style)
            content, error = LLMClient.generate_text(prompt, temperature=0.3)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.api_contract = content
            st.success("✅ 接口契约文档生成完成！")
    
    # 显示结果
    if st.session_state.api_contract:
        display_result(st.session_state.api_contract, "05_API_Contract.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### RESTful API设计原则
        
        1. **资源导向**: URL表示资源，而非动作
           - ✅ `/users` (用户资源)
           - ❌ `/getUsers` (动作)
        
        2. **HTTP方法语义**:
           - GET: 读取资源
           - POST: 创建资源
           - PUT: 完整更新
           - PATCH: 部分更新
           - DELETE: 删除资源
        
        3. **状态码规范**:
           - 2xx: 成功
           - 3xx: 重定向
           - 4xx: 客户端错误
           - 5xx: 服务器错误
        
        ### 响应格式标准
        
        **统一响应结构**:
        ```json
        {
          "code": 200,
          "message": "success",
          "data": { ... },
          "timestamp": "2024-01-15T10:30:00Z"
        }
        ```
        
        ### 字段命名一致性
        
        **必须与Data_Model.md保持一致**:
        - Data_Model: `user_id` → API: `user_id`
        - Data_Model: `created_at` → API: `created_at`
        
        ### 安全性考虑
        
        1. **敏感信息**: 不在URL中传递敏感数据
        2. **密码处理**: 永远不在响应中返回密码
        3. **HTTPS**: 生产环境强制使用HTTPS
        4. **输入验证**: 所有输入参数必须校验
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **UI/UX组件规范** 文档
        """)

