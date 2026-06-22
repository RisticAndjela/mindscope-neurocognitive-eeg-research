import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import { BlogPost, BlogPostCreate, BlogPostStatus, BlogPostUpdate, BlogPostVisibility, ResearchProject } from '../../../core/types/blog';
import { ResearchForbiddenStateComponent } from '../../../shared/research-forbidden-state/research-forbidden-state.component';

@Component({
  selector: 'ms-research-blog-editor',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink, ResearchForbiddenStateComponent],
  templateUrl: './research-blog-editor.component.html',
  styleUrl: './research-blog-editor.component.scss'
})
export class ResearchBlogEditorComponent {
  private readonly fb = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(ApiService);
  private readonly authService = inject(AuthService);

  private postId = this.route.snapshot.paramMap.get('id');

  protected readonly loading = signal(true);
  protected readonly saving = signal(false);
  protected readonly deleting = signal(false);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly successMessage = signal<string | null>(null);
  protected readonly currentPost = signal<BlogPost | null>(null);
  protected readonly projects = signal<ResearchProject[]>([]);
  protected readonly isResearcher = computed(() => this.authService.isResearcher());
  protected readonly isEditMode = computed(() => !!this.postId);
  protected readonly saveLabel = computed(() => (this.isEditMode() ? 'Save changes' : 'Create draft'));
  protected readonly wordCount = computed(() => {
    const content = this.form.controls.content_markdown.value.trim();
    return content ? content.split(/\s+/).length : 0;
  });

  protected readonly form = this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.maxLength(200)]],
    slug: [''],
    excerpt: [''],
    content_markdown: ['', [Validators.required]],
    status: this.fb.nonNullable.control<BlogPostStatus>('draft'),
    visibility: this.fb.nonNullable.control<BlogPostVisibility>('public'),
    tags: [''],
    project_id: ['']
  });

  constructor() {
    void this.initialize();
  }

  protected async save() {
    await this.persist();
  }

  protected async publishPublicly() {
    if (this.isEditMode() && this.currentPost()) {
      await this.runAction(async () => {
        const post = await firstValueFrom(this.api.publishBlogPost(this.currentPost()!.id));
        this.syncForm(post);
        this.successMessage.set('Published to the public MindScope journal.');
      });
      return;
    }

    await this.persist({ status: 'published', visibility: 'public' });
  }

  protected async markPrivate() {
    const nextStatus = this.form.controls.status.value === 'draft' ? 'draft' : 'published';
    await this.persist({ status: nextStatus, visibility: 'private' });
  }

  protected async archive() {
    if (!this.currentPost()) {
      return;
    }

    await this.runAction(async () => {
      const post = await firstValueFrom(this.api.archiveBlogPost(this.currentPost()!.id));
      this.syncForm(post);
      this.successMessage.set('Post archived in the research workspace.');
    });
  }

  protected async deletePost() {
    if (!this.currentPost()) {
      return;
    }

    const confirmed = window.confirm('Delete this post permanently?');
    if (!confirmed) {
      return;
    }

    this.deleting.set(true);
    this.errorMessage.set(null);
    this.successMessage.set(null);

    try {
      await firstValueFrom(this.api.deleteBlogPost(this.currentPost()!.id));
      await this.router.navigateByUrl('/research/blog');
    } catch (error) {
      this.errorMessage.set(this.toMessage(error, 'Unable to delete this post.'));
    } finally {
      this.deleting.set(false);
    }
  }

  private async initialize() {
    if (!this.authService.isResearcher()) {
      this.loading.set(false);
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    try {
      this.projects.set(await firstValueFrom(this.api.getProjects()));

      if (this.postId) {
        this.syncForm(await firstValueFrom(this.api.getMyBlogPost(this.postId)));
      }
    } catch (error) {
      this.errorMessage.set(this.toMessage(error, 'Unable to load the research editor.'));
    } finally {
      this.loading.set(false);
    }
  }

  private async persist(overrides?: BlogPostUpdate) {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.errorMessage.set('Add a title and some markdown content before saving.');
      return;
    }

    await this.runAction(async () => {
      const payload = this.buildPayload(overrides);
      const post = this.currentPost()
        ? await firstValueFrom(this.api.updateBlogPost(this.currentPost()!.id, payload))
        : await firstValueFrom(this.api.createBlogPost(payload as BlogPostCreate));

      this.syncForm(post);

      if (!this.isEditMode()) {
        this.postId = post.id;
        await this.router.navigate(['/research/blog', post.id, 'edit'], { replaceUrl: true });
      }

      this.successMessage.set(
        payload.status === 'published'
          ? `Saved and ${payload.visibility === 'private' ? 'kept private inside the lab' : 'published publicly'}.`
          : 'Draft saved in your research notebook.'
      );
    });
  }

  private buildPayload(overrides?: BlogPostUpdate): BlogPostCreate {
    const tags = this.form.controls.tags.value
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);

    return {
      title: this.form.controls.title.value.trim(),
      slug: this.form.controls.slug.value.trim() || null,
      excerpt: this.form.controls.excerpt.value.trim() || null,
      content_markdown: this.form.controls.content_markdown.value,
      status: this.form.controls.status.value,
      visibility: this.form.controls.visibility.value,
      project_id: this.form.controls.project_id.value || null,
      tags,
      ...overrides
    };
  }

  private syncForm(post: BlogPost) {
    this.currentPost.set(post);
    this.form.setValue({
      title: post.title,
      slug: post.slug,
      excerpt: post.excerpt ?? '',
      content_markdown: post.content_markdown,
      status: post.status,
      visibility: post.visibility,
      tags: post.tags.join(', '),
      project_id: post.project_id ?? ''
    });
  }

  private async runAction(action: () => Promise<void>) {
    this.saving.set(true);
    this.errorMessage.set(null);
    this.successMessage.set(null);

    try {
      await action();
    } catch (error) {
      this.errorMessage.set(this.toMessage(error, 'Unable to save this post.'));
    } finally {
      this.saving.set(false);
    }
  }

  private toMessage(error: unknown, fallback: string) {
    if (error && typeof error === 'object' && 'message' in error && typeof error.message === 'string') {
      return error.message;
    }

    return fallback;
  }
}
