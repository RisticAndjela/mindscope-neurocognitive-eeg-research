import { Component, computed, inject } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'ms-research-hub',
  standalone: true,
  templateUrl: './research-hub.component.html',
  styleUrl: './research-hub.component.scss'
})
export class ResearchHubComponent {
  private readonly authService = inject(AuthService);

  protected readonly profile = computed(() => this.authService.profile());
}
