import pytest
from unittest.mock import AsyncMock

from pydantic import HttpUrl

from app.core.models.db.links import Link
from app.core.models.dto.links import CreateShortLink
from app.core.repositories.link import LinkRepository
from app.core.services.link import LinkService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_repo(mocker):
    mock = mocker.MagicMock(spec=LinkRepository)
    mock.session = mocker.MagicMock()
    mock.session.commit = mocker.AsyncMock()
    return mock


@pytest.fixture
def link_service(mock_repo):
    return LinkService(repository=mock_repo, base_url="http://test.com")


async def test_generate_link_new_url(link_service, mock_repo):
    dto = CreateShortLink(link=HttpUrl("http://new-example.com"))
    
    mock_repo.get_by_url = AsyncMock(return_value=None)
    mock_repo.get_by_slug = AsyncMock(return_value=None)
    
    created_link = Link(link=str(dto.link), slug="newslug")
    mock_repo.create_from_dto = AsyncMock(return_value=created_link)
    mock_repo.add = AsyncMock()

    link_service._generate_unique_slug = AsyncMock(return_value="newslug")

    result_url = await link_service.generate_link(dto)

    mock_repo.get_by_url.assert_called_once_with(dto.link)
    link_service._generate_unique_slug.assert_called_once()
    
    mock_repo.create_from_dto.assert_called_once_with(dto=dto, slug="newslug")
    mock_repo.add.assert_called_once_with(created_link)
    mock_repo.session.commit.assert_called_once()

    assert result_url == "http://test.com/newslug"


async def test_generate_link_existing_url(link_service, mock_repo):
    dto = CreateShortLink(link=HttpUrl("http://existing-example.com"))
    existing_link = Link(link=str(dto.link), slug="exists")

    mock_repo.get_by_url = AsyncMock(return_value=existing_link)

    result_url = await link_service.generate_link(dto)

    mock_repo.get_by_url.assert_called_once_with(dto.link)
    
    mock_repo.create_from_dto.assert_not_called()
    mock_repo.add.assert_not_called()
    mock_repo.session.commit.assert_not_called()

    assert result_url == "http://test.com/exists"


async def test_generate_unique_slug_collision(link_service, mock_repo, mocker):
    dto = CreateShortLink(link=HttpUrl("http://collision-test.com"))

    mocker.patch('app.core.services.link.generate_slug', side_effect=['collide', 'unique'])
    
    mock_repo.get_by_url = AsyncMock(return_value=None)
    mock_repo.get_by_slug = AsyncMock(side_effect=[Link(link="http://some-other.com", slug="collide"), None])
    
    created_link = Link(link=str(dto.link), slug="unique")
    mock_repo.create_from_dto = AsyncMock(return_value=created_link)
    mock_repo.add = AsyncMock()

    result_url = await link_service.generate_link(dto)

    assert mock_repo.get_by_slug.call_count == 2
    mock_repo.add.assert_called_once_with(created_link)
    mock_repo.session.commit.assert_called_once()
    assert result_url == "http://test.com/unique"
