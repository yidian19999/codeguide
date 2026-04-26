import openai
from config import get_text_api_config, get_image_api_config
import traceback

class LLMClient:
    """LLM客户端，用于调用文本和图像生成API"""
    
    @staticmethod
    def generate_text(prompt, temperature=0.7, max_tokens=4000):
        """调用文本生成API"""
        config = get_text_api_config()
        if not config.get("api_key"):
            return None, "请先配置文本生成API"
        
        try:
            client = openai.OpenAI(
                base_url=config.get("base_url", "https://api.openai.com/v1"),
                api_key=config["api_key"]
            )
            
            response = client.chat.completions.create(
                model=config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "你是一个专业的软件开发专家，擅长软件架构设计、需求分析和文档编写。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content, None
        except Exception as e:
            error_msg = f"文本生成错误: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            return None, error_msg
    
    @staticmethod
    def generate_image(prompt, size="1024x1024", quality="standard"):
        """调用图像生成API"""
        config = get_image_api_config()
        if not config.get("api_key"):
            return None, "请先配置图像生成API（在系统设置中配置）"
        
        base_url = config.get("base_url", "https://api.openai.com/v1")
        api_key = config["api_key"]
        model = config.get("model", "dall-e-3")
        
        print(f"[DEBUG] 图像生成配置: base_url={base_url}, model={model}")
        
        try:
            client = openai.OpenAI(
                base_url=base_url,
                api_key=api_key
            )
            
            # 尝试使用标准的OpenAI图像生成接口
            print(f"[DEBUG] 尝试使用 images.generate 接口...")
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            return response.data[0].url, None
                    
        except openai.APIError as e:
            error_msg = f"API错误: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            return None, error_msg
        except openai.AuthenticationError as e:
            error_msg = f"API认证失败: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            return None, error_msg
        except openai.RateLimitError as e:
            error_msg = f"API请求频率限制: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            return None, error_msg
        except openai.BadRequestError as e:
            error_msg = f"请求参数错误: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            return None, error_msg
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            print(f"[DEBUG] 详细错误: {traceback.format_exc()}")
            return None, error_msg
