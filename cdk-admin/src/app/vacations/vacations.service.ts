import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import { environment } from "../../environments/environment";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class VacationsService {

  constructor(private http: HttpClient) { }

    getUkrainianDaysOff() {
        return this.http.get<any>(`${environment.baseUrl}/days_off/?next_month_only=False`)
    }

    getAllVacations() {
        return this.http.get<any>(`${environment.baseUrl}/all_holidays/`)
    }
}
