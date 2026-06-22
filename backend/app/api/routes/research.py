import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, get_current_user, require_research_user
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
from app.services.research import create_blog_post, create_research_project, prepare_blog_post_update

router = APIRouter()


async def get_or_404(repo, session: AsyncSession, item_id: uuid.UUID):
    item = await repo.get(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/projects", response_model=ResearchProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ResearchProjectCreate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    return await create_research_project(session, payload)


@router.get("/projects", response_model=list[ResearchProjectRead])
async def list_projects(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db_session),
):
    return await research_project_repo.list(session, limit, offset)


@router.get("/projects/slug/{slug}", response_model=ResearchProjectRead)
async def get_project_by_slug(slug: str, session: AsyncSession = Depends(get_db_session)):
    project = await research_project_repo.get_by_slug(session, slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return project


@router.get("/projects/{project_id}", response_model=ResearchProjectRead)
async def get_project(project_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    return await get_or_404(research_project_repo, session, project_id)


@router.patch("/projects/{project_id}", response_model=ResearchProjectRead)
async def update_project(
    project_id: uuid.UUID,
    payload: ResearchProjectUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(research_project_repo, session, project_id)
    return await research_project_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(research_project_repo, session, project_id)
    await research_project_repo.delete(session, item)


@router.post("/blog-posts", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: BlogPostCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    return await create_blog_post(session, payload, current_user)


@router.get("/blog-posts", response_model=list[BlogPostRead])
async def list_posts(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await blog_post_repo.list_public(session, limit, offset)


@router.get("/blog-posts/mine", response_model=list[BlogPostRead])
async def list_my_posts(
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    return await blog_post_repo.list_for_author(session, current_user.id, limit, offset)


@router.get("/blog-posts/mine/{post_id}", response_model=BlogPostRead)
async def get_my_post(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    post = await blog_post_repo.get_for_author(session, post_id, current_user.id)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return post


@router.get("/blog-posts/slug/{slug}", response_model=BlogPostRead)
async def get_post_by_slug(slug: str, session: AsyncSession = Depends(get_db_session)):
    post = await blog_post_repo.get_public_by_slug(session, slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return post


@router.get("/blog-posts/{post_id}", response_model=BlogPostRead)
async def get_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    post = await blog_post_repo.get_public(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return post


@router.patch("/blog-posts/{post_id}", response_model=BlogPostRead)
async def update_post(
    post_id: uuid.UUID,
    payload: BlogPostUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    item = await blog_post_repo.get_for_author(session, post_id, current_user.id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return await blog_post_repo.update(session, item, prepare_blog_post_update(payload, item))


@router.post("/blog-posts/{post_id}/publish", response_model=BlogPostRead)
async def publish_post(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    item = await blog_post_repo.get_for_author(session, post_id, current_user.id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return await blog_post_repo.update(
        session,
        item,
        prepare_blog_post_update(
            BlogPostUpdate(status="published", visibility="public"),
            item,
        ),
    )


@router.post("/blog-posts/{post_id}/visibility", response_model=BlogPostRead)
async def set_post_visibility(
    post_id: uuid.UUID,
    payload: BlogPostUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    item = await blog_post_repo.get_for_author(session, post_id, current_user.id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return await blog_post_repo.update(session, item, prepare_blog_post_update(payload, item))


@router.delete("/blog-posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(require_research_user),
):
    item = await blog_post_repo.get_for_author(session, post_id, current_user.id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await blog_post_repo.delete(session, item)


@router.post("/paper-notes", response_model=PaperNoteRead, status_code=status.HTTP_201_CREATED)
async def create_paper_note(
    payload: PaperNoteCreate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    return await paper_note_repo.create(session, payload.model_dump())


@router.get("/paper-notes", response_model=list[PaperNoteRead])
async def list_paper_notes(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await paper_note_repo.list(session, limit, offset)


@router.patch("/paper-notes/{note_id}", response_model=PaperNoteRead)
async def update_paper_note(
    note_id: uuid.UUID,
    payload: PaperNoteUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(paper_note_repo, session, note_id)
    return await paper_note_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/paper-notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper_note(
    note_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(paper_note_repo, session, note_id)
    await paper_note_repo.delete(session, item)


@router.post("/datasets", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    payload: DatasetCreate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    return await dataset_repo.create(session, payload.model_dump())


@router.get("/datasets", response_model=list[DatasetRead])
async def list_datasets(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await dataset_repo.list(session, limit, offset)


@router.patch("/datasets/{dataset_id}", response_model=DatasetRead)
async def update_dataset(
    dataset_id: uuid.UUID,
    payload: DatasetUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(dataset_repo, session, dataset_id)
    return await dataset_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/datasets/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(dataset_repo, session, dataset_id)
    await dataset_repo.delete(session, item)


@router.post("/experiments", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    payload: ExperimentCreate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    return await experiment_repo.create(session, payload.model_dump())


@router.get("/experiments", response_model=list[ExperimentRead])
async def list_experiments(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await experiment_repo.list(session, limit, offset)


@router.patch("/experiments/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(
    experiment_id: uuid.UUID,
    payload: ExperimentUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(experiment_repo, session, experiment_id)
    return await experiment_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/experiments/{experiment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiment(
    experiment_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(experiment_repo, session, experiment_id)
    await experiment_repo.delete(session, item)


@router.post("/model-runs", response_model=ModelRunRead, status_code=status.HTTP_201_CREATED)
async def create_model_run(
    payload: ModelRunCreate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    return await model_run_repo.create(session, payload.model_dump())


@router.get("/model-runs", response_model=list[ModelRunRead])
async def list_model_runs(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db_session)):
    return await model_run_repo.list(session, limit, offset)


@router.patch("/model-runs/{run_id}", response_model=ModelRunRead)
async def update_model_run(
    run_id: uuid.UUID,
    payload: ModelRunUpdate,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(model_run_repo, session, run_id)
    return await model_run_repo.update(session, item, payload.model_dump(exclude_unset=True))


@router.delete("/model-runs/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model_run(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    _: CurrentUser = Depends(require_research_user),
):
    item = await get_or_404(model_run_repo, session, run_id)
    await model_run_repo.delete(session, item)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
    }
