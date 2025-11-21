from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import select, update as sql_update

from app.core.models.dto.links import CreateShortLink
from app.core.repositories.base import BaseSQLAlchemyRepository
from app.core.models.db.links import Link


class LinkRepository(BaseSQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session)

    async def create_from_dto(self,
                              dto: CreateShortLink,
                              slug: str) -> Link:
        return Link(
                    link=str(dto.link),
                    slug=slug
        )

    async def add(self, model: Link) -> None:
        self.session.add(model)

    async def get_link_by_slug(self, slug: str):
        stmt = select(Link.link).where(Link.slug == slug,
                                       Link.is_active == True)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get(self, id_: UUID) -> Link | None:
        stmt = select(Link).where(Link.id == id_,
                                  Link.is_active == True)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_url(self, link: HttpUrl) -> None | Link:
        stmt = select(Link).where(Link.link == str(link),
                                  Link.is_active == True)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_slug(self, slug: str):
        stmt = select(Link).where(Link.slug == slug,
                                  Link.is_active == True)
        result = await self.session.scalars(stmt)
        return result.first()

    async def update(self, id_: UUID, updated_data: dict) -> Link | None:
        upd_stmt = (
            sql_update(Link)
            .where(Link.id == id_,
                   Link.is_active == True)
            .values(**updated_data)
        )
        await self.session.execute(upd_stmt)
        return await self.get(id_)

    async def delete(self, id_: UUID) -> None:
        soft_dlt_stmt = (
            sql_update(Link)
            .where(Link.id == id_,
                   Link.is_active == True)
            .values(is_active=False)
        )
        await self.session.execute(soft_dlt_stmt)








