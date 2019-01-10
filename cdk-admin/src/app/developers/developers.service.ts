import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import {DeveloperInterface, DeveloperListResponse} from "../interfaces/developer";

@Injectable({ providedIn: 'root' })
export class DevelopersService {
    constructor(private http: HttpClient) { }

    get_developers() {
        return this.http.get<DeveloperListResponse>(`${environment.baseUrl}/developers/`)
    }

    update_developer(data) {
      return this.http.put<DeveloperInterface>(`${environment.baseUrl}/developers/` + data.id + `/`, data)
    }
}
