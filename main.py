from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

# 加载 Jinja2 模板
env = Environment(loader=FileSystemLoader("templates"))

class InvokeRequest(BaseModel):
    mcp_json: Dict[str, Any]

@app.get("/schema")
def get_schema():
    return {
        "name": "MCP React Code Generator",
        "description": "将 MCP 协议结构生成 React + TailwindCSS 代码",
        "parameters": {
            "type": "object",
            "properties": {
                "mcp_json": {
                    "type": "object",
                    "description": "MCP JSON，包括 model/control/prompt"
                }
            },
            "required": ["mcp_json"]
        }
    }

@app.post("/invoke")
def invoke(data: InvokeRequest):
    mcp = data.mcp_json
    model = mcp.get("model", {})
    control = mcp.get("control", {})
    prompt = mcp.get("prompt", "")

    # 模板渲染
    template = env.get_template("react_template.j2")
    code = template.render(model=model, control=control, prompt=prompt)

    return JSONResponse({
        "output": code
    })
