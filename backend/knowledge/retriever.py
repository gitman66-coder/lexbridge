from sqlalchemy import select
from sqlalchemy.orm import Session

from knowledge.embedding import generate_embedding
from models.legal import LegalChunk


def search_legal_documents(
    query: str,
    top_k: int,
    db: Session
) -> list[LegalChunk]:

    query_embedding = generate_embedding(query)

    statement = (
        select(LegalChunk)
        .where(LegalChunk.embedding.is_not(None))
        .order_by(
            LegalChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(top_k)
    )

    results = db.execute(statement).scalars().all()

    return list(results)