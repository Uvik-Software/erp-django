import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import { environment } from "../../environments/environment";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

    getAllUsers() {
        return this.http.get<any>(`${environment.baseUrl}/users/`)
    }

    createUser(data) {
        return this.http.post<any>(`${environment.baseUrl}/users/`, data)
    }
}
