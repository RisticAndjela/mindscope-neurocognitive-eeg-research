import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")
CreateSchemaT = TypeVar("CreateSchemaT")
UpdateSchemaT = TypeVar("UpdateSchemaT")


class CRUDRepository(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model: type[ModelT]):
        self.model = model

    async def get(self, session: AsyncSession, item_id: uuid.UUID) -> ModelT | None:
        return await session.get(self.model, item_id)

    async def list(self, session: AsyncSession, limit: int = 50, offset: int = 0) -> list[ModelT]:
        result = await session.execute(
            select(self.model).order_by(self.model.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, data: dict) -> ModelT:
        item = self.model(**data)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def update(self, session: AsyncSession, item: ModelT, data: dict) -> ModelT:
        for key, value in data.items():
            setattr(item, key, value)
        await session.commit()
        await session.refresh(item)
        return item

    async def delete(self, session: AsyncSession, item: ModelT) -> None:
        await session.delete(item)
        await session.commit()
