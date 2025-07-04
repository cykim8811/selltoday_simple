import anthropic

client = anthropic.Anthropic()

usage = 0
cost = {
    "claude-3-haiku-20240307": {
        "input": 0.25 / 1000000,
        "output": 1.25 / 1000000
    },
    "claude-3-sonnet-20240229": {
        "input": 3 / 1000000,
        "output": 15 / 1000000
    },
    "claude-3-opus-20240229": {
        "input": 15 / 1000000,
        "output": 75 / 1000000
    }
}

models = {
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-sonnet-20240229",
    "haiku": "claude-3-haiku-20240307",
}

class ChatContext:
    def __init__(self, system_prompt, model="haiku"):
        self.messages = []
        self.system_prompt = system_prompt
        self.model = model if model not in models else models[model]
    
    def ask(self, message, force_format=None, **kwargs):
        global usage
        self.messages.append({"role": "user", "content": message})
        if force_format:
            self.messages.append({"role": "assistant", "content": force_format})
        response = client.messages.create(
            **{
                "model": self.model,
                "max_tokens": 1000,
                "temperature": 0.7,
                "system": self.system_prompt,
                "messages": self.messages,
                **kwargs
            }
        )
        usage += cost[self.model]["input"] * response.usage.input_tokens + cost[self.model]["output"] * response.usage.output_tokens
        if force_format:
            self.messages.pop()
            self.messages.append({"role": "assistant", "content": force_format + response.content[0].text})
            return force_format + response.content[0].text
        else:
            self.messages.append({"role": "assistant", "content": response.content[0].text})
            return response.content[0].text

    def copy(self, rollback=None):
        new_context = ChatContext(self.system_prompt)
        new_context.messages = self.messages.copy()
        if rollback:
            new_context.messages = new_context.messages[:rollback]
        return new_context
    
    def savepoint(self):
        return len(self.messages)


def singleChat(message, system_prompt="", force_format=None):
    context = ChatContext(system_prompt)
    return context.ask(message, force_format)

def getUsage():
    global usage
    current_usage = usage
    usage = 0
    return current_usage
