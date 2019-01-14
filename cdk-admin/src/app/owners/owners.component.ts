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

import { OwnerInterface, getOwnersResponse } from "../interfaces/owners";
import { OwnersService } from "./owners.service";

@Component({
  selector: 'app-owners',
  templateUrl: './owners.component.html',
  styleUrls: ['./owners.component.scss']
})

export class OwnersComponent implements OnInit {

  owners: Array<OwnerInterface> = [];
  displayedColumns: string[] = ['name', 'tax_number', 'edit'];
  dataSource = new MatTableDataSource<OwnerInterface>([]);

  constructor(private ownersService: OwnersService, private dialog: MatDialog) { }

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.getOwners();
  }

  getOwners(){
    this.ownersService.get_owners().subscribe((response:getOwnersResponse) => {
      this.owners = response.results;
      this.dataSource.data = response.results;
    })
  }

  openDialog(id) {

    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;

    if (id) {
      dialogConfig.data = this.owners.find(o => o.id === id);
      let dialogRef = this.dialog.open(OwnersModalComponent, dialogConfig).afterClosed()
        .subscribe(response => {
          if (response && response.changed) {
            this.ownersService.update_owner(response.data).subscribe(() => {
              this.getOwners();
            })
          }
        });
    } else {
      let dialogRef = this.dialog.open(OwnersModalComponent).afterClosed().subscribe(response => {
        if (response && response.changed) {
          this.ownersService.create_owner(response.data).subscribe(() => {
            this.getOwners();
          })
        }
      });
    }
  }

  deleteOwner(id) {
    this.ownersService.delete_owner(id).subscribe(() => {
      this.getOwners();
    })
  }
}


@Component({
  selector: 'owners-modal-component',
  templateUrl: './owners-modal.html',
})
export class OwnersModalComponent {

  owner_data: OwnerInterface;
  ownerCreateForm = new FormGroup({
    first_name: new FormControl(),
    last_name: new FormControl(),
    address: new FormControl(),
    tax_number: new FormControl(),
    num_contract_with_dev: new FormControl(),
    date_contract_with_dev: new FormControl(),
  });

  constructor( private ownersService: OwnersService,
               public dialogRef: MatDialogRef<OwnerInterface>,
               private fb: FormBuilder,
               @Inject(MAT_DIALOG_DATA) data) {
    this.owner_data = data || {};
    this.createForm();
  }

  ngOnInit() {
  }

  createForm() {

    this.ownerCreateForm = this.fb.group({
      id: this.owner_data.id,
      first_name: [this.owner_data.first_name, Validators.required],
      last_name: [this.owner_data.last_name, Validators.required],
      address: this.owner_data.address,
      tax_number: [this.owner_data.tax_number, Validators.required],
      num_contract_with_dev: [this.owner_data.num_contract_with_dev, Validators.required],
      date_contract_with_dev: this.owner_data.date_contract_with_dev
    });
  }

  save() {
    if (!this.ownerCreateForm.invalid) {
      this.dialogRef.close({ changed: this.ownerCreateForm.dirty,
                                         data: this.ownerCreateForm.value });
    }
  }
  discard() {
    this. dialogRef.close();
  }

}
