export type ResearchProject = {
  id: string;
  title: string;
  slug: string;
  summary?: string | null;
  research_question?: string | null;
  status: 'planned' | 'active' | 'paused' | 'completed';
  tags: string[];
  created_at: string;
  updated_at: string;
};

export type BlogPostStatus = 'draft' | 'published' | 'archived';
export type BlogPostVisibility = 'public' | 'private';

export type BlogPost = {
  id: string;
  author_id: string;
  project_id?: string | null;
  title: string;
  slug: string;
  excerpt?: string | null;
  content_markdown: string;
  status: BlogPostStatus;
  visibility: BlogPostVisibility;
  tags: string[];
  created_at: string;
  updated_at: string;
  published_at?: string | null;
};

export type BlogPostCreate = {
  project_id?: string | null;
  title: string;
  slug?: string | null;
  excerpt?: string | null;
  content_markdown: string;
  status: BlogPostStatus;
  visibility: BlogPostVisibility;
  tags: string[];
};

export type BlogPostUpdate = Partial<BlogPostCreate>;
