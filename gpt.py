from openai import OpenAI, api_key
import httpx
from config import ChatGPT_TOKEN



class ChatGptServices:
    client: OpenAI = None
    message_list: list = None

    def __init__(self):
        token = "sk-proj-" + ChatGPT_TOKEN[:3:-1] if ChatGPT_TOKEN.startswith('gpt:') else ChatGPT_TOKEN
        print(token)
        self.client = OpenAI(
            http_client=httpx.Client(
                proxies='http://18.199.183.77:49232'),
                api_key=token
            )
        self.message_list = []

    async def send_message_list(self) -> str:
        completion = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.message_list,
            max_tokens=3000,
            temperature=0.9
        )
        message = completion.choices[0].message
        self.message_list.append(message)
        return message.content

    def set_prompt(self, prompt_text: str) -> None:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})

    async def add_message(self, message_text: str) -> str:
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()