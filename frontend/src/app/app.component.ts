import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AppLayoutComponent } from './core/layout/app-layout.component';

@Component({
  selector: 'ms-root',
  standalone: true,
  imports: [RouterOutlet, AppLayoutComponent],
  template: '<ms-app-layout><router-outlet /></ms-app-layout>'
})
export class AppComponent {}
