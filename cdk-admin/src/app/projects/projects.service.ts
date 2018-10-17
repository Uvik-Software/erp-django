import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";

@Injectable({ providedIn: 'root' })
export class ProjectsService {
    constructor(private http: HttpClient) { }

    get_projects() {
        return this.http.get<any>(`${environment.baseUrl}/projects/`)
    }

    create_project(data) {
        return this.http.post<any>(`${environment.baseUrl}/projects/`, data)
    }

    update_project(data) {
      return this.http.put<any>(`${environment.baseUrl}/projects/` + data.id + `/`, data)
    }

    delete_project(id) {
      return this.http.delete<any>(`${environment.baseUrl}/projects/` + id + `/`)
    }

    assignDevToProject(data) {
      return this.http.post<any>(`${environment.baseUrl}/developers_on_project/`, data)
    }

    updateDevOnProject(data) {
      return this.http.put<any>(`${environment.baseUrl}/developers_on_project/` + data.id + `/`, data)
    }

    getAssignedDevs(id) {
      return this.http.get<any>(`${environment.baseUrl}/developers_on_project/?project_id=` + id )
    }

    deleteDevFromProject(id) {
      return this.http.delete<any>(`${environment.baseUrl}/developers_on_project/` + id + `/` )
    }
}
