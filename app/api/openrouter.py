from dotenv import load_dotenv

import aiohttp
import asyncio
import os


load_dotenv(dotenv_path=" ") # CHANGE IT!

key = os.getenv("KEY")
model = os.getenv("AIMODEL")
url = "https://openrouter.ai/api/v1/chat/completions"


async def _request(prompt: str, system_prompt: str = None) -> str:
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/mercyriobot",
        "X-Title": "AI Assistant"
    }

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error = await response.text()
                    raise Exception(f"API Error {response.status}: {error}")

    except Exception as e:
        return f"Ошибка: {str(e)}"