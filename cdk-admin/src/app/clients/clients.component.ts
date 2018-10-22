import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { ClientsService } from "./clients.service";
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogConfig,
  MatDialogRef,
  MatPaginator,
  MatTableDataSource
} from "@angular/material";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { ClientInterface, ClientListResponse } from "../interfaces/client";

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.scss']
})
export class ClientsComponent implements OnInit {

  clients: Array<ClientInterface> = [];
  displayedColumns: string[] = ['name', 'position', 'company_name', 'email', 'phone', 'edit'];
  dataSource = new MatTableDataSource<ClientInterface>([]);

  constructor(private clientsService: ClientsService,
              private dialog: MatDialog) { }

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.getClients();
  }

  ngAfterViewInit() {
        this.dataSource.paginator = this.paginator
    }

  getClients() {
    this.clientsService.get_clients().subscribe((response:ClientListResponse) => {
      this.clients = response.results;
      this.dataSource.data = response.results;
      })
  }

  openDialog(id) {
    const dialogConfig = new MatDialogConfig();
    //dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    if (id) {
      dialogConfig.data = this.clients.find(o => o.id === id);
      let dialogRef = this.dialog.open(ClientEditDialog, dialogConfig).afterClosed()
        .subscribe(response => {
          if (response && response.changed) {
            this.clientsService.update_client(response.data).subscribe(() => {
              this.getClients();
            })
          }
        });

    } else {
      dialogConfig.data = {};
      let dialogRef = this.dialog.open(ClientEditDialog).afterClosed()
        .subscribe(response => {
          if (response && response.changed) {
            response.data.owner = JSON.parse(localStorage.getItem('currentUser')).user.id;
            if (response && response.changed) {
            this.clientsService.createClient(response.data).subscribe(() => {
              this.getClients();
            })
          }
         }
       });
    }
  }
}


@Component({
  selector: 'client-edit-dialog',
  templateUrl: './client-edit-dialog.html',
})
export class ClientEditDialog {

  client_data: ClientInterface;

  clientEditForm = new FormGroup ({
    name: new FormControl(),
    position: new FormControl(),
    company_name: new FormControl(),
    email: new FormControl(),
    address: new FormControl(),
    phone: new FormControl(),
    identification_number: new FormControl()
  });

  constructor(public dialogRef: MatDialogRef<ClientEditDialog>,
              private fb: FormBuilder,
              @Inject(MAT_DIALOG_DATA) data) {
    this.client_data = data || {};
    this.createForm()
  }

  ngOnInit() {
  }

  createForm() {
    this.clientEditForm = this.fb.group({
      id: this.client_data.id,
      name: [this.client_data.name, Validators.required],
      position: [this.client_data.position, Validators.required],
      company_name: [this.client_data.company_name, Validators.required],
      email: [this.client_data.email, Validators.compose([
                                            Validators.required,
                                            Validators.email
                                          ])],
      address: [this.client_data.address, Validators.required],
      phone: [this.client_data.phone, Validators.required],
      identification_number: [this.client_data.identification_number, Validators.compose([
                                            Validators.required,
                                            Validators.pattern(/^-?(0|[1-9]\d*)?$/)
                                          ])],
      owner: this.client_data.owner
    });
}

  save() {
    if (!this.clientEditForm.invalid) {
      this.dialogRef.close({ changed: this.clientEditForm.dirty,
                                         data: this.clientEditForm.value });
    }

  }

  discard() {
    this.dialogRef.close();
  }

}
