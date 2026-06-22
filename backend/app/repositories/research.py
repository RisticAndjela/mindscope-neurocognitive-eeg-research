import uuid

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import BlogVisibility, PublicationStatus
from app.models.research import BlogPost, Dataset, Experiment, ModelRun, PaperNote, ResearchProject
from app.repositories.base import CRUDRepository


class BlogPostRepository(CRUDRepository[BlogPost, dict, dict]):
    async def list_public(self, session: AsyncSession, limit: int = 50, offset: int = 0) -> list[BlogPost]:
        result = await session.execute(
            select(BlogPost)
            .where(
                and_(
                    BlogPost.status == PublicationStatus.published,
                    BlogPost.visibility == BlogVisibility.public,
                )
            )
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_public(self, session: AsyncSession, post_id: uuid.UUID) -> BlogPost | None:
        result = await session.execute(
            select(BlogPost).where(
                and_(
                    BlogPost.id == post_id,
                    BlogPost.status == PublicationStatus.published,
                    BlogPost.visibility == BlogVisibility.public,
                )
            )
        )
        return result.scalar_one_or_none()

    async def list_for_author(self, session: AsyncSession, author_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[BlogPost]:
        result = await session.execute(
            select(BlogPost)
            .where(BlogPost.author_id == author_id)
            .order_by(BlogPost.updated_at.desc(), BlogPost.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_for_author(self, session: AsyncSession, post_id: uuid.UUID, author_id: uuid.UUID) -> BlogPost | None:
        result = await session.execute(
            select(BlogPost).where(and_(BlogPost.id == post_id, BlogPost.author_id == author_id))
        )
        return result.scalar_one_or_none()

    async def get_visible_to_author(self, session: AsyncSession, post_id: uuid.UUID, author_id: uuid.UUID) -> BlogPost | None:
        result = await session.execute(
            select(BlogPost).where(
                and_(
                    BlogPost.id == post_id,
                    or_(
                        BlogPost.author_id == author_id,
                        and_(
                            BlogPost.status == PublicationStatus.published,
                            BlogPost.visibility == BlogVisibility.public,
                        ),
                    ),
                )
            )
        )
        return result.scalar_one_or_none()

research_project_repo = CRUDRepository(ResearchProject)
blog_post_repo = BlogPostRepository(BlogPost)
paper_note_repo = CRUDRepository(PaperNote)
dataset_repo = CRUDRepository(Dataset)
experiment_repo = CRUDRepository(Experiment)
model_run_repo = CRUDRepository(ModelRun)
