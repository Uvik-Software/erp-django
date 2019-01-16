import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import { environment } from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {getVacationsResponse} from "../interfaces/vacations";

@Injectable()
export class VacationsService {

  constructor(private http: HttpClient) { }

    getUkrainianDaysOff() {
        return this.http.get(`${environment.baseUrl}/days_off/?next_month_only=False`)
    }

    getAllVacations() {
        return this.http.get<getVacationsResponse>(`${environment.baseUrl}/all_holidays/`)
    }

    createVacation(data) {
      return this.http.post<any>(`${environment.baseUrl}/vacations/`, data)
    }

    getVacation(id) {
      return this.http.get<getVacationsResponse>(`${environment.baseUrl}/vacations/` + id + `/`)
    }

    changeVacation(data) {
      return this.http.put<getVacationsResponse>(`${environment.baseUrl}/vacations/1/`, data)
    }

    deleteVacation(id) {
      return this.http.delete<getVacationsResponse>(`${environment.baseUrl}/vacations/` + id + `/`)
    }
}
