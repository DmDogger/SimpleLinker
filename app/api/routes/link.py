from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse 

from app.core.dependencies.services.link_service import get_link_service
from app.core.models.dto.links import ShortLinkResponse, CreateShortLink
from app.core.services.link import LinkService

router = APIRouter()

@router.post('/', response_model=ShortLinkResponse, status_code=201)
async def create_short_link(
        data: CreateShortLink,
        link_service: LinkService = Depends(get_link_service)
):
    short = await link_service.generate_link(data)
    return ShortLinkResponse(
        link=data.link,
        link_with_slug=short
    )

@router.get('/{slug}', status_code=307)
async def go_to_link(
        slug: str,
        link_service: LinkService = Depends(get_link_service)
):
    original_url = await link_service.get_link_by_slug(slug)
    return RedirectResponse(url=original_url)


