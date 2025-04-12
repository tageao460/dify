import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

"""
identity:
  name: visionx_call_tts
  author: wjl
  label:
    en_US: VisionX Call TTS
    zh_Hans: 视觉X调用TTS
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX Call TTS
    zh_Hans: 视觉X调用TTS
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to call tts.
parameters:
  - name: subtitle_matadata
    type: string
    required: true
    label:
      en_US: subtitle_matadata
      zh_Hans: 字幕脚本
      pt_BR: script de legendas
    human_description:
      en_US: subtitle_matadata
      zh_Hans: 字幕脚本
      pt_BR: script de legendas
    form: form
  - name: task_id
    type: string
    required: true
    label:
      en_US: task_id
      zh_Hans: 任务ID
      pt_BR: ID da tarefa
    form: form
"""

class VisionXCallTTSNodeTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        subtitle_matadata = tool_parameters.get("subtitle_matadata", "")
        task_id = tool_parameters.get("task_id", "")
        
        if not subtitle_matadata:
            return self.create_text_message("Please tell me your subtitle_matadata")
        if not task_id:
            return self.create_text_message("Please tell me your task_id")

        try:
            """
            {
            "subtitle_matadata", "task_id"
            }
            """
            payload = {
                "task_type": "gen_tts",
                "input": {
                    "subtitle_matadata": subtitle_matadata,
                    "task_id": task_id,
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
            