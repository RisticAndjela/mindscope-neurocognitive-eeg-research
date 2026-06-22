import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

@Component({
  selector: 'ms-research-forbidden-state',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="forbidden-shell">
      <div class="signal-column">
        <span class="badge">Restricted neural workspace</span>
        <div class="signal-stack" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <section class="forbidden glass-card">
      <span class="badge badge-inline">Research role required</span>
      <h1>Research workspace unavailable</h1>
      <p>
        This notebook is reserved for authenticated researchers. Your current account can still explore the public
        MindScope journal, projects, and conceptual pages.
      </p>
      <div class="next-route">
        <span>Requested route</span>
        <strong>{{ requestedRoute() }}</strong>
      </div>
      <div class="actions">
        <a routerLink="/blog" class="secondary-button">View public blog</a>
        <a routerLink="/projects" class="secondary-button">Browse projects</a>
        <a routerLink="/" class="primary-button">Return home</a>
      </div>
      </section>
    </section>
  `,
  styles: [`
    .forbidden-shell {
      width: min(980px, 100%);
      margin: 72px auto;
      display: grid;
      grid-template-columns: minmax(160px, 220px) minmax(0, 1fr);
      gap: 24px;
      align-items: stretch;
    }
    .signal-column {
      display: grid;
      gap: 18px;
      align-content: start;
    }
    .signal-stack {
      min-height: 260px;
      border: 1px solid rgba(124, 92, 255, 0.22);
      border-radius: 32px;
      background:
        linear-gradient(180deg, rgba(124, 92, 255, 0.12), rgba(53, 200, 255, 0.05)),
        rgba(18, 24, 38, 0.68);
      display: grid;
      place-items: center;
      gap: 12px;
      padding: 24px;
      box-shadow: 0 0 42px rgba(124, 92, 255, 0.16);
    }
    .signal-stack span {
      display: block;
      width: 100%;
      height: 2px;
      border-radius: 999px;
      background: linear-gradient(90deg, transparent, rgba(53, 200, 255, 0.95), transparent);
      animation: pulse 2.4s ease-in-out infinite;
    }
    .signal-stack span:nth-child(2) {
      animation-delay: .3s;
    }
    .signal-stack span:nth-child(3) {
      animation-delay: .6s;
    }
    .forbidden {
      padding: clamp(28px, 5vw, 48px);
      text-align: left;
      position: relative;
      overflow: hidden;
    }
    .forbidden::after {
      content: "";
      position: absolute;
      inset: auto -18% -32% 52%;
      width: 320px;
      height: 320px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(124, 92, 255, 0.2), transparent 68%);
      pointer-events: none;
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
    .badge-inline {
      position: relative;
      z-index: 1;
    }
    .next-route {
      margin-top: 22px;
      display: grid;
      gap: 8px;
      padding: 14px 16px;
      border: 1px solid rgba(53, 200, 255, 0.18);
      border-radius: 20px;
      background: rgba(6, 12, 22, 0.44);
      color: var(--text-soft);
      max-width: 460px;
    }
    .next-route span {
      font-family: "JetBrains Mono";
      font-size: 12px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--text-muted);
    }
    .next-route strong {
      word-break: break-word;
      font-weight: 500;
    }
    .actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 28px;
    }
    @keyframes pulse {
      0%, 100% { opacity: .35; transform: scaleX(.92); }
      50% { opacity: 1; transform: scaleX(1); }
    }
    @media (max-width: 860px) {
      .forbidden-shell {
        grid-template-columns: 1fr;
      }
      .signal-stack {
        min-height: 140px;
      }
    }
  `]
})
export class ResearchForbiddenStateComponent {
  private readonly route = inject(ActivatedRoute);

  protected readonly requestedRoute = computed(() => this.route.snapshot.queryParamMap.get('next') ?? '/research/blog');
}
