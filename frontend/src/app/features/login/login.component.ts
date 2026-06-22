import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService, type ProfileRole } from '../../core/services/auth.service';

@Component({
  selector: 'ms-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  protected readonly mode = signal<'login' | 'register'>('login');
  protected readonly authState = computed(() => ({
    user: this.authService.user(),
    profile: this.authService.profile(),
    isLoading: this.authService.isLoading(),
    isReady: this.authService.isReady(),
    isResearcher: this.authService.isResearcher(),
    authError: this.authService.authError()
  }));

  protected loginEmail = '';
  protected loginPassword = '';

  protected registerForm = {
    fullName: '',
    email: '',
    password: '',
    role: 'regular' as ProfileRole
  };

  protected errorMessage = '';
  protected successMessage = '';

  protected setMode(mode: 'login' | 'register') {
    this.mode.set(mode);
    this.errorMessage = '';
    this.successMessage = '';
  }

  protected async login() {
    this.errorMessage = '';
    this.successMessage = '';

    try {
      await this.authService.login(this.loginEmail, this.loginPassword);
      this.successMessage = 'You are now signed in.';
      await this.router.navigateByUrl(this.nextUrl());
    } catch (error) {
      this.errorMessage = this.toMessage(error, 'Login failed.');
    }
  }

  protected async register() {
    this.errorMessage = '';
    this.successMessage = '';

    try {
      await this.authService.register(this.registerForm);
      this.setMode('login');
      this.loginEmail = this.registerForm.email;
      this.loginPassword = '';
      this.successMessage =
        'Your account has been created. If email confirmation is enabled in Supabase, check your inbox before your first login.';
    } catch (error) {
      this.errorMessage = this.toMessage(error, 'Registration failed.');
    }
  }

  protected async logout() {
    this.errorMessage = '';
    this.successMessage = '';

    try {
      await this.authService.logout();
      this.successMessage = 'You are now signed out.';
    } catch (error) {
      this.errorMessage = this.toMessage(error, 'Logout failed.');
    }
  }

  private toMessage(error: unknown, fallback: string) {
    if (error && typeof error === 'object' && 'message' in error && typeof error.message === 'string') {
      return error.message;
    }

    return fallback;
  }

  private nextUrl() {
    return this.route.snapshot.queryParamMap.get('next') || (this.authService.isResearcher() ? '/research/blog' : '/');
  }
}
