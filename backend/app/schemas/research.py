import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import BlogVisibility, DatasetStatus, ExperimentStatus, PublicationStatus, ResearchStatus, TaskType


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ResearchProjectBase(BaseModel):
    title: str
    summary: str | None = None
    research_question: str | None = None
    status: ResearchStatus = ResearchStatus.planned
    tags: list[str] = Field(default_factory=list)


class ResearchProjectCreate(ResearchProjectBase):
    slug: str | None = None


class ResearchProjectUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    research_question: str | None = None
    status: ResearchStatus | None = None
    tags: list[str] | None = None


class ResearchProjectRead(ResearchProjectBase, ORMModel):
    id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: datetime


class BlogPostBase(BaseModel):
    project_id: uuid.UUID | None = None
    title: str
    slug: str | None = None
    excerpt: str | None = None
    content_markdown: str
    status: PublicationStatus = PublicationStatus.draft
    visibility: BlogVisibility = BlogVisibility.public
    tags: list[str] = Field(default_factory=list)


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    project_id: uuid.UUID | None = None
    title: str | None = None
    slug: str | None = None
    excerpt: str | None = None
    content_markdown: str | None = None
    status: PublicationStatus | None = None
    visibility: BlogVisibility | None = None
    tags: list[str] | None = None


class BlogPostRead(BlogPostBase, ORMModel):
    id: uuid.UUID
    slug: str
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None


class PaperNoteBase(BaseModel):
    project_id: uuid.UUID | None = None
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source_url: str | None = None
    doi: str | None = None
    summary: str | None = None
    methods: str | None = None
    findings: str | None = None
    limitations: str | None = None
    relevance_to_mindscope: str | None = None
    tags: list[str] = Field(default_factory=list)


class PaperNoteCreate(PaperNoteBase):
    pass


class PaperNoteUpdate(BaseModel):
    project_id: uuid.UUID | None = None
    title: str | None = None
    authors: list[str] | None = None
    year: int | None = None
    source_url: str | None = None
    doi: str | None = None
    summary: str | None = None
    methods: str | None = None
    findings: str | None = None
    limitations: str | None = None
    relevance_to_mindscope: str | None = None
    tags: list[str] | None = None


class PaperNoteRead(PaperNoteBase, ORMModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DatasetBase(BaseModel):
    project_id: uuid.UUID | None = None
    name: str
    source_url: str | None = None
    modality: str | None = None
    task_type: TaskType | None = None
    license: str | None = None
    description: str | None = None
    status: DatasetStatus = DatasetStatus.candidate
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(BaseModel):
    project_id: uuid.UUID | None = None
    name: str | None = None
    source_url: str | None = None
    modality: str | None = None
    task_type: TaskType | None = None
    license: str | None = None
    description: str | None = None
    status: DatasetStatus | None = None
    metadata_json: dict[str, Any] | None = None
    tags: list[str] | None = None


class DatasetRead(DatasetBase, ORMModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ExperimentBase(BaseModel):
    project_id: uuid.UUID
    dataset_id: uuid.UUID | None = None
    title: str
    hypothesis: str | None = None
    task_type: TaskType
    status: ExperimentStatus = ExperimentStatus.planned
    protocol_markdown: str | None = None
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    dataset_id: uuid.UUID | None = None
    title: str | None = None
    hypothesis: str | None = None
    task_type: TaskType | None = None
    status: ExperimentStatus | None = None
    protocol_markdown: str | None = None
    notes: str | None = None
    tags: list[str] | None = None


class ExperimentRead(ExperimentBase, ORMModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ModelRunBase(BaseModel):
    experiment_id: uuid.UUID
    model_name: str
    model_family: str | None = None
    status: ExperimentStatus = ExperimentStatus.planned
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    artifacts: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class ModelRunCreate(ModelRunBase):
    pass


class ModelRunUpdate(BaseModel):
    model_name: str | None = None
    model_family: str | None = None
    status: ExperimentStatus | None = None
    hyperparameters: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    artifacts: dict[str, Any] | None = None
    notes: str | None = None


class ModelRunRead(ModelRunBase, ORMModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
