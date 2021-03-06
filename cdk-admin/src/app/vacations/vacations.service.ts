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

    getAllVacations(projects, birthdays, vacations, holidays) {
        return this.http.get<getVacationsResponse>(`${environment.baseUrl}/all_holidays/`,
          {params: {'projects': projects, 'birthdays': birthdays, 'vacations': vacations, 'holidays': holidays}})
    }

    createVacation(data) {
      return this.http.post<any>(`${environment.baseUrl}/vacations/`, data)
    }

    getVacation(id) {
      return this.http.get<getVacationsResponse>(`${environment.baseUrl}/vacations/` + id + `/`)
    }

    changeVacation(id, data) {
      return this.http.put<getVacationsResponse>(`${environment.baseUrl}/vacations/` + id + `/`, data)
    }

    deleteVacation(id) {
      return this.http.delete<getVacationsResponse>(`${environment.baseUrl}/vacations/` + id + `/`)
    }
}
