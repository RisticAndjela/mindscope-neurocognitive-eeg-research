import enum


class PublicationStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class BlogVisibility(str, enum.Enum):
    public = "public"
    private = "private"


class ResearchStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    paused = "paused"
    completed = "completed"


class DatasetStatus(str, enum.Enum):
    candidate = "candidate"
    approved = "approved"
    imported = "imported"
    rejected = "rejected"


class ExperimentStatus(str, enum.Enum):
    planned = "planned"
    running = "running"
    completed = "completed"
    failed = "failed"


class TaskType(str, enum.Enum):
    eeg_processing = "eeg_processing"
    motor_imagery = "motor_imagery"
    working_memory = "working_memory"
    attention = "attention"
    sleep = "sleep"
    dream_research = "dream_research"
    literature_review = "literature_review"
