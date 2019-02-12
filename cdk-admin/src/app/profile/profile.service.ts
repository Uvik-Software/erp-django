import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import {User} from "../interfaces/user";

@Injectable({ providedIn: 'root' })
export class ProfileService {
    constructor(private http: HttpClient) { }

    update_profile(data) {
      return this.http.put<User>(`${environment.baseUrl}/profile/` + data.id + `/`, data)
    }
}
