import { DatePipe } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';
import { ApiService } from '../../core/services/api.service';
import { BlogPost } from '../../core/types/blog';
import { ResearchForbiddenStateComponent } from '../../shared/research-forbidden-state/research-forbidden-state.component';

@Component({
  selector: 'ms-research-blog',
  standalone: true,
  imports: [DatePipe, RouterLink, ResearchForbiddenStateComponent],
  templateUrl: './research-blog.component.html',
  styleUrl: './research-blog.component.scss'
})
export class ResearchBlogComponent {
  private readonly api = inject(ApiService);
  private readonly authService = inject(AuthService);

  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly posts = signal<BlogPost[]>([]);
  protected readonly isResearcher = computed(() => this.authService.isResearcher());
  protected readonly grouped = computed(() => {
    const posts = this.posts();
    return {
      drafts: posts.filter((post) => post.status === 'draft'),
      privatePosts: posts.filter((post) => post.visibility === 'private' && post.status !== 'draft'),
      published: posts.filter((post) => post.status === 'published' && post.visibility === 'public'),
      archived: posts.filter((post) => post.status === 'archived')
    };
  });
  protected readonly totalCount = computed(() => this.posts().length);

  constructor() {
    void this.loadPosts();
  }

  protected trackById(_: number, post: BlogPost) {
    return post.id;
  }

  protected async loadPosts() {
    if (!this.authService.isResearcher()) {
      this.loading.set(false);
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    try {
      this.posts.set(await firstValueFrom(this.api.listMyBlogPosts()));
    } catch (error) {
      this.errorMessage.set(this.toMessage(error, 'Unable to load your research posts.'));
    } finally {
      this.loading.set(false);
    }
  }

  private toMessage(error: unknown, fallback: string) {
    if (error && typeof error === 'object' && 'message' in error && typeof error.message === 'string') {
      return error.message;
    }

    return fallback;
  }
}
