# MindScope Backend Architecture

The backend is intentionally focused on research documentation and project tracking.

## Main domains

### Blog
Long-form public or private progress posts.

### Research Projects
Umbrella research areas such as EEG decoding, working memory modeling, attention modeling, or dream-state research.

### Paper Notes
Structured notes for papers, including summary, methods, findings, limitations, and relevance.

### Datasets
Metadata about public datasets, including source URL, modality, task type, license, and status.

### Experiments
Tracked research experiments connected to a project and optionally to a dataset.

### Model Runs
Specific model executions connected to an experiment, including model type, status, hyperparameters, and metrics.

## Architecture

```txt
app/api/routes        HTTP routes
app/models           SQLAlchemy database models
app/schemas          Pydantic request/response schemas
app/repositories     Database access layer
app/services         Business logic
app/db               Database session setup
app/core             Settings/configuration
sql                  Supabase/Postgres SQL scripts
```
