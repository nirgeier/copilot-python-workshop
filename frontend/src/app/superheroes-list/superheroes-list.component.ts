import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
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
  selectedHeroes: Superhero[] = [];

  constructor(
    private superheroService: SuperheroService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.superheroService.getAllSuperheroes().subscribe(
      heroes => this.superheroes = heroes
    );
  }

  toggleSelection(hero: Superhero): void {
    const index = this.selectedHeroes.findIndex(h => h.id === hero.id);
    if (index === -1) {
      if (this.selectedHeroes.length < 2) {
        this.selectedHeroes.push(hero);
      }
    } else {
      this.selectedHeroes.splice(index, 1);
    }
  }

  isSelected(hero: Superhero): boolean {
    return this.selectedHeroes.some(h => h.id === hero.id);
  }

  canCompare(): boolean {
    return this.selectedHeroes.length === 2;
  }

  compareHeroes(): void {
    if (this.canCompare()) {
      const [hero1, hero2] = this.selectedHeroes;
      this.router.navigate(['/compare', hero1.id, hero2.id]);
    }
  }
}