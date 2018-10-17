import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogConfig,
  MatDialogRef,
  MatPaginator,
  MatTableDataSource
} from "@angular/material";
import { ManagersService } from "./managers.service";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { ManagersInterface, ManagersListResponse } from "../interfaces/managers";

@Component({
  selector: 'app-managers',
  templateUrl: './managers.component.html',
  styleUrls: ['./managers.component.scss']
})
export class ManagersComponent implements OnInit {

  managers: ManagersInterface[] = [];
  displayedColumns: string[] = ['name', 'email', 'manager_position', 'company_name', 'edit'];
  dataSource = new MatTableDataSource<ManagersInterface>([]);

  constructor(private managersService: ManagersService, private dialog: MatDialog) { }

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.getManagers()
  }

  ngAfterViewInit() {
        this.dataSource.paginator = this.paginator
    }

  getManagers() {
    this.managersService.get_managers().subscribe((response:ManagersListResponse) => {
      this.managers = response.results;
      this.dataSource.data = response.results;
      })
  }

  openDialog(id) {
    const dialogConfig = new MatDialogConfig();
    //dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.data = this.managers.find(o => o.id === id);
    let dialogRef = this.dialog.open(ManagerEditDialog, dialogConfig).afterClosed()
      .subscribe(response => {
        if (response && response.changed) {
          this.managersService.update_manager(response.data).subscribe((response: ManagersInterface) => {
            this.getManagers();
          })
        }
      });

  }
}


@Component({
  selector: 'manager-edit-dialog',
  templateUrl: './manager-edit-dialog.html',
})
export class ManagerEditDialog {

  manager_data: ManagersInterface;

  managerEditForm = new FormGroup ({
    name: new FormControl(),
    surname: new FormControl(),
    email: new FormControl(),
    position: new FormControl(),
    address: new FormControl(),
    company_name: new FormControl()
  });

  constructor(public dialogRef: MatDialogRef<ManagersInterface>,
              private fb: FormBuilder,
              @Inject(MAT_DIALOG_DATA) data) {
    this.manager_data = data;
    this.createForm()
  }

  ngOnInit() {
  }

  createForm() {
    this.managerEditForm = this.fb.group({
      id: this.manager_data.id,
      name: [this.manager_data.name, Validators.required],
      surname: [this.manager_data.surname, Validators.required],
      email: [this.manager_data.email, Validators.compose([
                                            Validators.required,
                                            Validators.email
                                          ])],
      position: [this.manager_data.position, Validators.required],
      address: [this.manager_data.address, Validators.required],
      company_name: [this.manager_data.company_name, Validators.required],
      user: this.manager_data.user
    });
}

  save() {
    if (!this.managerEditForm.invalid) {
      this.dialogRef.close({ changed: this.managerEditForm.dirty,
                                         data: this.managerEditForm.value });
    }

  }

  discard() {
    this.dialogRef.close();
  }

}
