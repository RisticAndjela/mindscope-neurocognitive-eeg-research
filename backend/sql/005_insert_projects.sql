-- supabase/migrations/20260622_seed_research_projects.sql

insert into research_projects
  (title, slug, summary, research_question, status, tags)
values
  (
    'EEG Signal Processing Pipeline',
    'eeg-signal-processing-pipeline',
    'A pipeline for loading, cleaning, preprocessing, and preparing EEG recordings for later analysis and modeling.',
    'How can raw EEG recordings be transformed into clean and structured data suitable for neurocognitive research?',
    'planned',
    array['eeg', 'signal-processing', 'preprocessing', 'pipeline']
  ),
  (
    'EEG Artifact Detection',
    'eeg-artifact-detection',
    'Detection and handling of common EEG artifacts such as eye blinks, eye movement, muscle noise, and unstable channels.',
    'Which artifact detection methods are most useful for improving EEG data quality in cognitive experiments?',
    'planned',
    array['eeg', 'artifacts', 'noise-detection', 'preprocessing']
  ),
  (
    'Motor Imagery EEG Research',
    'motor-imagery-eeg-research',
    'A research module focused on motor imagery tasks and EEG patterns related to imagined movement.',
    'Can EEG patterns distinguish between different motor imagery tasks with useful accuracy?',
    'planned',
    array['eeg', 'motor-imagery', 'bci', 'classification']
  ),
  (
    'Working Memory EEG Research',
    'working-memory-eeg-research',
    'A research module focused on working memory tasks and their relationship with EEG activity.',
    'How do EEG features change during working memory tasks of different cognitive load levels?',
    'planned',
    array['eeg', 'working-memory', 'cognition', 'cognitive-load']
  ),
  (
    'Attention and Focus EEG Research',
    'attention-focus-eeg-research',
    'A research module focused on attention, focus, reaction time, and EEG markers of attentional state.',
    'Can EEG features be used to estimate changes in attention and focus during cognitive tasks?',
    'planned',
    array['eeg', 'attention', 'focus', 'reaction-time']
  ),
  (
    'Sleep and EEG State Analysis',
    'sleep-eeg-state-analysis',
    'A research module focused on sleep-related EEG patterns, sleep stages, and state transitions.',
    'Which EEG features are most relevant for identifying sleep-related brain states?',
    'planned',
    array['eeg', 'sleep', 'brain-states', 'state-analysis']
  ),
  (
    'Dream Research and EEG Patterns',
    'dream-research-eeg-patterns',
    'An exploratory module focused on the relationship between dreaming, sleep phases, and EEG activity.',
    'Can EEG patterns provide useful indicators related to dreaming or dream-associated sleep states?',
    'planned',
    array['eeg', 'dream-research', 'sleep', 'exploratory']
  ),
  (
    'EEG Feature Extraction',
    'eeg-feature-extraction',
    'Extraction of meaningful EEG features such as frequency band power, asymmetry, entropy, and statistical signal measures.',
    'Which EEG-derived features are most useful for neurocognitive analysis and machine learning?',
    'planned',
    array['eeg', 'features', 'band-power', 'machine-learning']
  ),
  (
    'Neurocognitive Dataset Review',
    'neurocognitive-dataset-review',
    'A structured review of publicly available EEG and neurocognitive datasets suitable for experiments.',
    'Which public EEG datasets are suitable for MindScope research experiments and why?',
    'planned',
    array['datasets', 'literature-review', 'eeg', 'open-data']
  ),
  (
    'Research Paper Knowledge Base',
    'research-paper-knowledge-base',
    'A curated knowledge base of scientific papers, methods, findings, limitations, and relevance to MindScope.',
    'How can relevant neuroscience and EEG research be organized into a useful project-level knowledge base?',
    'planned',
    array['papers', 'literature-review', 'knowledge-base', 'research']
  ),
  (
    'EEG Experiment Tracking',
    'eeg-experiment-tracking',
    'A system for defining experiments, linking datasets, tracking hypotheses, protocols, model runs, and results.',
    'How can EEG experiments be tracked in a reproducible and structured way?',
    'planned',
    array['experiments', 'reproducibility', 'model-runs', 'research-workflow']
  ),
  (
    'MindScope Research Blog',
    'mindscope-research-blog',
    'A blog section for publishing research explanations, paper summaries, experiment updates, and educational neuroscience content.',
    'How can complex EEG and neurocognitive research be explained clearly through public-facing articles?',
    'planned',
    array['blog', 'science-communication', 'education', 'research']
  )
on conflict (slug) do update set
  title = excluded.title,
  summary = excluded.summary,
  research_question = excluded.research_question,
  status = excluded.status,
  tags = excluded.tags,
  updated_at = now();