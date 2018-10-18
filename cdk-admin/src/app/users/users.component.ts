import {Component, Inject, OnInit, ViewChild} from '@angular/core';
import {UserService} from "./users.service";
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogConfig,
  MatDialogRef,
  MatPaginator,
  MatTableDataSource
} from "@angular/material";
import {ManagersInterface} from "../interfaces/managers";
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from "@angular/forms";
import {ClientInterface, ClientListResponse} from "../interfaces/client";
import {Currency, ProjectInterface, ProjectTypes} from "../interfaces/projects";
import {ClientsService} from "../clients/clients.service";
import {ProjectEditDialog} from "../projects/projects.component";

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {

  constructor(private userService: UserService, private dialog: MatDialog, private fb: FormBuilder) { }

  users: any[] = [];
  displayedColumns: string[] = ['name', 'email', 'user_type'];
  dataSource = new MatTableDataSource<ManagersInterface>([]);
  @ViewChild(MatPaginator) paginator: MatPaginator;

  userCreateForm = new FormGroup ({
    username: new FormControl(),
    email: new FormControl(),
    password: new FormControl(),
    position: new FormControl()
  });

  ngOnInit() {
    this.getAllUsers()
  }

  ngAfterViewInit() {
        this.dataSource.paginator = this.paginator
    }


  getAllUsers() {
    this.userService.getAllUsers().subscribe((response:any) => {
        this.dataSource.data = response.data;
      })
  }

  createUser() {

  }

  createForm() {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    let dialogRef = this.dialog.open(userCreateDialog).afterClosed().subscribe(response => {
        if (response && response.changed) {
          this.userService.createUser(response.data).subscribe((response: any) => {
            this.getAllUsers();
          })
        }
      });

  }
}


@Component({
  selector: 'user-create-dialog',
  templateUrl: './user-create-dialog.html',
})

export class userCreateDialog {

  user_data: any = {};
  userTypes = [
    'MANAGER', 'DEVELOPER'
  ];

  userCreateForm = new FormGroup ({
    first_name: new FormControl(),
    last_name: new FormControl(),
    user_name: new FormControl(),
    email: new FormControl(),
    password: new FormControl(),
    user_role: new FormControl(),
    address: new FormControl(),
    company_name: new FormControl(),
    position: new FormControl(),
    hourly_rate: new FormControl(),
    birthday_date: new FormControl(),
    monthly_salary: new FormControl()
  });

  constructor(public dialogRef: MatDialogRef<ProjectInterface>,
              private fb: FormBuilder,
              @Inject(MAT_DIALOG_DATA) data) {
    this.createForm()
  }

  ngOnInit() {

  }

  createForm() {

    this.userCreateForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      user_role: ['', Validators.required],
      email: ['', Validators.compose([Validators.required,
                                                Validators.email])],
      user_name: ['', Validators.required],
      password: ['', Validators.required],
      position: '',
      address: '',
      company_name: '',
      hourly_rate: '',
      birthday_date: '',
      monthly_salary: ''
    });
  }

  save() {
    if (!this.userCreateForm.invalid) {
      this.dialogRef.close({ changed: this.userCreateForm.dirty,
                                         data: this.userCreateForm.value });
    }
  }
  discard() {
    this.dialogRef.close();
  }

}


