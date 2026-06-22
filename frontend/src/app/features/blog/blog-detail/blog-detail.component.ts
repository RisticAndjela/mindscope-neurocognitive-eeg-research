import { AsyncPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'ms-blog-detail',
  standalone: true,
  imports: [AsyncPipe, DatePipe, RouterLink],
  templateUrl: './blog-detail.component.html',
  styleUrl: './blog-detail.component.scss'
})
export class BlogDetailComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ApiService);

  readonly post$ = this.route.paramMap.pipe(
    switchMap(params => this.api.getBlogPost(params.get('id') ?? ''))
  );
}