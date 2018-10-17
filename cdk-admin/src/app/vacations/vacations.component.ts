import { Component, OnInit, ViewChild } from '@angular/core';
import { CalendarComponent } from 'ng-fullcalendar';
import { Options } from 'fullcalendar';
import {VacationsService} from "./vacations.service";
import {ClientListResponse} from "../interfaces/client";

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

  constructor(private vacationsService: VacationsService) {}

  ngOnInit() {
    this.vacationsService.getUkrainianDaysOff().subscribe((response:any) => {
      for (let holidayData in response.data) {
        let holiday = {title: holidayData,
                    start: response.data[holidayData]};

        /*
        title: 'Meeting',
        start: yearMonth + '-12T10:30:00',
        end: yearMonth + '-12T12:30:00'
        */

        this.events.push(holiday);
      }
      this.calendarOptions = {
        editable: true,
        eventLimit: false,
        header: {
          left: 'prev,next today',
          center: 'title',
          right: 'month,agendaWeek,agendaDay,listMonth'
        },
        events: this.events
      };
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
    }
    this.displayEvent = model;
  }
  updateEvent(model: any) {
    model = {
      event: {
        id: model.event.id,
        start: model.event.start,
        end: model.event.end,
        title: model.event.title
        // other params
      },
      duration: {
        _data: model.duration._data
      }
    }
    this.displayEvent = model;
  }

}
