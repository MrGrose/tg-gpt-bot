import httpx
from bot.domain.interfaces import LLMProvider
from bot.config import SYSTEM_PROMPT


class DeepSeekProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None

    async def _get_client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def generate(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = SYSTEM_PROMPT,
    ) -> str:
        client = await self._get_client()

        full_messages = []
        has_system = any(msg.get("role") == "system" for msg in messages)

        if system_prompt and not has_system:
            full_messages.append({"role": "system", "content": system_prompt})

        full_messages.extend(messages)

        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": full_messages,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self):
        if self._client:
            await self._client.aclose()
