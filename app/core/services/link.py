from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from app.core.exceptions.links import NotFound
from app.core.models.dto.links import CreateShortLink
from app.core.repositories.link import LinkRepository
from app.core.utils.slug_utils import generate_slug

class LinkService:
    def __init__(self,
                 repository: LinkRepository,
                 base_url: str):
        self._repository = repository
        self._base_url = base_url


    async def generate_link(self, data: CreateShortLink) -> str:
        url = await self._repository.get_by_url(data.link)
        if url is not None:
            return f'{self._base_url}/{url.slug}'

        slug = await self._generate_unique_slug()
        link_obj = await self._repository.create_from_dto(dto=data, slug=slug)
        await self._repository.add(link_obj)
        await self._repository.session.commit()
        
        return f"{self._base_url}/{slug}"

    async def get_link_by_slug(self, slug: str) -> str | None:
        url = await self._repository.get_link_by_slug(slug)
        if not url:
            raise NotFound
        return str(url)


    async def _generate_unique_slug(self) -> str:
        """ Generate unique slug with recursion if exist """
        slug = generate_slug()
        if await self._repository.get_by_slug(slug):
            return await self._generate_unique_slug()
        return slug










