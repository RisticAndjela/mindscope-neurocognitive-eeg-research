import { Injectable, computed, signal } from '@angular/core';
import { createClient, type AuthChangeEvent, type Session, type User } from '@supabase/supabase-js';
import { environment } from '../../../environments/environment';

export type ProfileRole = 'regular' | 'research';

export type Profile = {
  id: string;
  email: string | null;
  full_name: string | null;
  role: ProfileRole;
  created_at: string;
  updated_at: string;
};

export type RegisterPayload = {
  email: string;
  password: string;
  fullName: string;
  role: ProfileRole;
};

const supabase = createClient(environment.supabaseUrl, environment.supabaseAnonKey);
const isSupabaseConfigured =
  !!environment.supabaseUrl &&
  !!environment.supabaseAnonKey &&
  environment.supabaseUrl !== 'https://YOUR_PROJECT.supabase.co' &&
  environment.supabaseAnonKey !== 'YOUR_SUPABASE_ANON_KEY';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly initialized = signal(false);
  private readonly sessionState = signal<Session | null>(null);
  private readonly profileState = signal<Profile | null>(null);
  private readonly loadingState = signal(false);
  private readonly authErrorState = signal<string | null>(null);
  private initializationPromise: Promise<void> | null = null;

  readonly session = computed(() => this.sessionState());
  readonly user = computed<User | null>(() => this.sessionState()?.user ?? null);
  readonly profile = computed(() => this.profileState());
  readonly isAuthenticated = computed(() => !!this.user());
  readonly isResearcher = computed(() => this.profile()?.role === 'research');
  readonly isLoading = computed(() => this.loadingState());
  readonly isReady = computed(() => this.initialized());
  readonly authError = computed(() => this.authErrorState());

  constructor() {
    this.initializationPromise = this.initialize();
  }

  async login(email: string, password: string) {
    this.ensureSupabaseConfigured();
    this.loadingState.set(true);
    this.authErrorState.set(null);

    try {
      const { error } = await supabase.auth.signInWithPassword({ email, password });

      if (error) {
        throw error;
      }

      await this.refreshSession();
    } finally {
      this.loadingState.set(false);
    }
  }

  async register(payload: RegisterPayload) {
    this.ensureSupabaseConfigured();
    this.loadingState.set(true);
    this.authErrorState.set(null);

    try {
      const { error } = await supabase.auth.signUp({
        email: payload.email,
        password: payload.password,
        options: {
          data: {
            full_name: payload.fullName,
            role: payload.role
          }
        }
      });

      if (error) {
        throw error;
      }

      await this.refreshSession();
    } finally {
      this.loadingState.set(false);
    }
  }

  async logout() {
    this.ensureSupabaseConfigured();
    this.loadingState.set(true);
    this.authErrorState.set(null);

    try {
      const { error } = await supabase.auth.signOut();

      if (error) {
        throw error;
      }

      this.sessionState.set(null);
      this.profileState.set(null);
    } finally {
      this.loadingState.set(false);
    }
  }

  async ensureInitialized() {
    await this.initializationPromise;
  }

  async getAccessToken() {
    await this.ensureInitialized();
    return this.sessionState()?.access_token ?? null;
  }

  private async initialize() {
    if (!isSupabaseConfigured) {
      this.authErrorState.set('Supabase is not configured. Add your real Supabase anon key in frontend/src/environments/environment.ts.');
      this.initialized.set(true);
      return;
    }

    try {
      const {
        data: { session }
      } = await supabase.auth.getSession();

      this.sessionState.set(session);
      try {
        await this.syncProfileWithRetry(session?.user?.id ?? null);
      } catch (error) {
        this.authErrorState.set(this.toMessage(error, 'Unable to load profile.'));
      }

      supabase.auth.onAuthStateChange((_event: AuthChangeEvent, nextSession: Session | null) => {
        this.sessionState.set(nextSession);
        void this.syncProfileWithRetry(nextSession?.user?.id ?? null).catch((error) => {
          this.authErrorState.set(this.toMessage(error, 'Unable to load profile.'));
        });
      });
    } finally {
      this.initialized.set(true);
    }
  }

  private async refreshSession() {
    const {
      data: { session }
    } = await supabase.auth.getSession();

    this.sessionState.set(session);
    await this.syncProfileWithRetry(session?.user?.id ?? null);
  }

  private async syncProfileWithRetry(userId: string | null) {
    if (!userId) {
      this.profileState.set(null);
      this.authErrorState.set(null);
      return;
    }

    const waitStepsMs = [0, 250, 750, 1500];

    for (const delayMs of waitStepsMs) {
      if (delayMs > 0) {
        await this.wait(delayMs);
      }

      const profile = await this.loadProfile(userId);
      if (profile) {
        this.profileState.set(profile);
        this.authErrorState.set(null);
        return;
      }
    }

    this.profileState.set(null);
    this.authErrorState.set('Your profile is not available yet. Refresh the page in a few seconds.');
  }

  private async loadProfile(userId: string) {
    const { data, error } = await supabase
      .from('profiles')
      .select('id, email, full_name, role, created_at, updated_at')
      .eq('id', userId)
      .maybeSingle();

    if (error) {
      throw error;
    }

    return data ? (data satisfies Profile) : null;
  }

  private wait(ms: number) {
    return new Promise<void>((resolve) => {
      window.setTimeout(resolve, ms);
    });
  }

  private toMessage(error: unknown, fallback: string) {
    if (error && typeof error === 'object' && 'message' in error && typeof error.message === 'string') {
      return error.message;
    }

    return fallback;
  }

  private ensureSupabaseConfigured() {
    if (!isSupabaseConfigured) {
      throw new Error('Supabase is not configured. Add your real Supabase anon key in frontend/src/environments/environment.ts.');
    }
  }
}
