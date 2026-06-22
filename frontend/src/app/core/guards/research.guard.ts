import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const researchGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  await authService.ensureInitialized();

  if (!authService.isAuthenticated()) {
    return router.createUrlTree(['/login'], { queryParams: { next: '/research-hub' } });
  }

  if (authService.isResearcher()) {
    return true;
  }

  return router.createUrlTree(['/']);
};
