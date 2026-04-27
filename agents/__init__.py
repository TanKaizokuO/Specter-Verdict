import os
import yaml

def get_llm():
    try:
        with open("config/settings.yaml", "r") as f:
            config = yaml.safe_load(f)
            model_name = config.get("llm", {}).get("model", "claude- sonnet-4-20250514")
            temp = config.get("llm", {}).get("temperature", 0.4)
            max_tokens = config.get("llm", {}).get("max_tokens", 1024)
    except Exception:
        model_name, temp, max_tokens = "gpt-4o", 0.4, 1024

    # We map claude names to Anthropic and gpt to OpenAI.
    is_openai_model = "gpt" in model_name.lower() or (os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"))
    
    if is_openai_model:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name if "gpt" in model_name.lower() else "gpt-4o", 
            temperature=temp, 
            max_tokens=max_tokens
        )
    else:
        from langchain_anthropic import ChatAnthropic
        # Fixed model name typo from config if necessary
        clean_model_name = "claude-3-5-sonnet-20240620" if "sonnet" in model_name.lower() else model_name
        return ChatAnthropic(
            model=clean_model_name, 
            temperature=temp, 
            max_tokens=max_tokens
        )
