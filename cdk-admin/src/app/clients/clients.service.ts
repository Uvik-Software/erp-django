import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import {ClientInterface, ClientListResponse} from "../interfaces/client";

@Injectable({ providedIn: 'root' })
export class ClientsService {
    constructor(private http: HttpClient) { }

    get_clients() {
        return this.http.get<ClientListResponse>(`${environment.baseUrl}/clients/`)
    }

    update_client(data) {
      return this.http.put<ClientInterface>(`${environment.baseUrl}/clients/` + data.id + `/`, data)
    }

    createClient(data) {
        return this.http.post<ClientListResponse>(`${environment.baseUrl}/clients/`, data)
    }
}
