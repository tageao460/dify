import json
from typing import Any, Optional, Union

import requests

from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

class VisionXCallGeminiSingleTool(BuiltinTool):
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
        gemini_video_name = tool_parameters.get("gemini_video_name", "")
        
        if not prompt:
            return self.create_text_message("Please tell me your prompt")
        if not gemini_video_name:
            return self.create_text_message("Please tell me your gemini_video_name")

        try:
            """
            {
            "video_oss_path", "task_id", "threshold", "keep_length",
            "clip_duration", "canvas_height", "canvas_width"
            }
            """
            payload = {
                "task_type": "call_gemini_single",
                "input": {
                    "prompt": prompt,
                    "gemini_video_name": gemini_video_name,
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
            