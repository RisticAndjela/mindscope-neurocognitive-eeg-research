import { Component } from '@angular/core';

@Component({
  selector: 'ms-neural-orb',
  standalone: true,
  template: `
    <div class="orb" aria-hidden="true">
      <div class="ring ring-one"></div>
      <div class="ring ring-two"></div>
      <div class="ring ring-three"></div>
      @for (node of nodes; track node) { <span class="node node-{{ node }}"></span> }
      <div class="scanline"></div>
    </div>
  `,
  styleUrl: './neural-orb.component.scss'
})
export class NeuralOrbComponent {
  readonly nodes = [1,2,3,4,5,6,7,8,9];
}
