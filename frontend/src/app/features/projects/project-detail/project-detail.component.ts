import { AsyncPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'ms-project-detail',
  standalone: true,
  imports: [AsyncPipe, DatePipe, RouterLink],
  templateUrl: './project-detail.component.html',
  styleUrl: './project-detail.component.scss'
})
export class ProjectDetailComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ApiService);

  readonly project$ = this.route.paramMap.pipe(
    switchMap(params => this.api.getProjectBySlug(params.get('slug') ?? ''))
  );
}
