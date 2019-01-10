import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { DndModule } from 'ng2-dnd';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from "@angular/flex-layout";
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
} from '@angular/material';
import {ProjectAssignComponent, ProjectEditDialog, ProjectsComponent} from "./projects.component";

export const ROUTES: Routes = [
   { path: '', component: ProjectsComponent },
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
  ],
  declarations: [ProjectsComponent, ProjectEditDialog, ProjectAssignComponent],
  entryComponents: [ProjectEditDialog, ProjectAssignComponent]
})
export class ProjectsModule { }
