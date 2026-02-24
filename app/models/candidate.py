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
    
    resume_text = Column(Text, nullable=True)
    
    embedding = Column(Vector(1024), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repl__(self):
        return f"<Candidate(name={self.first_name}  {self.last_name}, email={self.email})>"