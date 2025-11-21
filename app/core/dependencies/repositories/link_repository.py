from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_session
from app.core.repositories.link import LinkRepository

def get_link_repository(
        session: AsyncSession = Depends(get_session),
        ) -> LinkRepository:
    """
    Constructs an LinkRepository instance with injected AsyncSession
    """
    return LinkRepository(session=session)

