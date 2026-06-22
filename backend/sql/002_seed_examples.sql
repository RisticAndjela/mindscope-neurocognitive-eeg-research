insert into research_projects (title, slug, summary, research_question, status, tags)
values
(
  'Working Memory and Attention Bias',
  'working-memory-attention-bias',
  'Research track focused on how active memory representations influence attentional selection.',
  'Can active working-memory representations increase the probability of noticing related stimuli?',
  'active',
  array['working-memory', 'attention', 'cognitive-modeling']
)
on conflict (slug) do nothing;

insert into blog_posts (title, slug, excerpt, content_markdown, status, tags)
values
(
  'Starting MindScope',
  'starting-mindscope',
  'Initial notes on the MindScope research platform.',
  '# Starting MindScope\n\nThis post documents the first research direction: EEG decoding, working memory, and attention modeling.',
  'draft',
  array['mindscope', 'research-log']
)
on conflict (slug) do nothing;
