import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import {ManagersInterface, ManagersListResponse} from "../interfaces/managers";

@Injectable({ providedIn: 'root' })
export class ManagersService {
    constructor(private http: HttpClient) { }

    get_managers() {
        return this.http.get<ManagersListResponse>(`${environment.baseUrl}/managers/`)
    }

    update_manager(data) {
      return this.http.put<ManagersInterface>(`${environment.baseUrl}/managers/` + data.id + `/`, data)
    }
}
