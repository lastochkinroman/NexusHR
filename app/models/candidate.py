from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector 
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Сюда мы запишем весь текст из PDF резюме
    resume_text = Column(Text, nullable=True)
    
    # ВЕКТОР: Это массив из 1536 чисел (стандарт для OpenAI моделей)
    # Именно по нему мы будем искать кандидатов "по смыслу"
    embedding = Column(Vector(1536), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())