import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { guestGuard } from './core/guards/guest.guard';
import { researchGuard } from './core/guards/research.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent) },
  { path: 'projects', loadComponent: () => import('./features/projects/projects.component').then(m => m.ProjectsComponent) },
  { path: 'projects/:id', loadComponent: () => import('./features/projects/project-detail/project-detail.component').then(m => m.ProjectDetailComponent) },
  { path: 'blog', loadComponent: () => import('./features/blog/blog.component').then(m => m.BlogComponent) },
  { path: 'blog/:id', loadComponent: () => import('./features/blog/blog-detail/blog-detail.component').then(m => m.BlogDetailComponent) },
  { path: 'login', canActivate: [guestGuard], loadComponent: () => import('./features/login/login.component').then(m => m.LoginComponent) },
  { path: 'research-hub', canActivate: [authGuard, researchGuard], loadComponent: () => import('./features/research-hub/research-hub.component').then(m => m.ResearchHubComponent) },
  { path: '**', redirectTo: '' }
];
