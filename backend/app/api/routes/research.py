import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.research import (
    blog_post_repo,
    dataset_repo,
    experiment_repo,
    model_run_repo,
    paper_note_repo,
    research_project_repo,
)
from app.schemas.research import (
    BlogPostCreate,
    BlogPostRead,
    BlogPostUpdate,
    DatasetCreate,
    DatasetRead,
    DatasetUpdate,
    ExperimentCreate,
    ExperimentRead,
    ExperimentUpdate,
    ModelRunCreate,
    ModelRunRead,
    ModelRunUpdate,
    PaperNoteCreate,
    PaperNoteRead,
    PaperNoteUpdate,
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchProjectUpdate,
)
from app.services.research import create_blog_post, create_research_project

router = APIRouter()


async def get_or_404(repo, session: AsyncSession, item_id: uuid.UUID):
    item = await repo.get(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/projects", response_model=ResearchProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ResearchProjectCreate, session: AsyncSession = Depends(get_db_session)):
    return await create_research_project(session, payload)


@router.get("/projects", response_model=list[ResearchProjectRead])
async def list_projects(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db_session),
):
    return await research_project_repo.list(session, limit, offset)


@router.get("/projects/{project_id}", response_model=ResearchProjectRead)
async def get_project(project_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    return await get_or_404(research_project_repo, session, project_id)


@router.patch("/projects/{project_id}", response_model=ResearchProjectRead)
async def update_project(project_id: uuid.UUID, payload: ResearchProjectUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(research_project_repo, session, project_id)
    return await research_project_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(research_project_repo, session, project_id)
    await research_project_repo.delete(session, item)


@router.post("/blog-posts", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
async def create_post(payload: BlogPostCreate, session: AsyncSession = Depends(get_db_session)):
    return await create_blog_post(session, payload)


@router.get("/blog-posts", response_model=list[BlogPostRead])
async def list_posts(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await blog_post_repo.list(session, limit, offset)


@router.get("/blog-posts/{post_id}", response_model=BlogPostRead)
async def get_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    return await get_or_404(blog_post_repo, session, post_id)


@router.patch("/blog-posts/{post_id}", response_model=BlogPostRead)
async def update_post(post_id: uuid.UUID, payload: BlogPostUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(blog_post_repo, session, post_id)
    return await blog_post_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/blog-posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(blog_post_repo, session, post_id)
    await blog_post_repo.delete(session, item)


@router.post("/paper-notes", response_model=PaperNoteRead, status_code=status.HTTP_201_CREATED)
async def create_paper_note(payload: PaperNoteCreate, session: AsyncSession = Depends(get_db_session)):
    return await paper_note_repo.create(session, payload.model_dump())


@router.get("/paper-notes", response_model=list[PaperNoteRead])
async def list_paper_notes(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await paper_note_repo.list(session, limit, offset)


@router.patch("/paper-notes/{note_id}", response_model=PaperNoteRead)
async def update_paper_note(note_id: uuid.UUID, payload: PaperNoteUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(paper_note_repo, session, note_id)
    return await paper_note_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/paper-notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper_note(note_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(paper_note_repo, session, note_id)
    await paper_note_repo.delete(session, item)


@router.post("/datasets", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def create_dataset(payload: DatasetCreate, session: AsyncSession = Depends(get_db_session)):
    return await dataset_repo.create(session, payload.model_dump())


@router.get("/datasets", response_model=list[DatasetRead])
async def list_datasets(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await dataset_repo.list(session, limit, offset)


@router.patch("/datasets/{dataset_id}", response_model=DatasetRead)
async def update_dataset(dataset_id: uuid.UUID, payload: DatasetUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(dataset_repo, session, dataset_id)
    return await dataset_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/datasets/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(dataset_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(dataset_repo, session, dataset_id)
    await dataset_repo.delete(session, item)


@router.post("/experiments", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
async def create_experiment(payload: ExperimentCreate, session: AsyncSession = Depends(get_db_session)):
    return await experiment_repo.create(session, payload.model_dump())


@router.get("/experiments", response_model=list[ExperimentRead])
async def list_experiments(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await experiment_repo.list(session, limit, offset)


@router.patch("/experiments/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(experiment_id: uuid.UUID, payload: ExperimentUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(experiment_repo, session, experiment_id)
    return await experiment_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/experiments/{experiment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiment(experiment_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(experiment_repo, session, experiment_id)
    await experiment_repo.delete(session, item)


@router.post("/model-runs", response_model=ModelRunRead, status_code=status.HTTP_201_CREATED)
async def create_model_run(payload: ModelRunCreate, session: AsyncSession = Depends(get_db_session)):
    return await model_run_repo.create(session, payload.model_dump())


@router.get("/model-runs", response_model=list[ModelRunRead])
async def list_model_runs(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await model_run_repo.list(session, limit, offset)


@router.patch("/model-runs/{run_id}", response_model=ModelRunRead)
async def update_model_run(run_id: uuid.UUID, payload: ModelRunUpdate, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(model_run_repo, session, run_id)
    return await model_run_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/model-runs/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model_run(run_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    item = await get_or_404(model_run_repo, session, run_id)
    await model_run_repo.delete(session, item)
