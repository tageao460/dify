import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

"""
identity:
  name: visionx_tts_preprocess
  author: wjl
  label:
    en_US: VisionX TTS Preprocess
    zh_Hans: 视觉XTTS预处理
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX TTS Preprocess
    zh_Hans: 视觉XTTS预处理
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to call llm node.
parameters:
  - name: oss_video_path
    type: string
    required: true
    label:
      en_US: oss_video_path
      zh_Hans: 视频OSS路径
      pt_BR: caminho do vídeo OSS
    human_description:
      en_US: oss_video_path
      zh_Hans: 视频OSS路径
      pt_BR: caminho do vídeo OSS
    form: form
  - name: subtitle_script
    type: string
    required: true
    label:
      en_US: subtitle_script
      zh_Hans: 字幕脚本
      pt_BR: script de legendas
    form: form
  - name: title
    type: string
    required: true
    label:
      en_US: title
      zh_Hans: 标题
      pt_BR: título
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

class VisionXTTSPreprocessTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        oss_video_path = tool_parameters.get("oss_video_path", "")
        subtitle_script = tool_parameters.get("subtitle_script", "")
        title = tool_parameters.get("title", "")
        task_id = tool_parameters.get("task_id", "")
        
        if not oss_video_path:
            return self.create_text_message("Please tell me your oss_video_path")
        if not subtitle_script:
            return self.create_text_message("Please tell me your subtitle_script")
        if not title:
            return self.create_text_message("Please tell me your title")
        if not task_id:
            return self.create_text_message("Please tell me your task_id")

        title_info = {"title": title, "bgm": "", "title_font": "", "subtitle_font": ""}
        try:
            """
            {
            "oss_video_path", "subtitle_script", "title_info", "task_id"
            }
            """
            payload = {
                "task_type": "tts_preprocess",
                "input": {
                    "oss_video_path": oss_video_path,
                    "subtitle_script": subtitle_script,
                    "title_info": title_info,
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
            