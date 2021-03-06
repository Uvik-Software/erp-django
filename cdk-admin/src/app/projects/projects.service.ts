import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { environment } from "../../environments/environment";
import { devOnProject, getAssignedDevs, getProjectsResponse, ProjectInterface } from "../interfaces/projects";
import {ResponseContentType} from "@angular/http";

@Injectable({ providedIn: 'root' })
export class ProjectsService {
    constructor(private http: HttpClient) { }

    get_projects() {
        return this.http.get<getProjectsResponse>(`${environment.baseUrl}/projects/`)
    }

    create_project(data) {
        return this.http.post<ProjectInterface>(`${environment.baseUrl}/projects/`, data)
    }

    update_project(data) {
      return this.http.put<ProjectInterface>(`${environment.baseUrl}/projects/` + data.id + `/`, data)
    }

    delete_project(id) {
      return this.http.delete(`${environment.baseUrl}/projects/` + id + `/`)
    }

    assignDevToProject(data) {
      return this.http.post<devOnProject>(`${environment.baseUrl}/developers_on_project/`, data)
    }

    updateDevOnProject(data) {
      return this.http.put<devOnProject>(`${environment.baseUrl}/developers_on_project/` + data.id + `/`, data)
    }

    getAssignedDevs(id) {
      return this.http.get<getAssignedDevs>(`${environment.baseUrl}/developers_on_project/?project_id=` + id )
    }

    deleteDevFromProject(id) {
      return this.http.delete(`${environment.baseUrl}/developers_on_project/` + id + `/` )
    }

    generateInvoice(data) {
      const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
      return this.http.post(`${environment.baseUrl}/generate_invoice/`, data, {headers: headers, responseType: 'blob'})
    }
}
