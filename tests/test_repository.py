import pytest
from pydantic import HttpUrl

from app.core.models.db.links import Link
from app.core.repositories.link import LinkRepository
from tests.conftest import TestingSessionLocal, engine
from app.core.dependencies.database import Base

pytestmark = pytest.mark.asyncio


async def test_create_link():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with TestingSessionLocal() as session:
            repo = LinkRepository(session)
            link_data = {
                "link": "http://example.com",
                "slug": "abcdef"
            }
            link = Link(**link_data)
            await repo.add(link)
            await session.flush()  # Flush to get the ID
            link_id = link.id
            await session.commit()

            stmt = await session.get(Link, link_id)
            assert stmt is not None
            assert stmt.link == link_data["link"]
            assert stmt.slug == link_data["slug"]
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def test_get_by_url():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with TestingSessionLocal() as session:
            repo = LinkRepository(session)
            url = HttpUrl("http://example-get.com")
            link_data = {
                "link": str(url),
                "slug": "getslug"
            }
            link = Link(**link_data)
            await repo.add(link)
            await session.commit()

            found_link = await repo.get_by_url(url)
            assert found_link is not None
            assert found_link.slug == link_data["slug"]
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def test_get_by_slug():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with TestingSessionLocal() as session:
            repo = LinkRepository(session)
            link_data = {
                "link": "http://example-slug.com",
                "slug": "slugtest"
            }
            link = Link(**link_data)
            await repo.add(link)
            await session.commit()

            found_link = await repo.get_by_slug(link_data["slug"])
            assert found_link is not None
            assert found_link.link == link_data["link"]
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def test_soft_delete():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with TestingSessionLocal() as session:
            repo = LinkRepository(session)
            link_data = {
                "link": "http://example-delete.com",
                "slug": "deletest"
            }
            link = Link(**link_data)
            await repo.add(link)
            await session.flush()
            link_id = link.id
            await session.commit()

            await repo.delete(link_id)

            deleted_link = await repo.get(link_id)
            assert deleted_link is None

            stmt = await session.get(Link, link_id)
            assert stmt is not None
            assert stmt.is_active is False
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
