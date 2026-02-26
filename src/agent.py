import ollama
import json
import os
from rich.console import Console
from .tools import TOOLS, TOOL_MAP

console = Console()
HISTORY_FILE = "/workspace/.grnt_code_history.json"

class Agent48:
    def __init__(self, model: str):
        self.model = model
        self.system_prompt = (
            "You are GRNT CODE v1.0.0, a high-performance CLI coding agent. "
            "You were created by alan ctril sunny. "
            "You provide direct, functional, and efficient solutions. "
            "You have access to tools for file manipulation and command execution in '/workspace'. "
            "Respond concisely and focus on the technical implementation."
        )
        self.messages = self._load_history()

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return [{"role": "system", "content": self.system_prompt}]

    def _save_history(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self.messages, f)
        except:
            pass

    def chat(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        while True:
            try:
                # If there are no tool calls pending, we can stream the response
                response_stream = ollama.chat(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOLS,
                    stream=True,
                )
                
                full_message = {'role': 'assistant', 'content': ''}
                
                for chunk in response_stream:
                    if chunk.get('message', {}).get('tool_calls'):
                        # If tool calls are detected, we collect them
                        if 'tool_calls' not in full_message:
                            full_message['tool_calls'] = []
                        full_message['tool_calls'].extend(chunk['message']['tool_calls'])
                    
                    content = chunk.get('message', {}).get('content', '')
                    if content:
                        full_message['content'] += content
                        yield content  # Yield the content chunk for streaming
                
                self.messages.append(full_message)
                self._save_history()

                if not full_message.get('tool_calls'):
                    return  # End of the conversation turn

                # Handle tool calls
                for tool_call in full_message['tool_calls']:
                    function_name = tool_call['function']['name']
                    args = tool_call['function']['arguments']
                    
                    if function_name in TOOL_MAP:
                        console.print(f"\n[bold blue]Executing Tool:[/bold blue] [cyan]{function_name}[/cyan]({args})")
                        tool_result = TOOL_MAP[function_name](**args)
                        
                        self.messages.append({
                            'role': 'tool',
                            'name': function_name,
                            'content': str(tool_result),
                        })
                    else:
                        self.messages.append({
                            'role': 'tool',
                            'name': function_name,
                            'content': f"Error: Tool '{function_name}' not found.",
                        })
                self._save_history()

            except Exception as e:
                yield f"\nOllama Error: {str(e)}"
                return
