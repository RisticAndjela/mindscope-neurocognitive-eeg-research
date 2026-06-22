from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.models.enums import PublicationStatus
from app.models.research import BlogPost, ResearchProject
from app.repositories.research import blog_post_repo, research_project_repo
from app.utils.slugs import make_slug


async def create_research_project(session: AsyncSession, payload) -> ResearchProject:
    data = payload.model_dump()
    data["slug"] = data.get("slug") or make_slug(data["title"])
    return await research_project_repo.create(session, data)


def prepare_blog_post_create(payload) -> dict:
    data = payload.model_dump()
    data["slug"] = make_slug(data["slug"] or data["title"])
    data["published_at"] = datetime.now(timezone.utc) if data["status"] == PublicationStatus.published else None
    return data


def prepare_blog_post_update(payload, current_post: BlogPost) -> dict:
    data = payload.model_dump(exclude_unset=True)

    if "slug" in data:
        slug_source = data["slug"] or data.get("title") or current_post.title
        data["slug"] = make_slug(slug_source)

    next_status = data.get("status", current_post.status)
    if next_status == PublicationStatus.published and current_post.published_at is None:
        data["published_at"] = datetime.now(timezone.utc)

    return data


async def create_blog_post(session: AsyncSession, payload, author: CurrentUser) -> BlogPost:
    data = prepare_blog_post_create(payload)
    data["author_id"] = author.id
    return await blog_post_repo.create(session, data)
