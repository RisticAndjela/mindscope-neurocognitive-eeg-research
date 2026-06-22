import unittest
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

from app.api.routes.research import publish_post
from app.core.dependencies import CurrentUser
from app.models.enums import BlogVisibility, PublicationStatus


class PublishPostRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_publish_returns_404_when_post_does_not_exist(self):
        current_user = CurrentUser(
            id=uuid.uuid4(),
            auth_user_id=uuid.uuid4(),
            profile_id=uuid.uuid4(),
            email="researcher@example.com",
            role="research",
            claims={},
        )
        session = AsyncMock()

        with patch("app.api.routes.research.blog_post_repo.get", new=AsyncMock(return_value=None)):
            with self.assertRaises(HTTPException) as exc_info:
                await publish_post(uuid.uuid4(), session=session, current_user=current_user)

        self.assertEqual(exc_info.exception.status_code, 404)
        self.assertEqual(exc_info.exception.detail, "Blog post not found")

    async def test_publish_returns_403_for_non_owner(self):
        post_id = uuid.uuid4()
        current_user = CurrentUser(
            id=uuid.uuid4(),
            auth_user_id=uuid.uuid4(),
            profile_id=uuid.uuid4(),
            email="researcher@example.com",
            role="research",
            claims={},
        )
        session = AsyncMock()
        post = type(
            "BlogPostStub",
            (),
            {
                "id": post_id,
                "author_id": uuid.uuid4(),
                "status": PublicationStatus.draft,
                "visibility": BlogVisibility.private,
                "published_at": None,
            },
        )()

        with patch("app.api.routes.research.blog_post_repo.get", new=AsyncMock(return_value=post)):
            with self.assertRaises(HTTPException) as exc_info:
                await publish_post(post_id, session=session, current_user=current_user)

        self.assertEqual(exc_info.exception.status_code, 403)

    async def test_publish_updates_owner_post_idempotently(self):
        author_id = uuid.uuid4()
        post_id = uuid.uuid4()
        published_at = datetime(2026, 6, 22, 12, 0, tzinfo=timezone.utc)
        current_user = CurrentUser(
            id=author_id,
            auth_user_id=author_id,
            profile_id=author_id,
            email="researcher@example.com",
            role="research",
            claims={},
        )
        session = AsyncMock()
        post = type(
            "BlogPostStub",
            (),
            {
                "id": post_id,
                "author_id": author_id,
                "title": "Existing published post",
                "status": PublicationStatus.published,
                "visibility": BlogVisibility.public,
                "published_at": published_at,
            },
        )()

        async def update_stub(_session, item, data):
            for key, value in data.items():
                setattr(item, key, value)
            return item

        with patch("app.api.routes.research.blog_post_repo.get", new=AsyncMock(return_value=post)):
            with patch("app.api.routes.research.blog_post_repo.update", new=AsyncMock(side_effect=update_stub)):
                updated_post = await publish_post(post_id, session=session, current_user=current_user)

        self.assertIs(updated_post, post)
        self.assertEqual(updated_post.status, PublicationStatus.published)
        self.assertEqual(updated_post.visibility, BlogVisibility.public)
        self.assertEqual(updated_post.published_at, published_at)


if __name__ == "__main__":
    unittest.main()
