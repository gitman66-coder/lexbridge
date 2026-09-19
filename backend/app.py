from fastapi import FastAPI, Depends, UploadFile, File,  Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from knowledge.embedding import generate_embedding
from database import Base, engine, get_db

from models import Case, LegalDocument, LegalChunk, CaseBrief

from schemas.legal_search import LegalSearch
from schemas.intake_req import IntakeRequest

from knowledge.ingest import extract_text, create_chunks
from knowledge.case_state import CaseState

from graph.case_pipeline import case_pipeline

from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import cast
from pathlib import Path
import shutil

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LexBridge API",
    description="API for managing legal cases, documents, and briefs.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             
    allow_credentials=False,        
    allow_methods=["*"],             
    allow_headers=["*"],            
)

@app.get("/")
def home():
    return {"message": "Welcome to the LexBridge application!"}

@app.post("/get-legal-documents/")
def get_legal_documents(name: str = Form(...), jurisdiction: str = Form(...), source_url: str = Form(...),
                     file: UploadFile = File(...), db: Session = Depends(get_db)):

    upload_dir = Path("documents/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and TXT files are allowed.")

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_document = LegalDocument(
        name=name,
        jurisdiction=jurisdiction,
        source_url=source_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    extracted_text = extract_text(file_path)
    chunks = create_chunks(extracted_text)

    for chunk in chunks:
        embedding = generate_embedding(chunk["content"])  

        new_chunk = LegalChunk(
            document_id=new_document.id,
            section=chunk.get("section"),
            content=chunk.get("content"),
            embedding=embedding 
        )
        db.add(new_chunk)

    db.commit()

    return {"message": "Legal document and its chunks have been successfully added to the database."}

@app.post("/search-legal-documents/")
def search_legal_documents(search_request: LegalSearch, db: Session = Depends(get_db)):
    query_embedding = generate_embedding(search_request.query)

    statement = (
        select(LegalChunk)
        .where(LegalChunk.embedding.is_not(None))
        .order_by(
            LegalChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(search_request.top_k)
    )

    results = db.execute(statement).scalars().all()

    return {
        "question": search_request.query,
        "results": [
            {
                "document_id": chunk.document_id,
                "section": chunk.section,
                "content": chunk.content
            }
            for chunk in results
        ]
    }

@app.post("/intake/")
def intake(
    intake_request: IntakeRequest,
    db: Session = Depends(get_db)
):

    state: CaseState = {
        "conversation": [
            message.model_dump()
            for message in intake_request.conversation
        ]
    }

    result = cast(
        CaseState,
        case_pipeline.invoke(state)
    )

    case_id = None

    if result.get("intake_complete", False):

        case = Case(
            status="TRIAGE_COMPLETE",
            legal_area=result.get("legal_area", ""),
            legal_issue=result.get("legal_issue", ""),
            urgency_score=result.get("urgency_score", 0),
            priority=result.get("priority", "LOW"),
            intake_data=str({
                "conversation": result.get(
                    "conversation", []
                ),
                "jurisdiction": result.get(
                    "jurisdiction", ""
                ),
                "facts": result.get(
                    "facts", ""
                ),
                "classification_reason": result.get(
                    "classification_reason", ""
                ),
                "research_queries": result.get(
                    "research_queries", []
                ),
                "findings": result.get(
                    "findings", ""
                ),
                "relevant_sections": result.get(
                    "relevant_sections", []
                ),
                "sources": result.get(
                    "sources", []
                ),
                "unresolved_questions": result.get(
                    "unresolved_questions", []
                ),
                "triage_reason": result.get(
                    "triage_reason", ""
                )
            })
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        case_id = case.id

        case_brief = CaseBrief(
            case_id=case.id,
            facts=result.get("facts", ""),
            legal_issue=result.get("legal_issue", ""),
            research=result.get("findings", ""),
            suggested_next_step=(
                "Human lawyer review based on "
                "the case brief."
            ),
            draft=result.get("case_brief", "")
        )

        db.add(case_brief)
        db.commit()
        db.refresh(case_brief)

    return {
        "intake_complete": result.get(
            "intake_complete", False
        ),

        "case_id": case_id,

        "question": (
            result.get(
                "missing_information",
                [None]
            )[0]
            if result.get("missing_information")
            else None
        ),

        "legal_issue": result.get("legal_issue"),
        "jurisdiction": result.get("jurisdiction"),
        "facts": result.get("facts"),
        "legal_area": result.get("legal_area"),
        "urgency_score": result.get("urgency_score"),
        "priority": result.get("priority"),
        "triage_reason": result.get("triage_reason"),
        "case_brief": result.get("case_brief"),
        "conversation": result.get("conversation", [])
    }

@app.get("/get-case-details")
def get_case_details(case_id: int, db: Session = Depends(get_db)):

    case = db.get(Case, case_id)

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found."
        )

    statement = (
    select(CaseBrief)
    .where(CaseBrief.case_id == case_id)
)

    case_brief = db.execute(statement).scalars().first()

    return {
        "case": {
            "id": case.id,
            "status": case.status,
            "legal_area": case.legal_area,
            "legal_issue": case.legal_issue,
            "urgency_score": case.urgency_score,
            "priority": case.priority,
            "intake_data": case.intake_data,
            "created_at": case.created_at
        },

        "case_brief": {
            "id": case_brief.id if case_brief else None,
            "facts": case_brief.facts if case_brief else None,
            "legal_issue": case_brief.legal_issue if case_brief else None,
            "research": case_brief.research if case_brief else None,
            "suggested_next_step": (
                case_brief.suggested_next_step
                if case_brief else None
            ),
            "draft": case_brief.draft if case_brief else None
        }
    }

@app.post("/cases/{case_id}/review")
def review_case(
    case_id: int,
    approved: bool,
    db: Session = Depends(get_db)
):

    case = db.get(Case, case_id)

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found."
        )

    if approved:
        case.status = "LAWYER_APPROVED"
    else:
        case.status = "REQUIRES_REVISION"

    db.commit()
    db.refresh(case)

    return {
        "case_id": case.id,
        "status": case.status,
        "message": (
            "Case approved by lawyer."
            if approved
            else "Case marked for revision."
        )
    }

@app.get("/cases")
def get_cases(db: Session = Depends(get_db)):

    statement = (
        select(Case)
        .order_by(Case.urgency_score.desc())
    )

    cases = db.execute(statement).scalars().all()

    return {
        "cases": [
            {
                "id": case.id,
                "status": case.status,
                "legal_area": case.legal_area,
                "legal_issue": case.legal_issue,
                "urgency_score": case.urgency_score,
                "priority": case.priority,
                "created_at": case.created_at
            }
            for case in cases
        ]
    }
