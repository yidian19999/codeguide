import streamlit as st
import sys
sys.path.append('..')
from llm_client import LLMClient
from PIL import Image
import requests
from io import BytesIO
import re
import json

def extract_screenshot_markers(manual_content):
    """从软著手册中提取截图标记"""
    if not manual_content:
        return []
    
    # 匹配 [Insert Screenshot: Description] 或 [Insert Screenshot:Description] 格式
    pattern = r'\[Insert Screenshot:\s*([^\]]+)\]'
    matches = re.findall(pattern, manual_content, re.IGNORECASE)
    
    screenshots = []
    for i, desc in enumerate(matches, 1):
        screenshots.append({
            "id": f"SC-{i:03d}",
            "description": desc.strip(),
            "section": extract_section_context(manual_content, desc),
            "generated": False,
            "image_url": None,
            "local_path": None
        })
    
    return screenshots

def extract_section_context(content, marker_desc):
    """提取截图标记所在的章节上下文"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if marker_desc in line:
            # 向上查找最近的章节标题
            for j in range(i-1, -1, -1):
                if lines[j].startswith('## ') or lines[j].startswith('### '):
                    return lines[j].strip('# ').strip()
    return "未分类"

def analyze_docs_for_screenshots(tech_stack, api_contract, ui_component, manual):
    """综合分析文档，生成截图建议"""
    suggestions = []
    
    # 1. 从手册中提取已有的截图标记
    manual_screenshots = extract_screenshot_markers(manual)
    
    # 2. 从UI组件文档中提取页面信息
    pages = extract_pages_from_ui_component(ui_component)
    
    # 3. 从API文档中提取关键接口
    api_endpoints = extract_key_apis(api_contract)
    
    # 4. 从技术栈文档中提取UI框架信息
    ui_framework = extract_ui_framework(tech_stack)
    
    # 合并建议
    if manual_screenshots:
        suggestions.extend([{
            "source": "手册标记",
            "id": s["id"],
            "name": s["description"],
            "section": s["section"],
            "priority": "高",
            "context": {
                "ui_framework": ui_framework,
                "pages": pages,
                "apis": api_endpoints
            }
        } for s in manual_screenshots])
    
    # 如果没有手册标记，基于页面路由生成建议
    if not suggestions and pages:
        for i, page in enumerate(pages[:10], 1):  # 最多10个页面
            suggestions.append({
                "source": "页面分析",
                "id": f"SC-{i:03d}",
                "name": f"{page['name']}界面",
                "section": page.get('route', '主要功能'),
                "priority": "高" if i <= 5 else "中",
                "context": {
                    "ui_framework": ui_framework,
                    "page_info": page,
                    "apis": api_endpoints
                }
            })
    
    return suggestions

def extract_pages_from_ui_component(ui_content):
    """从UI组件文档中提取页面信息"""
    pages = []
    if not ui_content:
        return pages
    
    # 尝试提取路由表
    route_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    matches = re.findall(route_pattern, ui_content)
    
    for match in matches:
        if len(match) >= 3 and '路径' not in match[0]:
            pages.append({
                'route': match[0].strip(),
                'name': match[1].strip(),
                'description': match[2].strip()
            })
    
    return pages

def extract_key_apis(api_content):
    """从API契约文档中提取关键接口"""
    apis = []
    if not api_content:
        return apis
    
    # 提取接口路径
    api_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+([^\s]+)'
    matches = re.findall(api_pattern, api_content)
    
    for method, path in matches[:10]:  # 最多10个接口
        apis.append({
            'method': method,
            'path': path
        })
    
    return apis

def extract_ui_framework(tech_content):
    """从技术栈文档中提取UI框架信息"""
    if not tech_content:
        return {"framework": "React", "ui_lib": "Tailwind CSS"}
    
    frameworks = []
    ui_libs = []
    
    # 检测前端框架
    if 'react' in tech_content.lower():
        frameworks.append('React')
    if 'vue' in tech_content.lower():
        frameworks.append('Vue')
    if 'angular' in tech_content.lower():
        frameworks.append('Angular')
    
    # 检测UI库
    if 'tailwind' in tech_content.lower():
        ui_libs.append('Tailwind CSS')
    if 'element plus' in tech_content.lower() or 'element' in tech_content.lower():
        ui_libs.append('Element Plus')
    if 'antd' in tech_content.lower() or 'ant design' in tech_content.lower():
        ui_libs.append('Ant Design')
    if 'bootstrap' in tech_content.lower():
        ui_libs.append('Bootstrap')
    
    return {
        "framework": frameworks[0] if frameworks else "React",
        "ui_lib": ui_libs[0] if ui_libs else "Tailwind CSS"
    }

def generate_screenshot_prompt_v2(suggestion, all_docs):
    """生成截图提示词（增强版）"""
    ui_framework = suggestion.get('context', {}).get('ui_framework', {})
    page_info = suggestion.get('context', {}).get('page_info', {})
    
    framework = ui_framework.get('framework', 'React')
    ui_lib = ui_framework.get('ui_lib', 'Tailwind CSS')
    
    screenshot_name = suggestion['name']
    section = suggestion.get('section', '')
    
    # 构建提示词
    prompt = f"""请生成一张专业的软件界面截图，用于软著申请文档。

## 界面信息

**界面名称**: {screenshot_name}
**所属模块**: {section}
**前端技术**: {framework} + {ui_lib}

## 设计要求

### 1. 整体风格
- 采用现代、专业的商务风格
- 使用清晰的视觉层次
- 配色协调，以蓝色系为主（#1890ff 或类似专业蓝色）
- 白色背景，灰色边框分隔

### 2. 布局结构
- 顶部：导航栏（包含Logo、菜单、用户信息）
- 左侧：侧边栏菜单（如适用）
- 主内容区：展示核心业务数据和操作
- 底部：页脚或状态栏（可选）

### 3. 界面元素要求
- 使用真实的中文业务数据（不要出现"test"、"demo"等字样）
- 表格数据完整，包含表头和至少3-5行数据
- 按钮状态清晰（主按钮、次按钮区分）
- 表单元素对齐整齐
- 图标简洁明了

### 4. 数据示例（参考）
- 用户名：使用真实中文姓名（如：张明、李华）
- 订单号：使用真实格式（如：DD20240115001）
- 金额：使用千分位格式（如：¥12,345.67）
- 日期：使用标准格式（如：2024-01-15 14:30）
- 状态：使用业务状态（如：已完成、处理中、待审核）

### 5. 专业细节
- 显示当前登录用户信息（头像+姓名）
- 显示系统时间
- 面包屑导航显示当前位置
- 操作按钮有明确的文字说明
- 数据加载状态或分页组件（如适用）

### 6. 截图规格
- 分辨率：1920x1080 或 1440x900
- 比例：16:9
- 清晰度高，文字可读
- 无水印、无Mock字样

## 输出要求

请生成一张高质量的PNG格式界面截图，确保：
1. 界面布局合理，符合{framework} + {ui_lib}的设计规范
2. 数据真实可信，适合软著申请材料
3. 视觉效果专业美观
4. 所有文字清晰可读
"""
    
    return prompt

def test_image_api_connection():
    """测试图像生成API连接"""
    from config import get_image_api_config
    import openai
    
    config = get_image_api_config()
    if not config.get("api_key"):
        return False, "API Key未配置", ""
    
    try:
        client = openai.OpenAI(
            base_url=config.get("base_url", "https://api.openai.com/v1"),
            api_key=config["api_key"]
        )
        
        # 尝试一个简单的请求来测试连接
        # 使用最小的prompt进行测试
        test_prompt = "A simple blue square icon"
        
        response = client.images.generate(
            model=config.get("model", "dall-e-3"),
            prompt=test_prompt,
            size="2048x2048",
            quality="standard",
            n=1
        )
        
        return True, "连接成功", ""
    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        return False, f"连接失败: {str(e)}", full_error

def generate_single_screenshot_v2(suggestion, all_docs, regenerate=False):
    """生成单个截图（新版）"""
    from config import get_image_api_config
    
    # 获取配置信息用于调试
    config = get_image_api_config()
    base_url = config.get("base_url", "未配置")
    model = config.get("model", "未配置")
    
    prompt = generate_screenshot_prompt_v2(suggestion, all_docs)
    
    print(f"[DEBUG] 正在生成截图: {suggestion['name']}")
    print(f"[DEBUG] API配置: base_url={base_url}, model={model}")
    print(f"[DEBUG] 提示词长度: {len(prompt)} 字符")
    
    # 调用图像生成API
    # 豆包API要求最小 3686400 像素，使用 1920x1080 = 2073600 像素不满足
    # 需要使用更大的尺寸，如 2048x2048 = 4194304 像素
    image_url, error = LLMClient.generate_image(
        prompt, 
        size="2048x2048",  # 豆包API要求最小3686400像素
        quality="standard"
    )
    
    if error:
        # 添加更详细的错误信息
        detailed_error = f"API配置:\n"
        detailed_error += f"- Base URL: {base_url}\n"
        detailed_error += f"- Model: {model}\n\n"
        detailed_error += f"错误信息:\n{error}\n\n"
        detailed_error += "可能的原因:\n"
        detailed_error += "1. API Key未配置或错误 - 请检查系统设置中的图像生成API配置\n"
        detailed_error += "2. API不支持图像生成 - 请确认您的API提供商支持图像生成功能\n"
        detailed_error += "3. 模型名称错误 - 请检查模型名称是否正确（如 dall-e-3, gpt-4o 等）\n"
        detailed_error += "4. 网络连接问题 - 请检查网络连接\n"
        detailed_error += "5. API余额不足 - 请检查账户余额\n"
        detailed_error += "6. 提示词过长 - 尝试缩短描述"
        return None, detailed_error
    
    print(f"[DEBUG] 截图生成成功: {suggestion['name']}, URL: {image_url[:50]}...")
    return image_url, None

def show_ui_screenshot_generator():
    """显示UI截图生成界面（重构版）"""
    st.title("🔟 软著UI截图生成")
    st.markdown("---")
    
    st.info("""
    **智能分析文档，自动生成软著所需界面截图**
    
    **工作流程**:
    1. 读取 03/05/06/09 文档
    2. 分析并推荐需要生成的截图列表
    3. 批量生成高质量JPG截图
    4. 支持不满意重新生成（抽卡）
    """)
    
    # 初始化日志存储
    if "generation_logs" not in st.session_state:
        st.session_state.generation_logs = []
    
    # 检查API配置
    from config import get_image_api_config
    img_config = get_image_api_config()
    
    with st.expander("⚙️ API配置检查（点击展开）", expanded=not img_config.get("api_key")):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**图像生成API配置**")
            if img_config.get("api_key"):
                st.success("✅ API Key 已配置")
                st.text(f"Base URL: {img_config.get('base_url', '默认')}")
                st.text(f"Model: {img_config.get('model', 'dall-e-3')}")
                
                # 测试连接按钮
                if st.button("🧪 测试API连接", key="test_api_btn"):
                    with st.spinner("正在测试连接..."):
                        success, msg, full_error = test_image_api_connection()
                        if success:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
                            if full_error:
                                with st.expander("查看详细错误日志"):
                                    st.code(full_error, language=None)
            else:
                st.error("❌ API Key 未配置")
                st.warning("请先到「系统设置」中配置图像生成API")
        with col2:
            st.markdown("**支持的模型**")
            st.markdown("""
            - `dall-e-3` (OpenAI官方)
            - `gpt-4o` (部分API提供商)
            - `dall-e-2` (OpenAI官方)
            - `doubao-seedream-*` (豆包/火山引擎)
            """)
            
            st.markdown("**图片尺寸说明**")
            st.info("""
            当前使用 2048x2048 像素
            
            豆包API要求最小 3686400 像素
            (约 1920x1920)
            """)
    
    # 步骤1：文档输入
    st.header("📄 步骤1：选择输入文档")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**从当前会话获取文档**")
        
        # 检查可用文档
        docs_available = {
            "03_Tech_Stack.md": st.session_state.get("tech_stack", ""),
            "05_API_Contract.md": st.session_state.get("api_contract", ""),
            "06_UI_Component.md": st.session_state.get("ui_component", ""),
            "09_Software_Copyright_Manual.md": st.session_state.get("software_copyright_manual", ""),
        }
        
        for doc_name, content in docs_available.items():
            if content:
                st.success(f"✅ {doc_name}")
            else:
                st.warning(f"⚠️ {doc_name} (未生成)")
    
    with col2:
        st.markdown("**或手动粘贴09文档（优先）**")
        manual_input = st.text_area(
            "粘贴Software_Copyright_Manual.md内容",
            placeholder="粘贴完整的用户手册内容，系统将自动提取[Insert Screenshot]标记...",
            height=150
        )
    
    # 使用手动输入或会话中的文档
    tech_stack = docs_available["03_Tech_Stack.md"]
    api_contract = docs_available["05_API_Contract.md"]
    ui_component = docs_available["06_UI_Component.md"]
    manual = manual_input if manual_input else docs_available["09_Software_Copyright_Manual.md"]
    
    st.markdown("---")
    
    # 步骤2：分析并推荐截图列表
    st.header("📋 步骤2：截图列表推荐")
    
    if st.button("🔍 分析文档并生成截图列表", type="primary", use_container_width=True):
        if not manual:
            st.error("请提供Software_Copyright_Manual.md内容！")
            return
        
        with st.spinner("正在分析文档..."):
            suggestions = analyze_docs_for_screenshots(
                tech_stack, api_contract, ui_component, manual
            )
            
            if not suggestions:
                st.warning("未检测到截图标记，请检查手册内容格式")
                return
            
            st.session_state.screenshot_suggestions = suggestions
            st.success(f"✅ 分析完成，推荐生成 {len(suggestions)} 张截图")
    
    # 显示截图列表
    if st.session_state.get("screenshot_suggestions"):
        suggestions = st.session_state.screenshot_suggestions
        
        st.markdown(f"**共推荐 {len(suggestions)} 张截图**")
        
        # 初始化生成状态
        if "generated_screenshots" not in st.session_state:
            st.session_state.generated_screenshots = {}
        
        # 显示截图列表表格
        data = []
        for s in suggestions:
            gen_status = "✅ 已生成" if s['id'] in st.session_state.generated_screenshots else "⬜ 待生成"
            data.append({
                "序号": s['id'],
                "截图名称": s['name'],
                "所属章节": s['section'],
                "优先级": s['priority'],
                "状态": gen_status
            })
        
        st.dataframe(data, use_container_width=True, hide_index=True)
        
        # 选择要生成的截图
        st.markdown("**选择要生成的截图**")
        
        selected_ids = []
        cols = st.columns(3)
        for i, s in enumerate(suggestions):
            with cols[i % 3]:
                is_generated = s['id'] in st.session_state.generated_screenshots
                checkbox_label = f"{s['id']}: {s['name']}"
                if is_generated:
                    checkbox_label += " ✅"
                
                if st.checkbox(checkbox_label, key=f"select_{s['id']}", value=not is_generated):
                    selected_ids.append(s['id'])
        
        st.markdown("---")
        
        # 步骤3：批量生成
        st.header("🎨 步骤3：批量生成截图")
        
        # 检查API配置
        from config import get_image_api_config
        img_config = get_image_api_config()
        api_ready = bool(img_config.get("api_key"))
        
        if not api_ready:
            st.error("⚠️ 图像生成API未配置，无法生成截图。请先到「系统设置」中配置API。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 开始批量生成", type="primary", use_container_width=True, disabled=not api_ready):
                if not selected_ids:
                    st.error("请至少选择一张截图！")
                    return
                
                all_docs = {
                    "tech_stack": tech_stack,
                    "api_contract": api_contract,
                    "ui_component": ui_component,
                    "manual": manual
                }
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 清空之前的日志
                st.session_state.generation_logs = []
                
                for i, sid in enumerate(selected_ids):
                    suggestion = next(s for s in suggestions if s['id'] == sid)
                    status_text.text(f"正在生成: {suggestion['name']}... ({i+1}/{len(selected_ids)})")
                    
                    # 记录开始生成日志
                    log_entry = f"[{i+1}/{len(selected_ids)}] 开始生成: {suggestion['name']}"
                    st.session_state.generation_logs.append(log_entry)
                    
                    image_url, error = generate_single_screenshot_v2(suggestion, all_docs)
                    
                    if error:
                        error_log = f"❌ {suggestion['name']} 失败"
                        st.session_state.generation_logs.append(error_log)
                        # 保存错误信息到session_state以便rerun后显示
                        if "generation_errors" not in st.session_state:
                            st.session_state.generation_errors = {}
                        st.session_state.generation_errors[sid] = {
                            "name": suggestion['name'],
                            "error": error
                        }
                    else:
                        success_log = f"✅ {suggestion['name']} 生成成功"
                        st.session_state.generation_logs.append(success_log)
                        st.session_state.generated_screenshots[sid] = {
                            **suggestion,
                            "image_url": image_url,
                            "timestamp": st.session_state.get("timestamp", "")
                        }
                        # 清除该截图之前的错误记录
                        if "generation_errors" in st.session_state and sid in st.session_state.generation_errors:
                            del st.session_state.generation_errors[sid]
                    
                    progress_bar.progress((i + 1) / len(selected_ids))
                
                status_text.text("批量生成完成！")
                st.success("✅ 批量生成完成！")
                
                # 显示日志
                with st.expander("📋 查看生成日志", expanded=True):
                    st.code("\n".join(st.session_state.generation_logs), language=None)
                
                st.rerun()
        
        with col2:
            if st.button("🔄 重新生成选中项", use_container_width=True):
                if not selected_ids:
                    st.error("请至少选择一张截图！")
                    return
                
                # 清除选中项的生成记录
                for sid in selected_ids:
                    if sid in st.session_state.generated_screenshots:
                        del st.session_state.generated_screenshots[sid]
                
                st.success("已重置选中项，请重新点击生成")
                st.rerun()
    
    st.markdown("---")
    
    # 显示生成错误（如果有）
    if st.session_state.get("generation_errors"):
        st.header("❌ 生成错误详情")
        st.error(f"共有 {len(st.session_state.generation_errors)} 个截图生成失败")
        
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🗑️ 清除错误记录", key="clear_errors"):
                st.session_state.generation_errors = {}
                st.rerun()
        
        for sid, error_data in st.session_state.generation_errors.items():
            with st.expander(f"❌ {error_data['name']} - 点击查看错误详情", expanded=True):
                st.code(error_data['error'], language=None)
        
        st.markdown("---")
    
    # 步骤4：展示生成结果
    if st.session_state.get("generated_screenshots"):
        st.header("📸 步骤4：生成结果预览")
        
        screenshots = st.session_state.generated_screenshots
        
        for sid, data in screenshots.items():
            with st.container():
                st.markdown(f"**{data['id']}: {data['name']}**")
                st.caption(f"所属章节: {data['section']}")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if data.get('image_url'):
                        try:
                            response = requests.get(data['image_url'])
                            image = Image.open(BytesIO(response.content))
                            
                            # 转换为JPG格式
                            if image.mode in ('RGBA', 'LA', 'P'):
                                background = Image.new('RGB', image.size, (255, 255, 255))
                                if image.mode == 'P':
                                    image = image.convert('RGBA')
                                if image.mode in ('RGBA', 'LA'):
                                    background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                                    image = background
                                else:
                                    image = image.convert('RGB')
                            
                            st.image(image, use_column_width=True)
                            
                            # 保存到session用于下载
                            img_buffer = BytesIO()
                            image.save(img_buffer, format='JPEG', quality=95)
                            img_buffer.seek(0)
                            
                            st.download_button(
                                label=f"📥 下载 {data['name']}.jpg",
                                data=img_buffer,
                                file_name=f"{data['id']}_{data['name']}.jpg",
                                mime="image/jpeg",
                                key=f"download_{sid}"
                            )
                        except Exception as e:
                            st.error(f"图片加载失败: {e}")
                    else:
                        st.error("图片URL无效")
                
                with col2:
                    st.markdown("**功能描述**:")
                    st.write(data['name'])
                    
                    st.markdown("**插入位置**:")
                    st.code(f"[Insert Screenshot: {data['name']}]", language=None)
                    
                    if st.button("🎲 重新抽卡", key=f"redraw_{sid}"):
                        if sid in st.session_state.generated_screenshots:
                            del st.session_state.generated_screenshots[sid]
                        st.rerun()
                
                st.markdown("---")
        
        # 批量下载
        st.subheader("📦 批量导出")
        
        if st.button("📥 导出所有截图清单", use_container_width=True):
            # 生成截图清单文档
            manifest = "# 软著截图清单\n\n"
            manifest += "| 序号 | 截图名称 | 所属章节 | 文件名 |\n"
            manifest += "|------|----------|----------|--------|\n"
            
            for sid, data in screenshots.items():
                manifest += f"| {data['id']} | {data['name']} | {data['section']} | {data['id']}_{data['name']}.jpg |\n"
            
            st.download_button(
                label="📄 下载截图清单 (Markdown)",
                data=manifest,
                file_name="screenshot_manifest.md",
                mime="text/markdown"
            )
    
    # 使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ### 功能说明
        
        本模块智能分析您的设计文档，自动推荐需要生成的软著截图：
        
        1. **文档分析**
           - 读取 03_Tech_Stack.md 获取前端技术栈
           - 读取 05_API_Contract.md 获取接口数据示例
           - 读取 06_UI_Component.md 获取页面结构
           - 读取 09_Software_Copyright_Manual.md 获取截图标记
        
        2. **智能推荐**
           - 自动提取 `[Insert Screenshot: Description]` 标记
           - 分析页面路由补充关键界面
           - 按优先级排序推荐列表
        
        3. **批量生成**
           - 支持选择部分或全部生成
           - 生成JPG格式高清图片
           - 支持不满意重新生成（抽卡）
        
        4. **导出管理**
           - 单张下载为JPG
           - 批量导出截图清单
           - 文件名包含序号便于对应
        
        ### 截图要求
        
        - 使用真实中文业务数据
        - 不出现"test""mock"等字样
        - 界面布局清晰专业
        - 符合软著申请材料标准
        """)
