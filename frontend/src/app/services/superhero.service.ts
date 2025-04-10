import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

interface Powerstats {
  intelligence: number;
  strength: number;
  speed: number;
  durability: number;
  power: number;
  combat: number;
}

export interface Superhero {
  id: number;
  name: string;
  image: string;
  powerstats: Powerstats;
}

@Injectable({
  providedIn: 'root'
})
export class SuperheroService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  getAllSuperheroes(): Observable<Superhero[]> {
    return this.http.get<Superhero[]>(`${this.apiUrl}/superheroes/all`);
  }

  getSuperhero(id: number): Observable<Superhero> {
    return this.http.get<Superhero>(`${this.apiUrl}/superheroes/${id}`);
  }

  getSuperheroStats(id: number): Observable<Powerstats> {
    return this.http.get<Powerstats>(`${this.apiUrl}/superheroes/${id}/powerstats`);
  }
}