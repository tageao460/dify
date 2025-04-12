import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

"""
identity:
  name: visionx_split_video
  author: wjl
  label:
    en_US: VisionX Split Video
    zh_Hans: 视觉X分割视频
    pt_BR: Divisão de vídeo VisionX
  icon: icon.svg
description:
  human:
    en_US: VisionX Split Video
    zh_Hans: 视觉X分割视频
    pt_BR: Divisão de vídeo VisionX
  llm: A tool when you want to split video.
parameters:
  - name: video_url
    type: string
    required: true
    label:
      en_US: video_url
      zh_Hans: 视频链接
      pt_BR: link do vídeo
    human_description:
      en_US: Video link
      zh_Hans: 视频链接
      pt_BR: link do vídeo
    form: form
  - name: task_id
    type: string
    required: true
    label:
      en_US: task_id
      zh_Hans: 任务ID
      pt_BR: ID da tarefa
    form: form
  - name: canvas_height
    type: number
    required: true
    label:
      en_US: canvas_height
      zh_Hans: 画布高度
      pt_BR: altura do canvas
    form: form
  - name: canvas_width
    type: number
    required: true
    label:
      en_US: canvas_width
      zh_Hans: 画布宽度
      pt_BR: largura do canvas
    form: form
"""

class VisionXSplitVideoTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        video_url = tool_parameters.get("video_url", "")
        task_id = tool_parameters.get("task_id", "")
        canvas_height = tool_parameters.get("canvas_height", 960)
        canvas_width = tool_parameters.get("canvas_width", 540)
        if not video_url:
            return self.create_text_message("Please tell me your video_url")

        try:
            """
            {
            "video_oss_path", "task_id", "threshold", "keep_length",
            "clip_duration", "canvas_height", "canvas_width"
            }
            """
            payload = {
                "task_type": "split_video",
                "input": {
                    "video_oss_path": video_url,
                    "task_id": task_id,
                    "threshold": 40,
                    "keep_length": 2,
                    "clip_duration": 0.3,
                    "canvas_height": canvas_height,
                    "canvas_width": canvas_width,
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
            return self.create_text_message("VisionX Split Video Tool Error: {}".format(e))
