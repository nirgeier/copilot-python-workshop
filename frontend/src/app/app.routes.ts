import { Routes } from '@angular/router';
import { SuperheroesListComponent } from './superheroes-list/superheroes-list.component';
import { HeroComparisonComponent } from './hero-comparison/hero-comparison.component';

export const routes: Routes = [
  { path: '', redirectTo: '/superheroes', pathMatch: 'full' },
  { path: 'superheroes', component: SuperheroesListComponent },
  { path: 'compare/:id1/:id2', component: HeroComparisonComponent }
];
