import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

"""
identity:
  name: visionx_call_gemini_each
  author: wjl
  label:
    en_US: VisionX Call Gemini Each
    zh_Hans: 视觉X调用Gemini每个片段
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX Call Gemini Each
    zh_Hans: 视觉X调用Gemini每个片段
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to call gemini each.
parameters:
  - name: prompt
    type: string
    required: true
    label:
      en_US: prompt
      zh_Hans: 提示词
      pt_BR: prompt
    human_description:
      en_US: prompt
      zh_Hans: 提示词
      pt_BR: prompt
    form: form
  - name: local_video_dir
    type: string
    required: true
    label:
      en_US: local_video_dir
      zh_Hans: 本地视频目录
      pt_BR: diretório local do vídeo
    form: form
"""

class VisionXCallGeminiEachTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        prompt = tool_parameters.get("prompt", "")
        local_video_dir = tool_parameters.get("local_video_dir", "")
        
        if not prompt:
            return self.create_text_message("Please tell me your prompt")
        if not local_video_dir:
            return self.create_text_message("Please tell me your local_video_dir")

        try:
            """
            {
            "video_oss_path", "task_id", "threshold", "keep_length",
            "clip_duration", "canvas_height", "canvas_width"
            }
            """
            payload = {
                "task_type": "call_gemini_each",
                "input": {
                    "prompt": prompt,
                    "local_video_dir": local_video_dir,
                    "clip_duration": 0.3,
                    "temperature": 0.5,
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
            