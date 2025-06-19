from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, Generator
from jinja2 import Environment, FileSystemLoader
import json
import time
import os

app = FastAPI()

# 加载 Jinja2 模板
env = Environment(loader=FileSystemLoader("templates"))

class InvokeRequest(BaseModel):
    mcp_json: Dict[str, Any]

class StreamInvokeRequest(BaseModel):
    mcp_json: Dict[str, Any]
    stream: bool = True

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
                },
                "stream": {
                    "type": "boolean",
                    "description": "是否使用流式响应",
                    "default": False
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

def generate_code_stream(mcp_json: Dict[str, Any]) -> Generator[str, None, None]:
    """生成流式代码响应"""
    model = mcp_json.get("model", {})
    control = mcp_json.get("control", {})
    prompt = mcp_json.get("prompt", "")
    
    # 模拟分步骤生成代码
    steps = [
        {"step": "parsing", "message": "正在解析 MCP 数据结构..."},
        {"step": "template_loading", "message": "正在加载 React 模板..."},
        {"step": "rendering", "message": "正在渲染组件代码..."},
        {"step": "optimization", "message": "正在优化生成的代码..."},
        {"step": "complete", "message": "代码生成完成"}
    ]
    
    # 发送开始事件
    yield f"data: {json.dumps({'type': 'start', 'message': '开始生成 React 代码'})}\n\n"
    
    # 发送进度事件
    for i, step in enumerate(steps[:-1]):
        time.sleep(0.5)  # 模拟处理时间
        progress = (i + 1) / len(steps) * 100
        yield f"data: {json.dumps({'type': 'progress', 'step': step['step'], 'message': step['message'], 'progress': progress})}\n\n"
    
    # 生成最终代码
    template = env.get_template("react_template.j2")
    code = template.render(model=model, control=control, prompt=prompt)
    
    # 发送完成事件
    final_step = steps[-1]
    yield f"data: {json.dumps({'type': 'progress', 'step': final_step['step'], 'message': final_step['message'], 'progress': 100})}\n\n"
    
    # 发送结果
    yield f"data: {json.dumps({'type': 'result', 'output': code})}\n\n"
    
    # 发送结束事件
    yield f"data: {json.dumps({'type': 'end'})}\n\n"

@app.post("/invoke/stream")
def invoke_stream(data: StreamInvokeRequest):
    """支持 SSE 的流式代码生成端点"""
    def event_stream():
        try:
            for chunk in generate_code_stream(data.mcp_json):
                yield chunk
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

@app.get("/")
def read_root():
    return {"message": "MCP React Code Generator with SSE support"}

@app.get("/test")
def test_page():
    """提供 SSE 测试页面"""
    try:
        with open("templates/sse_test.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>测试页面未找到</h1><p>请确保 templates/sse_test.html 文件存在</p>")
