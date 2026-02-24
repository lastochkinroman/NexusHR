from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.candidate import Candidate
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
from sqlalchemy import select

router = APIRouter()
ai_service = AIService()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    content = await file.read()
    text = PDFService.extract_text(content)

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    
    embedding = await ai_service.get_embedding(text)

    new_candidate = Candidate(
        first_name = "Candidate",
        last_name = file.filename,
        email = f"test_{file.filename}@example.com",
        resume_text=text,
        embedding=embedding
    )

    db.add(new_candidate)
    await db.commit()
    await db.refresh(new_candidate)

    return {"status": "success", "candidate_id": new_candidate.id}


@router.get("/search")
async def search_candidates(
    query: str, 
    limit: int = 3, 
    db: AsyncSession = Depends(get_db)
):
    query_embedding = await ai_service.get_embedding(query)

    statement = (
        select(Candidate)
        .order_by(Candidate.embedding.l2_distance(query_embedding))
        .limit(limit)
    )
    
    result = await db.execute(statement)
    candidates = result.scalars().all()

    return [
        {
            "id": c.id,
            "name": f"{c.first_name} {c.last_name}",
            "relevance_score": "top match",
            "preview": c.resume_text[:200] + "..."
        } for c in candidates
    ]
