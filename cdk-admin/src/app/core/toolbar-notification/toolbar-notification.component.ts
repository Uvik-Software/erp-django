import { Component, OnInit, Input, HostListener, ElementRef } from '@angular/core';
import { NotificationService } from "./toolbar-notification.service";
import {Notification_} from "../../interfaces/notification";

@Component({
  selector: 'cdk-toolbar-notification',
  templateUrl: './toolbar-notification.component.html',
  styleUrls: ['./toolbar-notification.component.scss']
})
export class ToolbarNotificationComponent implements OnInit {
	cssPrefix = 'toolbar-notification';
  	isOpen: boolean = false;
  	notifications: Array<Notification_> = [];
  	unchecked_notices: Array<Notification_> = [];

    @HostListener('document:click', ['$event', '$event.target'])
    onClick(event: MouseEvent, targetElement: HTMLElement) {
        if (!targetElement) {
              return;
        }
        const clickedInside = this.elementRef.nativeElement.contains(targetElement);
        if (!clickedInside) {
             this.isOpen = false;
        }
    }
  	
  	constructor(private elementRef: ElementRef, private noticeService: NotificationService) { }

  	ngOnInit() {
      this.getNotifications();
  	}

    getNotifications() {
      this.noticeService.getAllNotifications().subscribe( (response) => {
        this.notifications = response.results;
        this.unchecked_notices = this.notifications.filter(o => o.checked == false)
      })
    }

  	setChecked() {
      this.noticeService.markNotifications().subscribe((response) => {
        this.getNotifications();
      })
  	}

  	delete(notification) {
      this.noticeService.deleteNotifications(notification.id).subscribe((response) => {
        this.getNotifications();
      })
  	}

  	deleteAll() {
      this.noticeService.deleteNotifications('all').subscribe((respose) => {
        this.getNotifications();
      })
    }


}
