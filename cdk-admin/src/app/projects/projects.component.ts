import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogConfig,
  MatDialogRef,
  MatPaginator,
  MatTableDataSource
} from "@angular/material";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";

import {
  Currency,
  devOnProject,
  getAssignedDevs,
  getProjectsResponse,
  ProjectInterface,
  ProjectTypes
} from "../interfaces/projects";

import { ProjectsService } from "./projects.service";
import { ClientsService } from "../clients/clients.service";
import { DevelopersService } from "../developers/developers.service";
import { ManagersService } from "../managers/managers.service";
import { OwnersService } from "../owners/owners.service";
// import {DeveloperInterface} from "../interfaces/developer";

import {ClientInterface, ClientListResponse} from "../interfaces/client";
import {ManagersInterface, ManagersListResponse} from "../interfaces/managers";
import { OwnerInterface, getOwnersResponse } from "../interfaces/owners";
import {ProfileService} from "../profile/profile.service";
import {ToastrManager} from 'ng6-toastr-notifications';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.scss']
})
export class ProjectsComponent implements OnInit {

  is_admin: boolean = JSON.parse(localStorage.getItem('currentUser')).user.is_staff;
  projects: Array<ProjectInterface> = [];
  displayedColumns: string[] = ['project_name', 'project_type', 'edit'];
  dataSource = new MatTableDataSource<ProjectInterface>([]);

  constructor(private projectsService: ProjectsService, private dialog: MatDialog, private toastr: ToastrManager) { }

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.getProjects();
  }

  ngAfterViewInit() {
        this.dataSource.paginator = this.paginator
    }

  getProjects() {
    this.projectsService.get_projects().subscribe((response:getProjectsResponse) => {
      this.projects = response.results;
      this.dataSource.data = response.results;
      })
  }

  openDialog(id) {

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;

    if (id) {
      dialogConfig.data = this.projects.find(o => o.id === id);
      let dialogRef = this.dialog.open(ProjectEditDialog, dialogConfig).afterClosed()
        .subscribe(response => {
          if (response && response.changed) {
            this.projectsService.update_project(response.data).subscribe(() => {
              this.getProjects();
              this.toastr.successToastr('Project was successfully updated', 'Project updated')
            })
          }
        });
    } else {
      let dialogRef = this.dialog.open(ProjectEditDialog).afterClosed().subscribe(response => {
          if (response && response.changed) {
            // response.data.owner = JSON.parse(localStorage.getItem('currentUser')).user.id;
            response.data.client = response.data.client.id;
            console.log(response.data);
            this.projectsService.create_project(response.data).subscribe(() => {
              this.getProjects();
              this.toastr.successToastr('Project was successfully created', 'Project created');
            })
          }
        });
    }
  }

  deleteProject(id) {
    this.projectsService.delete_project(id).subscribe(() => {
              this.getProjects();
            })
  }

  assignToProject(id) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    dialogConfig.data = this.projects.find(o => o.id === id);
    let dialogRef = this.dialog.open(ProjectAssignComponent, dialogConfig)
  }
}

@Component({
  selector: 'project-edit-dialog',
  templateUrl: './project-edit-dialog.html',
})

export class ProjectEditDialog {

  project_data: ProjectInterface;
  projectTypes: ProjectTypes[] = [
    { value: 'OUTSTAFF', name: 'Outstaff' },
    { value: 'FIX_PRICE_PROJECT', name: 'Fix Price Project' },
    { value: 'TIME_AND_MATERIAL', name: 'Time & Material' }
  ];
  currencies: Currency[] = [
    { name: 'USD' },
    { name: 'EUR' },
    { name: 'UAH' }
  ];

  clients:ClientInterface[] = [];
  client:ClientInterface;

  managers: ManagersInterface[] = [];
  manager_info: ManagersInterface;

  owners: OwnerInterface[] = [];
  owner: OwnerInterface;

  projectEditForm = new FormGroup ({
    project_name: new FormControl(),
    project_type: new FormControl(),
    project_description: new FormControl(),
    currency: new FormControl(),
    basic_price: new FormControl(),
    client: new FormControl(),
    manager_info: new FormControl(),
    all_time_money_spent: new FormControl(),
    deadline: new FormControl(),
    project_started_date: new FormControl(),
  });

  constructor(public dialogRef: MatDialogRef<ProjectInterface>,
              private fb: FormBuilder,
              private clientService: ClientsService,
              private managerService: ManagersService,
              private ownerService: OwnersService,
              @Inject(MAT_DIALOG_DATA) data) {
    this.project_data = data || {};
    this.createForm()
  }

  ngOnInit() {
    this.getClientsList();
    this.getManagers();
    this.getOwners();
  }

  getClientsList() {
    this.clientService.get_clients().subscribe((response:ClientListResponse) => {
      this.clients = response.results;
    });
  }

  getManagers() {
    this.managerService.get_managers().subscribe((response:ManagersListResponse) => {
      this.managers = response.results;
    })
  }

  getOwners() {
    this.ownerService.get_owners().subscribe((response: getOwnersResponse) => {
      this.owners = response.results;
    })
  }

  createForm() {

    if (this.project_data.client) {
      this.client = this.project_data.client;
    }

    this.projectEditForm = this.fb.group({
      id: this.project_data.id,
      project_name: [this.project_data.project_name, Validators.required],
      project_type: [this.project_data.project_type, Validators.required],
      project_description: [this.project_data.project_description, Validators.required],
      currency: [this.project_data.currency, Validators.required],
      basic_price: [this.project_data.basic_price || 0],
      // manager_info: this.project_data.manager_info,
      client: [this.client, Validators.required],
      manager_info: [this.project_data.manager_info, Validators.required],
      all_time_money_spent: [{value: this.project_data.all_time_money_spent, disabled: true}],
      deadline: this.project_data.deadline,
      project_started_date: this.project_data.project_started_date,
      owner: this.project_data.owner
    });
}

  save() {
    console.log(this.projectEditForm);
    if (!this.projectEditForm.invalid) {
      this.projectEditForm.value.client = this.client;
      this.dialogRef.close({ changed: this.projectEditForm.dirty,
                                         data: this.projectEditForm.value });
    }
  }

  discard() {
    this.dialogRef.close();
  }

  changeProjectType(event) {
    this.projectEditForm.value.project_type = event;
  }

  changeCurrency(event) {
    this.projectEditForm.value.currency = event;
  }

  changeClient(event) {
    this.client = this.clients.find(o => o.id === event);
  }

  changeManager(event) {
    this.manager_info = this.managers.find(o => o.id === event);
  }

  changeOwner(event) {
    this.owner = this.owners.find(o => o.id == event);
  }

}

@Component({
  selector: 'app-scrumboard-assign',
  templateUrl: './project-assign-dialog.html'
})
export class ProjectAssignComponent {

    availableDevelopers: devOnProject[];
    assignedDevelopers: devOnProject[];
    availableDevelopersAtStart: devOnProject[];
    assignedDevelopersAtStart: devOnProject[];
    project: ProjectInterface;

    constructor(private developersService: DevelopersService,
                private projectsService:ProjectsService,
                public dialogRef: MatDialogRef<any>,
              @Inject(MAT_DIALOG_DATA) data) {
    this.project = data;
  }

  ngOnInit() {
    this.getDevelopers();
  }

  getDevelopers() {
    this.projectsService.getAssignedDevs(this.project.id).subscribe((response: getAssignedDevs) => {
      this.assignedDevelopers = response.results;
      this.developersService.get_developers().subscribe((response: any) => {
        this.availableDevelopers = response.results;
        for (let dev of this.assignedDevelopers) {
          this.availableDevelopers.splice(0, 1);
        }
        this.availableDevelopersAtStart = [...this.availableDevelopers];
        this.assignedDevelopersAtStart = [...this.assignedDevelopers];
      });
    });
  }

  apply() {
    for (let developer of this.assignedDevelopers) {
        if (!this.assignedDevelopersAtStart.includes(developer)) {

          let data = {project: this.project.id,
                      developer: developer.id,
                      // owner: JSON.parse(localStorage.getItem('currentUser')).user.id,
                      hours: developer.hours,
                      description: developer.description};
            this.projectsService.assignDevToProject(data).subscribe(() => {
      })
        } else if (this.assignedDevelopersAtStart.includes(developer)) {
          let data = {project: this.project.id,
                      id: developer.id,
                      // owner: JSON.parse(localStorage.getItem('currentUser')).user.id,
                      hours: developer.hours,
                      description: developer.description,
                      developer: developer.developer};
                  this.projectsService.updateDevOnProject(data).subscribe(() => {
            })
        }
    }
    for (let developer of this.availableDevelopers) {
        if(!this.availableDevelopersAtStart.includes(developer)) {
          this.projectsService.deleteDevFromProject(developer.id).subscribe(() => {
      })
        }
    }
    this.dialogRef.close();
  }

  discard() {
    this.dialogRef.close();
  }

}
