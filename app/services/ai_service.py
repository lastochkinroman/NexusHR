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
    
    async def analyze_candidates(self, query: str, candidates_content: str) -> str:
        """
        Метод для финальной стадии RAG: генерация ответа на основе найденных данных.
        """
        system_prompt = (
            "Ты — профессиональный технический рекрутер в IT-компании. "
            "Твоя задача: проанализировать предоставленные резюме и ответить на запрос нанимающего менеджера. "
            "Пиши кратко, честно и только по делу. Если кандидат не подходит, укажи причины."
        )
        user_prompt = f"""
        Запрос менеджера: "{query}"

        Вот список найденных резюме из нашей базы данных:
        ---
        {candidates_content}
        ---

        На основе этих данных, составь краткий аналитический отчет по самому подходящему кандидату (или нескольким).
        """

        response = await self.client.chat.complete_async(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content