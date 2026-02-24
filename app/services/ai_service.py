from mistralai import Mistral 
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)

    async def get_embedding(self, text: str) -> list[float]:
        """Превращает текст в вектор (1024 числа для Mistral)"""
        truncated_text = text[:10000] 
        
        # Новый асинхронный вызов эмбеддингов
        response = await self.client.embeddings.create_async(
            model="mistral-embed",
            inputs=[truncated_text] 
        )
        return response.data[0].embedding
