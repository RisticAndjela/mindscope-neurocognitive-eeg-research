import { AsyncPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'ms-blog',
  standalone: true,
  imports: [AsyncPipe, DatePipe, RouterLink],
  templateUrl: './blog.component.html',
  styleUrl: './blog.component.scss'
})
export class BlogComponent {
  private readonly api = inject(ApiService);

  readonly posts$ = this.api.getBlogPosts();
}