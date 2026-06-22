import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, defer, from, switchMap, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { BlogPost, BlogPostCreate, BlogPostUpdate, ResearchProject } from '../types/blog';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);
  private readonly baseUrl = `${environment.backendApiBaseUrl}/research`;

  getProjects() {
    return this.http.get<ResearchProject[]>(`${this.baseUrl}/projects`);
  }

  getProject(id: string) {
    return this.http.get<ResearchProject>(`${this.baseUrl}/projects/${id}`);
  }

  getProjectBySlug(slug: string) {
    return this.http.get<ResearchProject>(`${this.baseUrl}/projects/slug/${slug}`);
  }

  listPublicBlogPosts() {
    return this.http.get<BlogPost[]>(`${this.baseUrl}/blog-posts`);
  }

  getPublicBlogPost(id: string) {
    return this.http.get<BlogPost>(`${this.baseUrl}/blog-posts/${id}`);
  }

  getPublicBlogPostBySlug(slug: string) {
    return this.http.get<BlogPost>(`${this.baseUrl}/blog-posts/slug/${slug}`);
  }

  listMyBlogPosts() {
    return this.withAuth((headers) => this.http.get<BlogPost[]>(`${this.baseUrl}/blog-posts/mine`, { headers }));
  }

  getMyBlogPost(id: string) {
    return this.withAuth((headers) => this.http.get<BlogPost>(`${this.baseUrl}/blog-posts/mine/${id}`, { headers }));
  }

  createBlogPost(payload: BlogPostCreate) {
    return this.withAuth((headers) => this.http.post<BlogPost>(`${this.baseUrl}/blog-posts`, payload, { headers }));
  }

  updateBlogPost(id: string, payload: BlogPostUpdate) {
    return this.withAuth((headers) => this.http.patch<BlogPost>(`${this.baseUrl}/blog-posts/${id}`, payload, { headers }));
  }

  publishBlogPost(id: string) {
    return this.withAuth((headers) => this.http.post<BlogPost>(`${this.baseUrl}/blog-posts/${id}/publish`, {}, { headers }));
  }

  setBlogPostVisibility(id: string, visibility: 'public' | 'private') {
    return this.withAuth((headers) =>
      this.http.post<BlogPost>(`${this.baseUrl}/blog-posts/${id}/visibility`, { visibility }, { headers })
    );
  }

  archiveBlogPost(id: string) {
    return this.updateBlogPost(id, { status: 'archived' });
  }

  deleteBlogPost(id: string) {
    return this.withAuth((headers) => this.http.delete<void>(`${this.baseUrl}/blog-posts/${id}`, { headers }));
  }

  private withAuth<T>(factory: (headers: HttpHeaders) => Observable<T>) {
    return defer(() =>
      from(this.authService.getAccessToken()).pipe(
        switchMap((token) => {
          if (!token) {
            return throwError(() => new Error('You must be logged in to manage research posts.'));
          }

          return from([factory(new HttpHeaders({ Authorization: `Bearer ${token}` }))]);
        }),
        switchMap((request) => request)
      )
    );
  }
}
