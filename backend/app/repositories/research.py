from app.models.research import BlogPost, Dataset, Experiment, ModelRun, PaperNote, ResearchProject
from app.repositories.base import CRUDRepository

research_project_repo = CRUDRepository(ResearchProject)
blog_post_repo = CRUDRepository(BlogPost)
paper_note_repo = CRUDRepository(PaperNote)
dataset_repo = CRUDRepository(Dataset)
experiment_repo = CRUDRepository(Experiment)
model_run_repo = CRUDRepository(ModelRun)
