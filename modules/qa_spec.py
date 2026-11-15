import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from utils import display_result

def generate_qa_spec_prompt(requirement_spec, api_contract):
    """生成测试规范提示词"""
    return f"""请作为资深QA工程师，基于以下需求规格和接口契约，生成测试用例与验收准则文档 (QA_Spec.md)。

## 输入：Requirement_Spec.md

{requirement_spec}

## 输入：API_Contract.md

{api_contract}

## 输出要求

请生成完整的 QA_Spec.md 文档，包含以下章节：

### 1. 文档信息
- 文档版本: v1.0
- 依赖文档: 01_Requirement_Spec.md, 05_API_Contract.md
- 文档状态: 草案/已批准
- 测试策略概述

### 2. 测试策略
#### 2.1 测试层级
| 测试类型 | 目标 | 工具 | 覆盖率目标 |
|----------|------|------|-----------|
| 单元测试 | 函数/组件级别 | Jest/Pytest | 80%+ |
| 集成测试 | 模块间交互 | 同单元测试 | 60%+ |
| E2E测试 | 完整业务流程 | Cypress/Playwright | 核心流程 |
| 性能测试 | 响应时间/并发 | k6/Artillery | 关键接口 |

#### 2.2 测试环境
- 开发环境
- 测试环境
- 预发布环境
- 生产环境（冒烟测试）

#### 2.3 测试数据策略
- 数据准备方式
- 数据清理策略
- Mock数据管理

### 3. 单元测试规范

#### 3.1 测试命名规范
```
[被测对象]_[场景]_[预期结果]

示例：
- userService_createUser_validInput_returnsUser
- authController_login_invalidPassword_throwsError
```

#### 3.2 测试结构模板
```typescript
// AAA模式
describe('UserService', () => {{
  describe('createUser', () => {{
    // Arrange
    beforeEach(() => {{
      // 准备测试数据
    }});
    
    it('should create user with valid input', () => {{
      // Act
      const result = userService.createUser(validInput);
      
      // Assert
      expect(result).toBeDefined();
      expect(result.id).toBeTruthy();
    }});
  }});
}});
```

#### 3.3 核心功能单元测试用例
为每个核心功能提供测试用例：

**功能**: 用户注册
**测试文件**: `user.service.test.ts`

| 用例ID | 用例名称 | 前置条件 | 输入 | 预期结果 | 优先级 |
|--------|----------|----------|------|----------|--------|
| UT-001 | 有效输入创建用户 | 数据库连接正常 | 有效用户信息 | 返回新用户对象 | P0 |
| UT-002 | 重复邮箱拒绝 | 用户已存在 | 相同邮箱 | 抛出UserExistsError | P0 |
| UT-003 | 无效邮箱格式 | - | 无效邮箱 | 抛出ValidationError | P1 |

### 4. 集成测试规范

#### 4.1 API集成测试
**测试范围**: 控制器 → 服务 → 数据库

| 用例ID | 接口 | 场景 | 请求 | 预期响应 | 数据库状态 |
|--------|------|------|------|----------|-----------|
| IT-001 | POST /users | 创建用户成功 | 有效JSON | 201 + 用户数据 | 用户表新增记录 |
| IT-002 | POST /users | 重复创建 | 已存在用户 | 409 + 错误信息 | 无变化 |
| IT-003 | GET /users/:id | 查询存在用户 | 有效ID | 200 + 用户数据 | - |
| IT-004 | GET /users/:id | 查询不存在用户 | 无效ID | 404 + 错误信息 | - |

#### 4.2 数据库集成测试
- 连接池测试
- 事务回滚测试
- 并发访问测试

### 5. E2E测试规范

#### 5.1 用户旅程测试
**旅程**: 用户注册 → 登录 → 使用核心功能

| 步骤 | 操作 | 预期结果 | 断言点 |
|------|------|----------|--------|
| 1 | 访问注册页面 | 显示注册表单 | URL正确 |
| 2 | 填写有效信息 | 输入框正常 | 无错误提示 |
| 3 | 点击注册 | 跳转到登录页 | 显示成功提示 |
| 4 | 登录 | 进入仪表盘 | 显示用户信息 |

#### 5.2 关键业务流程测试
列出所有关键业务流程的E2E测试：

**流程**: 订单创建流程
**用例ID**: E2E-001
**前置条件**: 用户已登录

| 步骤 | 页面 | 操作 | 预期结果 |
|------|------|------|----------|
| 1 | 商品列表 | 选择商品 | 商品加入购物车 |
| 2 | 购物车 | 点击结算 | 进入订单确认页 |
| 3 | 订单确认 | 确认信息 | 生成订单 |
| 4 | 订单详情 | 查看订单 | 显示正确订单信息 |

### 6. 性能测试规范

#### 6.1 性能指标
| 指标 | 目标值 | 警告值 | 严重值 |
|------|--------|--------|--------|
| API响应时间(P95) | < 200ms | 200-500ms | > 500ms |
| 页面加载时间 | < 2s | 2-5s | > 5s |
| 并发用户数 | 1000 | 500 | < 100 |
| 错误率 | < 0.1% | 0.1-1% | > 1% |

#### 6.2 性能测试场景
| 场景ID | 场景描述 | 并发数 | 持续时间 | 目标 |
|--------|----------|--------|----------|------|
| PERF-001 | 登录接口压力测试 | 100 | 5分钟 | 响应时间<200ms |
| PERF-002 | 首页加载测试 | 50 | 10分钟 | 加载时间<2s |

### 7. 安全测试规范

#### 7.1 认证授权测试
| 用例ID | 测试项 | 测试方法 | 预期结果 |
|--------|--------|----------|----------|
| SEC-001 | 未授权访问 | 不带Token访问受保护接口 | 返回401 |
| SEC-002 | 无效Token | 使用过期Token | 返回401 |
| SEC-003 | 权限控制 | 低权限用户访问高权限接口 | 返回403 |

#### 7.2 输入验证测试
| 用例ID | 测试项 | 输入 | 预期结果 |
|--------|--------|------|----------|
| SEC-004 | SQL注入 | `' OR '1'='1` | 被过滤/转义 |
| SEC-005 | XSS攻击 | `<script>alert('xss')</script>` | 被转义 |
| SEC-006 | 超长输入 | 10000字符 | 被截断/拒绝 |

### 8. 兼容性测试

#### 8.1 浏览器兼容性
| 浏览器 | 版本 | 优先级 |
|--------|------|--------|
| Chrome | 最新2个版本 | P0 |
| Firefox | 最新2个版本 | P0 |
| Safari | 最新2个版本 | P1 |
| Edge | 最新2个版本 | P1 |

#### 8.2 设备兼容性
| 设备类型 | 分辨率 | 优先级 |
|----------|--------|--------|
| 桌面 | 1920x1080 | P0 |
| 笔记本 | 1366x768 | P0 |
| 平板 | 768x1024 | P1 |
| 手机 | 375x667 | P1 |

### 9. 验收准则

#### 9.1 功能验收
- [ ] 所有P0功能正常
- [ ] 所有P1功能正常
- [ ] 单元测试覆盖率>80%
- [ ] 集成测试通过率100%
- [ ] E2E测试通过率100%

#### 9.2 性能验收
- [ ] API响应时间达标
- [ ] 页面加载时间达标
- [ ] 并发用户数达标
- [ ] 内存使用稳定

#### 9.3 安全验收
- [ ] 通过安全测试
- [ ] 无高危漏洞
- [ ] 敏感数据加密
- [ ] 审计日志完整

### 10. Bug分级标准

| 级别 | 定义 | 响应时间 | 修复时间 |
|------|------|----------|----------|
| P0-致命 | 系统崩溃/数据丢失 | 立即 | 4小时 |
| P1-严重 | 核心功能不可用 | 2小时 | 24小时 |
| P2-一般 | 非核心功能异常 | 24小时 | 3天 |
| P3-轻微 | UI/UX问题 | 3天 | 1周 |

### 11. 测试报告模板
提供测试报告的标准模板：
- 测试概览
- 测试执行情况
- 缺陷统计
- 风险评估
- 发布建议

## 格式要求
- 使用标准Markdown格式
- 使用表格展示测试用例
- 使用代码块展示测试代码模板
- **开发完成后，Trae依据此文件运行测试，闭环验证**

请直接输出Markdown格式的文档内容：
"""

def show_qa_spec():
    """显示测试规范界面"""
    st.title("🧪 08. 测试用例与验收准则 (QA_Spec.md)")
    st.markdown("---")
    
    st.info("""
    **开发完成后，Trae依据此文件运行测试，闭环验证。**
    
    **输入**: Requirement_Spec.md + API_Contract.md
    **输出**: 单元测试逻辑、集成测试路径
    """)
    
    # 输入区域
    st.subheader("📝 输入信息")
    
    # 获取文档
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Requirement_Spec.md**")
        req_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="req_input_qa",
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
                key="req_paste_qa"
            )
    
    with col2:
        st.markdown("**API_Contract.md**")
        api_input_method = st.radio(
            "选择输入方式",
            ["从当前会话获取", "手动粘贴"],
            key="api_input_qa",
            horizontal=True
        )
        
        if api_input_method == "从当前会话获取":
            if st.session_state.api_contract:
                api_contract = st.session_state.api_contract
                with st.expander("查看已加载内容"):
                    st.markdown(api_contract[:1500] + "..." if len(api_contract) > 1500 else api_contract)
            else:
                st.warning("当前会话没有API_Contract.md")
                api_contract = ""
        else:
            api_contract = st.text_area(
                "粘贴API_Contract.md",
                placeholder="请粘贴05_API_Contract.md的完整内容...",
                height=150,
                key="api_paste_qa"
            )
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🚀 生成测试规范", type="primary", use_container_width=True):
        if not requirement_spec or not api_contract:
            st.error("请提供Requirement_Spec.md和API_Contract.md内容！")
            return
        
        with st.spinner("正在生成测试规范，请稍候..."):
            prompt = generate_qa_spec_prompt(requirement_spec, api_contract)
            content, error = LLMClient.generate_text(prompt, temperature=0.4)
            
            if error:
                st.error(f"生成失败: {error}")
                return
            
            st.session_state.qa_spec = content
            st.success("✅ 测试规范生成完成！")
    
    # 显示结果
    if st.session_state.qa_spec:
        display_result(st.session_state.qa_spec, "08_QA_Spec.md")
    
    # 使用指南
    with st.expander("📖 使用指南"):
        st.markdown("""
        ### 测试金字塔
        
        ```
            /\\
           /  \\
          / E2E\\      <- 少量，关键流程
         /--------\\
        / Integration\\  <- 中等，模块交互
       /--------------\\
      /    Unit Tests   \\n     /___________________\\ <- 大量，核心逻辑
        ```
        
        ### 测试优先级
        
        | 优先级 | 含义 | 处理策略 |
        |--------|------|----------|
        | P0 | 必须测试 | 所有场景必须覆盖 |
        | P1 | 应该测试 | 核心场景必须覆盖 |
        | P2 | 可以测试 | 时间允许时覆盖 |
        
        ### AAA测试模式
        
        ```typescript
        // Arrange - 准备
        const input = {{ username: 'test' }};
        
        // Act - 执行
        const result = service.create(input);
        
        // Assert - 断言
        expect(result.username).toBe('test');
        ```
        
        ### 给Trae的测试指令
        
        开发完成后，给Trae以下指令：
        ```
        请根据08_QA_Spec.md编写并执行测试：
        1. 实现所有单元测试（P0/P1优先）
        2. 实现API集成测试
        3. 执行测试并修复失败项
        4. 生成测试报告
        ```
        
        ### 验收检查清单
        
        发布前必须检查：
        - [ ] 单元测试通过率 > 90%
        - [ ] 核心功能E2E测试通过
        - [ ] 无P0/P1级Bug
        - [ ] 性能指标达标
        - [ ] 安全测试通过
        
        ### 下一步
        
        生成完成后，您可以：
        1. 复制内容到剪贴板
        2. 下载为 .md 文件
        3. 继续生成 **软件用户手册** 文档
        """)

