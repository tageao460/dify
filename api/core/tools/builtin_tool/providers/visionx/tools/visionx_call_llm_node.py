import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

"""
identity:
  name: visionx_call_llm_node
  author: wjl
  label:
    en_US: VisionX Call LLM Node
    zh_Hans: 视觉X调用LLM节点
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX Call LLM Node
    zh_Hans: 视觉X调用LLM节点
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to call llm node.
parameters:
  - name: llm_model
    type: select
    default: gemini
    required: false
    form: llm
    options:
      - value: gemini
        label:
          en_US: gemini-1.5-pro
          zh_Hans: Gemini 1.5 Pro
          pt_BR: Gemini 1.5 Pro
      - value: flash
        label:
          en_US: gemini-1.5-flash
          zh_Hans: Gemini 1.5 Flash
          pt_BR: Gemini 1.5 Flash
      - value: claude
        label:
          en_US: claude 3.5 sonnet
          zh_Hans: Claude 3.5 Sonnet
          pt_BR: Claude 3.5 Sonnet
      - value: gpt-4o
        label:
          en_US: gpt-4o
          zh_Hans: GPT-4o
          pt_BR: GPT-4o
    label:
      en_US: llm_model
      zh_Hans: LLM模型
      pt_BR: modelo LLM
    human_description:
      en_US: llm_model
      zh_Hans: LLM模型
      pt_BR: modelo LLM
  - name: prompt
    type: string
    required: true
    label:
      en_US: prompt
      zh_Hans: 提示词
      pt_BR: prompt
    form: llm
  - name: check_json
    type: boolean
    default: false
    required: false
    label:
      en_US: check_json
      zh_Hans: 是否检查JSON
      pt_BR: check_json
    form: llm
  - name: template
    type: string
    required: false
    label:
      en_US: template
      zh_Hans: 模板
      pt_BR: template
    form: llm
"""

class VisionXCallLLMNodeTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        llm_model = tool_parameters.get("llm_model", "gemini")
        prompt = tool_parameters.get("prompt", "")
        check_json = tool_parameters.get("check_json", False)
        template = tool_parameters.get("template", "{}")
        
        if not prompt:
            return self.create_text_message("Please tell me your prompt")

        try:
            """
            {
            "prompt", "llm_model", "check_json", "template"
            }
            """
            payload = {
                "task_type": "call_llm",
                "input": {
                    "prompt": prompt,
                    "llm_model": llm_model,
                    "check_json": check_json,
                    "template": template,
                    "extra_info": {
                        "conversation_id": conversation_id,
                        "user_id": user_id,
                        "app_id": app_id,
                        "message_id": message_id,
                    }
                }
            }
            url = "http://8.154.35.143:8006"
            response = requests.post(url, json=payload)
            return self.create_text_message(response.text)
        except Exception as e:
            return self.create_text_message("Error: {}".format(e))
            