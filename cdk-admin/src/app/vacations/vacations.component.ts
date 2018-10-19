import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { CalendarComponent } from 'ng-fullcalendar';
import { Options } from 'fullcalendar';
import { VacationsService } from "./vacations.service";
import { DevelopersService } from "../developers/developers.service";
import { getVacationsResponse } from "../interfaces/vacations";
import { MAT_DIALOG_DATA, MatDialog, MatDialogConfig, MatDialogRef } from "@angular/material";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";

@Component({
  selector: 'app-vacations',
  templateUrl: './vacations.component.html',
  styleUrls: ['./vacations.component.scss']
})
export class VacationsComponent implements OnInit {

  calendarOptions: Options;
  events: any = [];
  displayEvent: any;

  @ViewChild(CalendarComponent) ucCalendar: CalendarComponent;

  constructor(private vacationsService: VacationsService,
              private dialog: MatDialog) {}

  ngOnInit() {
    this.getAllDaysOff();
  }

  getAllDaysOff() {
    this.vacationsService.getAllVacations().subscribe((response:getVacationsResponse) => {
        this.calendarOptions = {
        editable: true,
        eventLimit: false,
        header: {
          left: 'prev,next today',
          center: 'title',
          right: 'month,agendaWeek,agendaDay,listMonth'
        },
        events: response.data
      };
        this.events = response.data
    })
  }

  clickButton(model: any) {
    this.displayEvent = model;
  }

  eventClick(model: any) {
    model = {
      event: {
        id: model.event.id,
        start: model.event.start,
        end: model.event.end,
        title: model.event.title,
        allDay: model.event.allDay
        // other params
      },
      duration: {}
    };
    this.displayEvent = model;
    this.createVacationDialog(model.event.id,false)
  }

  updateEvent(model: any) {
    model = {
      event: {
        id: model.id,
        start: model.start,
        end: model.end,
        title: model.title
        // other params
      },
      duration: {
        _data: model.duration
      }
    };
    this.displayEvent = model;
  }

  createVacationDialog(id, create) {
    const dialogConfig = new MatDialogConfig();
      dialogConfig.autoFocus = true;
    if (id) {
      this.vacationsService.getVacation(id).subscribe((response:any) => {
        dialogConfig.data = response.data;
      let dialogRef = this.dialog.open(VacationCreateDialog, dialogConfig).afterClosed()
        .subscribe(response => {
          if (response && response.deleted) {
            this.getAllDaysOff()
          }
          if (response && response.changed) {
            this.vacationsService.changeVacation(response.data).subscribe(() => {
              this.getAllDaysOff()
            })
          }
        });
      });
    } else if (create) {
      let dialogRef = this.dialog.open(VacationCreateDialog).afterClosed()
        .subscribe(response => {
          if (response && response.changed) {
            this.vacationsService.createVacation(response.data).subscribe(() => {
              this.getAllDaysOff();
            })
          }
        });
    }
  }
}

@Component({
  selector: 'vacation-create-dialog',
  templateUrl: './vacation-create-dialog.html',
})
export class VacationCreateDialog {

  developers: any = [];
  user = JSON.parse(localStorage.getItem('currentUser')).user;
  vacation: any;

  vacationCreateForm = new FormGroup ({
    developer_id: new FormControl(),
    from_date: new FormControl(),
    to_date: new FormControl(),
    comments: new FormControl(),
    approved: new FormControl(),
  });

  constructor(public dialogRef: MatDialogRef<any>,
              private developersService: DevelopersService,
              private fb: FormBuilder,
              private vacationsService: VacationsService,
              @Inject(MAT_DIALOG_DATA) data) {
    this.vacation = data || {};
  }

  ngOnInit() {
    this.getDevelopers();
  }

  getDevelopers() {
      this.developersService.get_developers().subscribe((response) => {
        this.developers = response.results;
        this.createForm()
    });
  }

  createForm() {
    let dev_id = this.vacation.developer || '';
    if (this.user.user_type === 'DEVELOPER') {
      dev_id = this.developers.find(o => o.user === this.user.id)
    }

    this.vacationCreateForm = this.fb.group({
      id: this.vacation.id,
      developer_id: [dev_id, Validators.required],
      from_date: [this.vacation.from_date || '', Validators.required],
      to_date: [this.vacation.to_date || '', Validators.required],
      comments: [{value: this.vacation.comments || '', disabled: this.user.user_type === 'DEVELOPER'}],
      approved: [{value: this.vacation.approved || false, disabled: this.user.user_type === 'DEVELOPER'}],
    });
}

  save() {
    if (!this.vacationCreateForm.invalid) {
      this.dialogRef.close({ changed: this.vacationCreateForm.dirty,
                                         data: this.vacationCreateForm.value });
    }

  }

  discard() {
    this.dialogRef.close();
  }

  delete(id) {
    this.vacationsService.deleteVacation(id).subscribe(() => {
        this.dialogRef.close({ deleted: true });
    });
  }

}
