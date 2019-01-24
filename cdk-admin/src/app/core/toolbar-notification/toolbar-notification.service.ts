import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import { environment } from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {getAllNotifications} from "../../interfaces/notification";

@Injectable({ providedIn: 'root' })
export class NotificationService {

  constructor(private http: HttpClient) { }

    getAllNotifications() {
        return this.http.get<getAllNotifications>(`${environment.baseUrl}/notifications/`)
    }

    deleteNotifications(data) {
    if (data !== 'all') {
        return this.http.delete(`${environment.baseUrl}/notifications/` + data + `/`)
    }
    return this.http.delete(`${environment.baseUrl}/notifications/1/`, {params: {data}})
    }

    markNotifications() {
        return this.http.put(`${environment.baseUrl}/notifications/1/`, {})
    }
}
