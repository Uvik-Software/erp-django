import {Component, OnInit, Input, ViewChild, Inject} from '@angular/core';
import { DevelopersService } from "./developers.service";
import {
  MatTableDataSource,
  MatPaginator,
  MatDialog,
  MatDialogRef,
  MatDialogConfig,
  MAT_DIALOG_DATA
} from '@angular/material';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {DeveloperInterface, DeveloperListResponse} from "../interfaces/developer";
import { ToastrManager } from 'ng6-toastr-notifications';

@Component({
  selector: 'app-developers',
  templateUrl: './developers.component.html',
  styleUrls: ['./developers.component.scss']
})
export class DevelopersComponent implements OnInit {

  displayedColumns: string[] = ['full_name', 'email', 'hourly_rate', 'monthly_salary', 'birthday_date', 'edit'];
  dataSource = new MatTableDataSource<DeveloperInterface>([]);
  developers: Array<DeveloperInterface> = [];

  constructor(private developersService: DevelopersService,
              private dialog: MatDialog, private toastr: ToastrManager) { }

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.getDevelopers();
  }

  ngAfterViewInit() {
        this.dataSource.paginator = this.paginator
    }

  getDevelopers() {
    this.developersService.get_developers().subscribe((response:DeveloperListResponse) => {
      this.developers = response.results;
      this.dataSource.data = response.results;
      })
  }

  openDialog(id) {
    const dialogConfig = new MatDialogConfig();
    //dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.data = this.developers.find(o => o.id === id);
    let dialogRef = this.dialog.open(DeveloperEditDialog, dialogConfig).afterClosed()
      .subscribe(response => {
        if (response && response.changed) {
          this.developersService.update_developer(response.data).subscribe((response:DeveloperInterface) => {
            this.getDevelopers();
            this.toastr.successToastr('Developer was successfully updated', 'Developer updated')
      })
        }
      });

  }

}

@Component({
  selector: 'developer-edit-dialog',
  templateUrl: './developer-edit-modal.html',
})
export class DeveloperEditDialog {

  dev_data: DeveloperInterface;

  developerEditForm = new FormGroup ({
    first_name: new FormControl(),
    last_name: new FormControl(),
    email: new FormControl(),
    hourly_rate: new FormControl(),
    monthly_salary: new FormControl(),
    birthday_date: new FormControl(),
    vacation_days: new FormControl(),
  });

  constructor(public dialogRef: MatDialogRef<DeveloperEditDialog>,
              private fb: FormBuilder,
              @Inject(MAT_DIALOG_DATA) data) {
    this.dev_data = data;
    this.createForm()
  }

  ngOnInit() {
  }

  createForm() {
    this.developerEditForm = this.fb.group({
      id: this.dev_data.id,
      first_name: [this.dev_data.first_name, Validators.required],
      last_name: [this.dev_data.last_name, Validators.required],
      email: [this.dev_data.email, Validators.compose([
                                            Validators.required,
                                            Validators.email
                                          ])],
      hourly_rate: [this.dev_data.hourly_rate, Validators.compose([
                                            Validators.required,
                                            Validators.pattern(/^-?(0|[1-9]\d*)?$/)
                                          ])],
      monthly_salary: [this.dev_data.monthly_salary, Validators.compose([
                                            Validators.required,
                                            Validators.pattern(/^-?(0|[1-9]\d*)?$/)
                                          ])],
      birthday_date: [this.dev_data.birthday_date, Validators.required],
      user: this.dev_data.user,
      vacation_days: this.dev_data.vacation_days
    });
}

  save() {
    if (!this.developerEditForm.invalid) {
      this.dialogRef.close({ changed: this.developerEditForm.dirty,
                                         data: this.developerEditForm.value });
    }

  }

  discard() {
    this.dialogRef.close();
  }

}
