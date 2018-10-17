import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";

@Injectable({ providedIn: 'root' })
export class ManagersService {
    constructor(private http: HttpClient) { }

    get_managers() {
        return this.http.get<any>(`${environment.baseUrl}/managers/`)
    }

    update_manager(data) {
      return this.http.put<any>(`${environment.baseUrl}/managers/` + data.id + `/`, data)
    }
}
