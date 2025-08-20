import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SuperheroService, Superhero } from '../services/superhero.service';

@Component({
  selector: 'app-superheroes-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './superheroes-list.component.html',
  styleUrls: ['./superheroes-list.component.css']
})
export class SuperheroesListComponent implements OnInit {
  superheroes: Superhero[] = [];

  constructor(private superheroService: SuperheroService) {}

  ngOnInit(): void {
    this.superheroService.getAllSuperheroes().subscribe(
      heroes => this.superheroes = heroes
    );
  }
}