from configs import (PROMPT_TEMPLATES)
from webui_pages.utils import *

def dialogue_page_gradio(api: ApiRequest, prompt: str):
    history_len = 3
    temperature = 0.0
    selected_kb = 'Trial'
    kb_top_k = 3
    score_threshold=1.00
    llm_model=  "qwen-api"
    index_prompt = {
        "LLM 对话": "llm_chat",
        "自定义Agent问答": "agent_chat",
        "搜索引擎问答": "search_engine_chat",
        "知识库问答": "knowledge_base_chat",
        "文件对话": "knowledge_base_chat",
    }
    dialogue_mode = "知识库问答"
    prompt_templates_kb_list = list(PROMPT_TEMPLATES[index_prompt[dialogue_mode]].keys())
    prompt_template_name = prompt_templates_kb_list[3]
    
    text = ""
    for d in api.knowledge_base_chat(prompt,
                                        knowledge_base_name=selected_kb,
                                        top_k=kb_top_k,
                                        score_threshold=score_threshold,
                                        # history=history,
                                        model=llm_model,
                                        prompt_name=prompt_template_name,
                                        temperature=temperature):
        if error_msg := check_error_msg(d):  # check whether error occured
            print(f"Error while generating response: {error_msg}")
        elif chunk := d.get("answer"):
            text += chunk
            # chat_box.update_msg(text, element_index=0)
    # chat_box.update_msg(text, element_index=0, streaming=False)
    # chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
    print(text)
    return text

if __name__ == "__main__":
    api = ApiRequest(base_url=api_address())
    text = dialogue_page_gradio(api, "给我推荐一本书，要求：动漫，并给出推荐理由。你的回答格式为：\"书名：{}\n推荐理由：{}\"")
    name = text[text.find("书名：") + 3:text.find("推荐理由：")].strip(' ').strip('\n')
    reason = text[text.find("推荐理由：") + 5:]
    print(name, reason)
