import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'ms-research-forbidden-state',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="forbidden glass-card">
      <span class="badge">Restricted access</span>
      <h1>Research workspace unavailable</h1>
      <p>
        This notebook is reserved for authenticated researchers. Your current account can still explore the public
        MindScope journal, projects, and conceptual pages.
      </p>
      <div class="actions">
        <a routerLink="/blog" class="secondary-button">View public blog</a>
        <a routerLink="/" class="primary-button">Return home</a>
      </div>
    </section>
  `,
  styles: [`
    .forbidden {
      width: min(760px, 100%);
      margin: 72px auto;
      padding: clamp(28px, 5vw, 48px);
      text-align: left;
    }
    h1 {
      margin: 18px 0 12px;
      font-family: "Space Grotesk";
      font-size: clamp(34px, 6vw, 62px);
      line-height: .96;
      letter-spacing: -.05em;
    }
    p {
      max-width: 620px;
      color: var(--text-soft);
      line-height: 1.8;
    }
    .actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 28px;
    }
  `]
})
export class ResearchForbiddenStateComponent {}
