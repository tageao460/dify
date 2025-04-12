import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage
"""
identity:
  name: visionx_run_video_syn
  author: wjl
  label:
    en_US: VisionX Run Video Syn
    zh_Hans: 视觉X合成视频
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX Run Video Syn
    zh_Hans: 视觉X合成视频
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to run video syn.
parameters:
  - name: video_metadata
    type: string
    required: true
    label:
      en_US: video_metadata
      zh_Hans: 视频元数据
      pt_BR: metadados do vídeo
    human_description:
      en_US: video_metadata
      zh_Hans: 视频元数据
      pt_BR: metadados do vídeo
    form: form
  - name: canvas_width
    type: string
    required: false
    label:
      en_US: canvas_width
      zh_Hans: 画布宽度
      pt_BR: largura do canvas
    form: form
  - name: canvas_height
    type: string
    required: false
    label:
      en_US: canvas_height
      zh_Hans: 画布高度
      pt_BR: altura do canvas
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

class VisionXRunVideoSynTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        video_metadata = tool_parameters.get("video_metadata", "")
        canvas_width = tool_parameters.get("canvas_width", 960)
        canvas_height = tool_parameters.get("canvas_height", 540)
        task_id = tool_parameters.get("task_id", "")
        add_title = tool_parameters.get("add_title", True)
        add_danmu = tool_parameters.get("add_danmu", False)
        add_bgm = tool_parameters.get("add_bgm", True)
        add_tts = tool_parameters.get("add_tts", True)
        add_subtitle = tool_parameters.get("add_subtitle", True)
        
        if not video_metadata:
            return self.create_text_message("Please tell me your video_metadata")

        try:
            """
            {
            "video_metadata", "canvas_width", "canvas_height", "task_id"
            }
            """
            payload = {
                "task_type": "run_video_syn",
                "input": {
                    "video_metadata": video_metadata,
                    "canvas_width": canvas_width,
                    "canvas_height": canvas_height,
                    "task_id": task_id,
                    "add_title": add_title,
                    "add_danmu": add_danmu,
                    "add_bgm": add_bgm,
                    "add_tts": add_tts,
                    "add_subtitle": add_subtitle,
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
            