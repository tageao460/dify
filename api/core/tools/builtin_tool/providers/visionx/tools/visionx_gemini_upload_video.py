import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

class VisionXGeminiUploadVideoTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        video_oss_path = tool_parameters.get("video_oss_path", "")
        task_id = tool_parameters.get("task_id", "")
        canvas_width = tool_parameters.get("canvas_width", "")
        canvas_height = tool_parameters.get("canvas_height", "")
        
        if not video_oss_path:
            return self.create_text_message("Please tell me your video_oss_path")
        if not task_id:
            return self.create_text_message("Please tell me your task_id")

        try:
            """
            {
            "video_oss_path", "task_id", "threshold", "keep_length",
            "clip_duration", "canvas_height", "canvas_width"
            }
            """
            payload = {
                "task_type": "upload_only",
                "input": {
                    "video_oss_path": video_oss_path,
                    "task_id": task_id,
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
            return self.create_text_message("Error: {}".format(e))
            