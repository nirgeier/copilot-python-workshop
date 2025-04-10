import { Routes } from '@angular/router';
import { SuperheroesListComponent } from './superheroes-list/superheroes-list.component';

export const routes: Routes = [
  { path: '', redirectTo: '/superheroes', pathMatch: 'full' },
  { path: 'superheroes', component: SuperheroesListComponent }
];
