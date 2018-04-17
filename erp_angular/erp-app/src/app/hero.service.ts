import { Injectable } from '@angular/core';
import { Hero } from './hero';
import { HEROES } from './mock-heroes';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { MessageService } from './message.service';
import {HttpClient} from '@angular/common/http';


@Injectable()
export class HeroService {
  configUrl = 'http://127.0.0.1:8000/heroes';
  configDetailUrl = 'http://127.0.0.1:8000/hero/';

  getHero(id: number): Observable<Hero> {
    // TODO: send the message _after_ fetching the hero
    this.messageService.add(`HeroService: fetched hero id=${id}`);
    return this.http.get(this.configDetailUrl + id);
  }

  getHeroes(): Observable<Hero[]> {
    this.messageService.add('HeroService: fetched heroes');
    return this.http.get(this.configUrl);
  }

  constructor(private messageService: MessageService, private http: HttpClient) { }

}
