import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import BlogVisibility, DatasetStatus, ExperimentStatus, PublicationStatus, ResearchStatus, TaskType


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    email: Mapped[str | None] = mapped_column(Text, unique=True)
    full_name: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(32), nullable=False)


class ResearchProject(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "research_projects"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    research_question: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ResearchStatus] = mapped_column(
        Enum(ResearchStatus, name="research_status"),
        default=ResearchStatus.planned,
        nullable=False,
    )
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)

    datasets: Mapped[list["Dataset"]] = relationship(back_populates="project")
    experiments: Mapped[list["Experiment"]] = relationship(back_populates="project")
    paper_notes: Mapped[list["PaperNote"]] = relationship(back_populates="project")
    blog_posts: Mapped[list["BlogPost"]] = relationship(back_populates="project")


class BlogPost(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "blog_posts"

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PublicationStatus] = mapped_column(
        Enum(PublicationStatus, name="publication_status"),
        default=PublicationStatus.draft,
        nullable=False,
    )
    visibility: Mapped[BlogVisibility] = mapped_column(
        Enum(BlogVisibility, name="blog_visibility"),
        default=BlogVisibility.public,
        nullable=False,
    )
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped[ResearchProject | None] = relationship(back_populates="blog_posts")


class PaperNote(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "paper_notes"

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    authors: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    year: Mapped[int | None]
    source_url: Mapped[str | None] = mapped_column(Text)
    doi: Mapped[str | None] = mapped_column(String(200))
    summary: Mapped[str | None] = mapped_column(Text)
    methods: Mapped[str | None] = mapped_column(Text)
    findings: Mapped[str | None] = mapped_column(Text)
    limitations: Mapped[str | None] = mapped_column(Text)
    relevance_to_mindscope: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)

    project: Mapped[ResearchProject | None] = relationship(back_populates="paper_notes")


class Dataset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "datasets"

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_url: Mapped[str | None] = mapped_column(Text)
    modality: Mapped[str | None] = mapped_column(String(80))  # EEG, fMRI, MEG, behavioral
    task_type: Mapped[TaskType | None] = mapped_column(Enum(TaskType, name="task_type"))
    license: Mapped[str | None] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus, name="dataset_status"),
        default=DatasetStatus.candidate,
        nullable=False,
    )
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)

    project: Mapped[ResearchProject | None] = relationship(back_populates="datasets")
    experiments: Mapped[list["Experiment"]] = relationship(back_populates="dataset")


class Experiment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "experiments"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    dataset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    hypothesis: Mapped[str | None] = mapped_column(Text)
    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType, name="task_type"), nullable=False)
    status: Mapped[ExperimentStatus] = mapped_column(
        Enum(ExperimentStatus, name="experiment_status"),
        default=ExperimentStatus.planned,
        nullable=False,
    )
    protocol_markdown: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)

    project: Mapped[ResearchProject] = relationship(back_populates="experiments")
    dataset: Mapped[Dataset | None] = relationship(back_populates="experiments")
    model_runs: Mapped[list["ModelRun"]] = relationship(back_populates="experiment")


class ModelRun(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "model_runs"

    experiment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiments.id", ondelete="CASCADE"),
        nullable=False,
    )
    model_name: Mapped[str] = mapped_column(String(160), nullable=False)
    model_family: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[ExperimentStatus] = mapped_column(
        Enum(ExperimentStatus, name="experiment_status"),
        default=ExperimentStatus.planned,
        nullable=False,
    )
    hyperparameters: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    artifacts: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    experiment: Mapped[Experiment] = relationship(back_populates="model_runs")
