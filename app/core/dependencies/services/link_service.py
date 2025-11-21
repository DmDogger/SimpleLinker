from fastapi import Depends

from app.core.dependencies.repositories.link_repository import get_link_repository
from app.core.repositories.link import LinkRepository
from app.core.services.link import LinkService
from app.config.config import settings


def get_link_service(repository: LinkRepository = Depends(get_link_repository)):
    return LinkService(repository=repository, base_url=settings.base_url)
