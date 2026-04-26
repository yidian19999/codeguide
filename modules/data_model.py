import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_data_model_prompt(business_logic, tech_stack, db_preference=""):
    """生成数据模型提示词"""
    return f"""请作为资深数据库架构师，基于以下业务逻辑和技术栈，生成数据架构与模型文档 (Data_Model.md)。

## 输入：Business_Logic.md

{business_logic}

## 输入：Tech_Stack.md

{tech_stack}

## 数据库偏好
{db_preference if db_preference else "根据技术栈自动选择合适的数据库类型"}

## 输出要求

请生成完整的 Data_Model.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 02_Business_Logic.md, 03_Tech_Stack.md
- 文档状态: 草案/已批准

### 2. 数据库选型
- 数据库类型（SQL/NoSQL/混合）
- 具体数据库产品（如 PostgreSQL 15, MongoDB 6.0）
- 选型理由
- 版本要求

### 3. 实体关系图 (ERD)
使用Mermaid语法提供ER图：

```mermaid
erDiagram
    ENTITY1 ||--o{{ ENTITY2 : relationship
    ENTITY1 {{
        type field1 "description"
        type field2 "description"
    }}
```

并附上文字说明每个实体的职责。

### 4. 数据库Schema定义

#### 4.1 表/集合清单
| 表名 | 类型 | 用途 | 预估数据量 |
|------|------|------|-----------|
| users | 表 | 用户数据 | 10万+ |

#### 4.2 详细字段定义（每个表）
为每个表提供详细定义：

**表名**: users
**描述**: 用户基础信息表
**引擎**: InnoDB (MySQL) / 默认 (PostgreSQL)
**字符集**: utf8mb4

| 字段名 | 数据类型 | 长度 | 是否可空 | 默认值 | 索引 | 说明 |
|--------|----------|------|----------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | PK | 主键 |
| username | VARCHAR | 50 | NO | - | UNIQUE | 用户名 |
| email | VARCHAR | 100 | NO | - | INDEX | 邮箱 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | 创建时间 |

**索引清单**:
- PRIMARY KEY (id)
- UNIQUE KEY uk_username (username)
- KEY idx_email (email)

**外键关系**:
- 无外键 / 或列出外键定义

### 5. 实体类定义
根据技术栈提供对应的实体类代码：

#### 5.1 ORM模型定义
例如 SQLAlchemy (Python):
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
```

或 Prisma (Node.js):
```prisma
model User {{
  id        BigInt   @id @default(autoincrement())
  username  String   @unique @db.VarChar(50)
}}
```

### 6. 数据校验规则

#### 6.1 字段级校验
| 字段 | 校验规则 | 错误提示 |
|------|----------|----------|
| username | 长度3-50, 字母数字下划线 | 用户名格式不正确 |
| email | 邮箱格式 | 邮箱格式不正确 |

#### 6.2 业务级校验
- 唯一性约束
- 关联性约束
- 状态转换约束

### 7. 数据字典
定义所有枚举类型和常量：

| 枚举名 | 值 | 说明 |
|--------|-----|------|
| UserStatus | ACTIVE | 正常 |
| UserStatus | INACTIVE | 未激活 |
| UserStatus | BANNED | 已封禁 |

### 8. 数据迁移策略
- 迁移工具选择
- 命名规范
- 回滚策略
- 示例迁移脚本

### 9. 数据安全与备份
- 敏感数据加密方案
- 备份策略
- 数据保留策略
- 脱敏规则

### 10. 一致性检查点
- 与业务逻辑的状态对应关系
- 与API字段的映射关系（预留）

## 格式要求
- 使用标准Markdown格式
- 使用表格展示字段定义
- 使用代码块展示SQL和ORM代码
- **字段名必须在此定死，禁止AI在后面步骤自行发挥**
- 确保所有字段都有明确的数据类型、约束和说明

请直接输出Markdown格式的文档内容：
"""

def show_data_model():
    """显示数据模型界面"""
    st.title("🗄️ 04. 数据架构与模型 (Data_Model.md)")
    st.markdown("---")
    
    st.info("""
    **后端逻辑的物理基础。**
    
    **输入**: Business_Logic.md + Tech_Stack.md
    **输出**: 数据库Schema（SQL或NoSQL）、实体类定义、数据校验规则
    
    **一致性点**: 字段名必须在此定死，禁止AI在后面步骤自行发挥
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取业务逻辑文档
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Business_Logic.md**")
        bl_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="bl_input",
            horizontal=True
        )
        
        if bl_input_method == "从当前会话获取":
            if st.session_state.business_logic:
                business_logic = st.session_state.business_logic
                with st.expander("查看已加载内容"):
                    st.markdown(business_logic[:1500] + "..." if len(business_logic) > 1500 else business_logic)
            else:
                st.warning("当前会话没有Business_Logic.md")
                business_logic = ""
        else:
            business_logic = st.text_area(
                "粘贴Business_Logic.md",
                placeholder="请粘贴02_Business_Logic.md的完整内容...",
                height=150,
                key="bl_paste"
            )
    
    with col2:
        st.markdown("**Tech_Stack.md**")
        ts_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="ts_input",
            horizontal=True
        )
        
        if ts_input_method == "从当前会话获取":
            if st.session_state.tech_stack:
                tech_stack = st.session_state.tech_stack
                with st.expander("查看已加载内容"):
                    st.markdown(tech_stack[:1500] + "..." if len(tech_stack) > 1500 else tech_stack)
            else:
                st.warning("当前会话没有Tech_Stack.md")
                tech_stack = ""
        else:
            tech_stack = st.text_area(
                "粘贴Tech_Stack.md",
                placeholder="请粘贴03_Tech_Stack.md的完整内容...",
                height=150,
                key="ts_paste"
            )
    
    # 数据库偏好
    st.subheader("🗄️ 数据库偏好（可选）")
    db_preference = st.text_input(
        "指定数据库类型",
        placeholder="例如：PostgreSQL, MySQL, MongoDB, 或混合架构",
        help="如果不指定，将根据技术栈自动选择"
    )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成数据模型文档", type="primary", use_container_width=True):
        if not business_logic or not tech_stack:
            st.error("请提供Business_Logic.md和Tech_Stack.md内容！")
            return
        
        with st.spinner("正在生成数据模型文档，请稍候..."):
            prompt = generate_data_model_prompt(business_logic, tech_stack, db_preference)
            content, error = LLMClient.generate_text(prompt, temperature=0.3)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.data_model = content
            st.success("✅ 数据模型文档生成完成！")
    
    # 显示结果
    if st.session_state.data_model:
        display_result(st.session_state.data_model, "04_Data_Model.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 字段命名规范
        
        **重要**: 本文档中定义的字段名是最终标准，后续所有文档和代码必须严格遵循：
        
        ✅ **正确示例**:
        - `user_id` (用户ID)
        - `created_at` (创建时间)
        - `order_status` (订单状态)
        
        ❌ **错误示例**:
        - `userId` (驼峰命名)
        - `create_time` (与created_at混用)
        - `status` (过于模糊)
        
        ### 数据库设计原则
        
        1. **三大范式**: 遵循数据库范式，避免数据冗余
        2. **索引策略**: 为高频查询字段建立索引
        3. **扩展性**: 预留扩展字段，考虑未来需求
        4. **安全性**: 敏感字段加密存储
        
        ### ORM选择建议
        
        | 技术栈 | 推荐ORM |
        |--------|---------|
        | Python | SQLAlchemy, Django ORM |
        | Node.js | Prisma, TypeORM, Sequelize |
        | Java | Hibernate, MyBatis |
        | Go | GORM, Ent |
        
        ### 数据校验层级
        
        1. **数据库层**: NOT NULL, UNIQUE, CHECK约束
        2. **应用层**: ORM验证、业务规则验证
        3. **API层**: 输入参数验证
        4. **前端层**: 表单即时验证
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **接口契约** 文档
        """)

