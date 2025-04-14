import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { SuperheroService, Superhero } from '../services/superhero.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-hero-comparison',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './hero-comparison.component.html',
  styleUrls: ['./hero-comparison.component.css']
})
export class HeroComparisonComponent implements OnInit {
  hero1: Superhero | null = null;
  hero2: Superhero | null = null;
  winner: string = '';
  readonly statsList = ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat'] as const;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private heroService: SuperheroService
  ) {}

  ngOnInit(): void {
    const id1 = Number(this.route.snapshot.paramMap.get('id1'));
    const id2 = Number(this.route.snapshot.paramMap.get('id2'));

    if (isNaN(id1) || isNaN(id2)) {
      this.router.navigate(['/superheroes']);
      return;
    }

    // Load both heroes in parallel
    forkJoin({
      hero1: this.heroService.getSuperhero(id1),
      hero2: this.heroService.getSuperhero(id2)
    }).subscribe({
      next: ({ hero1, hero2 }) => {
        this.hero1 = hero1;
        this.hero2 = hero2;
        this.determineWinner();
      },
      error: () => this.router.navigate(['/superheroes'])
    });
  }

  private determineWinner(): void {
    if (!this.hero1 || !this.hero2) return;

    let score1 = 0;
    let score2 = 0;

    for (const stat of this.statsList) {
      if (this.hero1.powerstats[stat] > this.hero2.powerstats[stat]) {
        score1++;
      } else if (this.hero2.powerstats[stat] > this.hero1.powerstats[stat]) {
        score2++;
      }
    }

    if (score1 > score2) {
      this.winner = this.hero1.name;
    } else if (score2 > score1) {
      this.winner = this.hero2.name;
    } else {
      this.winner = 'Tie';
    }
  }

  getWinnerClass(stat: string): string {
    if (!this.hero1 || !this.hero2) return '';
    
    if (this.hero1.powerstats[stat] > this.hero2.powerstats[stat]) {
      return 'winner-1';
    } else if (this.hero2.powerstats[stat] > this.hero1.powerstats[stat]) {
      return 'winner-2';
    }
    return 'tie';
  }

  goBack(): void {
    this.router.navigate(['/superheroes']);
  }
}