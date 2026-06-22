import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

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

export type BlogPost = {
  id: string;
  project_id?: string | null;
  title: string;
  slug: string;
  excerpt?: string | null;
  content_markdown: string;
  status: 'draft' | 'published' | 'archived';
  tags: string[];
  created_at: string;
  updated_at: string;
};

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = 'http://127.0.0.1:8000/api/v1/research';

  constructor(private readonly http: HttpClient) {}

  getProjects() { return this.http.get<ResearchProject[]>(`${this.baseUrl}/projects`); }
  getProject(id: string) { return this.http.get<ResearchProject>(`${this.baseUrl}/projects/${id}`); }
  getBlogPosts() { return this.http.get<BlogPost[]>(`${this.baseUrl}/blog-posts`); }
  getBlogPost(id: string) { return this.http.get<BlogPost>(`${this.baseUrl}/blog-posts/${id}`); }
}
