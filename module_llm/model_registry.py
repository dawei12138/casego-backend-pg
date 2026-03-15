# -*- coding: utf-8 -*-
"""
模型注册配置
维护各提供商支持的模型列表，新增模型只需在这里添加一行
"""
from module_llm.enums import ModelTypeEnum

# =============================================================================
# 模型定义：(model_id, display_name, model_type)
# =============================================================================

OPENAI_MODELS = [
    ("gpt-4o", "GPT-4o", ModelTypeEnum.CHAT),
    ("gpt-4o-mini", "GPT-4o Mini", ModelTypeEnum.CHAT),
    ("gpt-4-turbo", "GPT-4 Turbo", ModelTypeEnum.CHAT),
    ("gpt-4", "GPT-4", ModelTypeEnum.CHAT),
    ("gpt-3.5-turbo", "GPT-3.5 Turbo", ModelTypeEnum.CHAT),
    ("o1", "O1", ModelTypeEnum.CHAT),
    ("o1-mini", "O1 Mini", ModelTypeEnum.CHAT),
    ("o1-preview", "O1 Preview", ModelTypeEnum.CHAT),
    ("o3-mini", "O3 Mini", ModelTypeEnum.CHAT),
    ("text-embedding-3-large", "Embedding 3 Large", ModelTypeEnum.EMBEDDING),
    ("text-embedding-3-small", "Embedding 3 Small", ModelTypeEnum.EMBEDDING),
    ("dall-e-3", "DALL-E 3", ModelTypeEnum.IMAGE),
    ("whisper-1", "Whisper", ModelTypeEnum.AUDIO),
    ("tts-1", "TTS", ModelTypeEnum.AUDIO),
]

ANTHROPIC_MODELS = [
    ("claude-opus-4-20250514", "Claude Opus 4", ModelTypeEnum.CHAT),
    ("claude-sonnet-4-20250514", "Claude Sonnet 4", ModelTypeEnum.CHAT),
    ("claude-3-7-sonnet-20250219", "Claude 3.7 Sonnet", ModelTypeEnum.CHAT),
    ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet", ModelTypeEnum.CHAT),
    ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku", ModelTypeEnum.CHAT),
    ("claude-3-opus-20240229", "Claude 3 Opus", ModelTypeEnum.CHAT),
]

DEEPSEEK_MODELS = [
    ("deepseek-chat", "DeepSeek Chat", ModelTypeEnum.CHAT),
    ("deepseek-reasoner", "DeepSeek Reasoner (R1)", ModelTypeEnum.CHAT),
]

GOOGLE_MODELS = [
    ("gemini-2.0-flash", "Gemini 2.0 Flash", ModelTypeEnum.CHAT),
    ("gemini-2.0-flash-lite", "Gemini 2.0 Flash Lite", ModelTypeEnum.CHAT),
    ("gemini-1.5-pro", "Gemini 1.5 Pro", ModelTypeEnum.CHAT),
    ("gemini-1.5-flash", "Gemini 1.5 Flash", ModelTypeEnum.CHAT),
]

QWEN_MODELS = [
    ("qwen-max", "通义千问 Max", ModelTypeEnum.CHAT),
    ("qwen-plus", "通义千问 Plus", ModelTypeEnum.CHAT),
    ("qwen-turbo", "通义千问 Turbo", ModelTypeEnum.CHAT),
    ("qwen-long", "通义千问 Long", ModelTypeEnum.CHAT),
]

ZHIPU_MODELS = [
    ("glm-4-plus", "GLM-4 Plus", ModelTypeEnum.CHAT),
    ("glm-4", "GLM-4", ModelTypeEnum.CHAT),
    ("glm-4-flash", "GLM-4 Flash", ModelTypeEnum.CHAT),
    ("glm-4v", "GLM-4V (视觉)", ModelTypeEnum.CHAT),
]

MOONSHOT_MODELS = [
    ("moonshot-v1-128k", "Kimi 128K", ModelTypeEnum.CHAT),
    ("moonshot-v1-32k", "Kimi 32K", ModelTypeEnum.CHAT),
    ("moonshot-v1-8k", "Kimi 8K", ModelTypeEnum.CHAT),
]

OLLAMA_MODELS = [
    ("llama3.3", "Llama 3.3", ModelTypeEnum.CHAT),
    ("qwen2.5", "Qwen 2.5", ModelTypeEnum.CHAT),
    ("deepseek-r1", "DeepSeek R1", ModelTypeEnum.CHAT),
    ("mistral", "Mistral", ModelTypeEnum.CHAT),
    ("phi4", "Phi-4", ModelTypeEnum.CHAT),
    ("nomic-embed-text", "Nomic Embed", ModelTypeEnum.EMBEDDING),
]

# =============================================================================
# 提供商 -> 模型映射
# =============================================================================

PROVIDER_MODELS = {
    "openai": OPENAI_MODELS,
    "azure_openai": OPENAI_MODELS,  # Azure用同样的模型
    "anthropic": ANTHROPIC_MODELS,
    "deepseek": DEEPSEEK_MODELS,
    "google": GOOGLE_MODELS,
    "qwen": QWEN_MODELS,
    "zhipu": ZHIPU_MODELS,
    "moonshot": MOONSHOT_MODELS,
    "ollama": OLLAMA_MODELS,
}

# 所有已知模型（用于自定义提供商）
ALL_MODELS = []
for models in PROVIDER_MODELS.values():
    ALL_MODELS.extend(models)
# 去重（基于model_id）
ALL_MODELS = list({m[0]: m for m in ALL_MODELS}.values())


# =============================================================================
# 工具函数
# =============================================================================

def get_models_by_provider(provider_key: str) -> list:
    """
    获取提供商支持的模型列表

    Args:
        provider_key: 提供商标识

    Returns:
        模型列表，每项为 (model_id, display_name, model_type)
    """
    # 预置提供商返回对应模型
    if provider_key in PROVIDER_MODELS:
        return PROVIDER_MODELS[provider_key]

    # 自定义提供商返回所有模型（用户可以自己输入任意model_id）
    return ALL_MODELS


def get_model_info(model_id: str) -> dict | None:
    """
    获取模型信息

    Args:
        model_id: 模型ID

    Returns:
        {"model_id": ..., "display_name": ..., "model_type": ...} 或 None
    """
    for mid, name, mtype in ALL_MODELS:
        if mid == model_id:
            return {
                "model_id": mid,
                "display_name": name,
                "model_type": mtype.value
            }
    return None


def is_known_model(model_id: str) -> bool:
    """判断是否为已知模型"""
    return any(m[0] == model_id for m in ALL_MODELS)


if __name__ == "__main__":
    print(ALL_MODELS)
