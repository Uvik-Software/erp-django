import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { DndModule } from 'ng2-dnd';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from "@angular/flex-layout";
import { FullCalendarModule } from 'ng-fullcalendar';
import {
  MatToolbarModule,
  MatListModule,
  MatCardModule,
  MatButtonModule,
  MatProgressSpinnerModule,
  MatIconModule,
  MatTableModule,
  MatMenuModule,
  MatSelectModule, MatSortModule, MatFormFieldModule, MatInputModule, MatPaginatorModule, MatDialogModule,
  MatCheckboxModule,
} from '@angular/material';
import {VacationCreateDialog, VacationsComponent} from "./vacations.component";
import {VacationsService} from "./vacations.service";
import {HTTP_INTERCEPTORS} from "@angular/common/http";
import {ErrorInterceptor, JwtInterceptor} from "../_helpers";
import { ToastrModule } from 'ng6-toastr-notifications';

export const ROUTES: Routes = [
   { path: '', component: VacationsComponent },
];
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(ROUTES),
    DndModule.forRoot(),
    FormsModule,
    MatToolbarModule,
    FlexLayoutModule,
    MatListModule,
    MatCardModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatMenuModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSortModule,
    MatTableModule,
    MatPaginatorModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    FullCalendarModule,
    MatCheckboxModule,
    ToastrModule.forRoot(),
  ],
  declarations: [VacationsComponent, VacationCreateDialog],
  entryComponents: [VacationCreateDialog],
  providers: [ VacationsService,
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ]
})
export class VacationsModule { }
