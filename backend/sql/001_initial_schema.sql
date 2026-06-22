create extension if not exists "pgcrypto";

do $$ begin
  create type research_status as enum ('planned', 'active', 'paused', 'completed');
exception when duplicate_object then null;
end $$;

do $$ begin
  create type publication_status as enum ('draft', 'published', 'archived');
exception when duplicate_object then null;
end $$;

do $$ begin
  create type dataset_status as enum ('candidate', 'approved', 'imported', 'rejected');
exception when duplicate_object then null;
end $$;

do $$ begin
  create type experiment_status as enum ('planned', 'running', 'completed', 'failed');
exception when duplicate_object then null;
end $$;

do $$ begin
  create type task_type as enum (
    'eeg_processing',
    'motor_imagery',
    'working_memory',
    'attention',
    'sleep',
    'dream_research',
    'literature_review'
  );
exception when duplicate_object then null;
end $$;

create table if not exists research_projects (
  id uuid primary key default gen_random_uuid(),
  title varchar(200) not null,
  slug varchar(220) not null unique,
  summary text,
  research_question text,
  status research_status not null default 'planned',
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists blog_posts (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references research_projects(id) on delete set null,
  title varchar(200) not null,
  slug varchar(220) not null unique,
  excerpt text,
  content_markdown text not null,
  status publication_status not null default 'draft',
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists paper_notes (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references research_projects(id) on delete set null,
  title varchar(300) not null,
  authors text[] not null default '{}',
  year integer,
  source_url text,
  doi varchar(200),
  summary text,
  methods text,
  findings text,
  limitations text,
  relevance_to_mindscope text,
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists datasets (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references research_projects(id) on delete set null,
  name varchar(200) not null,
  source_url text,
  modality varchar(80),
  task_type task_type,
  license varchar(120),
  description text,
  status dataset_status not null default 'candidate',
  metadata_json jsonb not null default '{}',
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists experiments (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references research_projects(id) on delete cascade,
  dataset_id uuid references datasets(id) on delete set null,
  title varchar(220) not null,
  hypothesis text,
  task_type task_type not null,
  status experiment_status not null default 'planned',
  protocol_markdown text,
  notes text,
  tags text[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists model_runs (
  id uuid primary key default gen_random_uuid(),
  experiment_id uuid not null references experiments(id) on delete cascade,
  model_name varchar(160) not null,
  model_family varchar(120),
  status experiment_status not null default 'planned',
  hyperparameters jsonb not null default '{}',
  metrics jsonb not null default '{}',
  artifacts jsonb not null default '{}',
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_blog_posts_project_id on blog_posts(project_id);
create index if not exists idx_paper_notes_project_id on paper_notes(project_id);
create index if not exists idx_datasets_project_id on datasets(project_id);
create index if not exists idx_experiments_project_id on experiments(project_id);
create index if not exists idx_experiments_dataset_id on experiments(dataset_id);
create index if not exists idx_model_runs_experiment_id on model_runs(experiment_id);
create index if not exists idx_blog_posts_tags on blog_posts using gin(tags);
create index if not exists idx_paper_notes_tags on paper_notes using gin(tags);
create index if not exists idx_datasets_tags on datasets using gin(tags);
