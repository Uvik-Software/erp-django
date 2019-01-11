import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import { OwnerInterface, getOwnersResponse } from "../interfaces/owners";

@Injectable({ providedIn: 'root' })
export class OwnersService {
    constructor(private http: HttpClient) { }

    get_owners() {
        return this.http.get<getOwnersResponse>(`${environment.baseUrl}/owners/`)
    }

    create_owner(data) {
        return this.http.post<OwnerInterface>(`${environment.baseUrl}/owners/`, data)
    }

    update_owner(data) {
      return this.http.put<OwnerInterface>(`${environment.baseUrl}/owners/` + data.id + `/`, data)
    }

    delete_owner(id) {
      return this.http.delete(`${environment.baseUrl}/projects/` + id + `/`)
    }
}
