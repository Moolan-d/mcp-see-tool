#!/usr/bin/env python3
"""
MCP React Code Generator SSE 测试脚本
使用此脚本测试服务器端事件流功能
"""

import requests
import json
import time

def test_normal_invoke():
    """测试普通API调用"""
    print("🔄 测试普通API调用...")
    
    test_data = {
        "mcp_json": {
            "model": {
                "name": "TestComponent",
                "style": {
                    "width": 400,
                    "height": 300,
                    "backgroundColor": "#e3f2fd"
                }
            },
            "control": {
                "props": {
                    "hasAvatar": True
                }
            },
            "prompt": "生成一个测试组件"
        }
    }
    
    try:
        response = requests.post("http://localhost:8000/invoke", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 普通API调用成功:")
            print(result['output'])
        else:
            print(f"❌ 普通API调用失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 连接错误: {e}")

def test_sse_invoke():
    """测试SSE流式调用"""
    print("\n🌊 测试SSE流式调用...")
    
    test_data = {
        "mcp_json": {
            "model": {
                "name": "SSETestComponent",
                "style": {
                    "width": 500,
                    "height": 350,
                    "backgroundColor": "#f3e5f5"
                }
            },
            "control": {
                "props": {
                    "hasAvatar": True
                }
            },
            "prompt": "通过SSE生成一个测试组件"
        },
        "stream": True
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/invoke/stream", 
            json=test_data,
            stream=True,
            headers={
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache'
            }
        )
        
        if response.status_code == 200:
            print("✅ SSE连接建立成功，开始接收流式数据...")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])  # 移除 'data: ' 前缀
                            
                            if data['type'] == 'start':
                                print(f"🚀 {data['message']}")
                            elif data['type'] == 'progress':
                                print(f"⏳ {data['message']} ({data['progress']:.1f}%)")
                            elif data['type'] == 'result':
                                print("✅ 代码生成完成:")
                                print("=" * 50)
                                print(data['output'])
                                print("=" * 50)
                            elif data['type'] == 'end':
                                print("🎉 流式传输结束")
                                break
                            elif data['type'] == 'error':
                                print(f"❌ 错误: {data['error']}")
                                break
                                
                        except json.JSONDecodeError as e:
                            print(f"⚠️ JSON解析错误: {e}")
                            print(f"原始数据: {line}")
        else:
            print(f"❌ SSE调用失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ SSE连接错误: {e}")

def check_server_status():
    """检查服务器状态"""
    print("🔍 检查服务器状态...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器状态异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("请确保服务器已启动: python -m uvicorn main:app --reload --port 8000")
        return False

if __name__ == "__main__":
    print("🚀 MCP React Code Generator SSE 测试")
    print("=" * 50)
    
    if check_server_status():
        test_normal_invoke()
        time.sleep(1)
        test_sse_invoke()
    
    print("\n📋 手动测试提示:")
    print("1. 启动服务器: python -m uvicorn main:app --reload --port 8000")
    print("2. 访问测试页面: http://localhost:8000/test")
    print("3. 或使用此脚本测试: python test_sse.py") 