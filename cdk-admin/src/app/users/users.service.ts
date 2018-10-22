import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import { environment } from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {getAllUsers} from "../interfaces/user";

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

    getAllUsers() {
        return this.http.get<getAllUsers>(`${environment.baseUrl}/users/`)
    }

    createUser(data) {
        return this.http.post(`${environment.baseUrl}/users/`, data)
    }
}
