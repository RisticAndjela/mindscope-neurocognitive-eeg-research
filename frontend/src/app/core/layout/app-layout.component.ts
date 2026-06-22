import { Component, computed, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'ms-app-layout',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <div class="app-shell">
      <header class="navbar">
        <a routerLink="/" class="brand"><span class="brand-mark">M</span><span class="brand-text">MindScope</span></a>
        <nav class="nav-links">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Home</a>
          <a routerLink="/projects" routerLinkActive="active">Projects</a>
          <a routerLink="/blog" routerLinkActive="active">Blog</a>
          @if (authState().isResearcher) {
            <a routerLink="/research/blog" routerLinkActive="active">Research Lab</a>
          }
        </nav>
        @if (authState().user) {
          <div class="auth-actions">
            <a [routerLink]="authState().isResearcher ? '/research/blog' : '/login'" class="login-link">
              {{ authState().profile?.full_name || authState().user?.email }}
            </a>
            <button class="logout-button" type="button" (click)="logout()">Logout</button>
          </div>
        } @else {
          <a routerLink="/login" class="login-link">Login</a>
        }
      </header>
      <main><ng-content /></main>
    </div>
  `,
  styleUrl: './app-layout.component.scss'
})
export class AppLayoutComponent {
  private readonly authService = inject(AuthService);

  protected readonly authState = computed(() => ({
    user: this.authService.user(),
    profile: this.authService.profile(),
    isResearcher: this.authService.isResearcher()
  }));

  protected async logout() {
    await this.authService.logout();
  }
}
