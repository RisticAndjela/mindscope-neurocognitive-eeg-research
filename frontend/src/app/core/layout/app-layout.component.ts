import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

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
        </nav>
        <a routerLink="/login" class="login-link">Login</a>
      </header>
      <main><ng-content /></main>
    </div>
  `,
  styleUrl: './app-layout.component.scss'
})
export class AppLayoutComponent {}
