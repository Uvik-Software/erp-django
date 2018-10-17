import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { environment } from "../../environments/environment";
import {DashboardReportResponse} from "../interfaces/responses";

@Injectable({ providedIn: 'root' })
export class DashboardReportService {
    constructor(private http: HttpClient) { }

    get_report() {
        return this.http.get<DashboardReportResponse>(`${environment.baseUrl}/dashboard_report/`)
    }
}
