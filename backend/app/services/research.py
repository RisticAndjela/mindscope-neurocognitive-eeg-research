from sqlalchemy.ext.asyncio import AsyncSession

from app.models.research import BlogPost, ResearchProject
from app.repositories.research import blog_post_repo, research_project_repo
from app.utils.slugs import make_slug


async def create_research_project(session: AsyncSession, payload) -> ResearchProject:
    data = payload.model_dump()
    data["slug"] = data.get("slug") or make_slug(data["title"])
    return await research_project_repo.create(session, data)


async def create_blog_post(session: AsyncSession, payload) -> BlogPost:
    data = payload.model_dump()
    data["slug"] = data.get("slug") or make_slug(data["title"])
    return await blog_post_repo.create(session, data)
