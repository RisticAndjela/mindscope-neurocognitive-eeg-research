import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NeuralOrbComponent } from '../../shared/neural-orb/neural-orb.component';

@Component({
  selector: 'ms-home',
  standalone: true,
  imports: [RouterLink, NeuralOrbComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {}
