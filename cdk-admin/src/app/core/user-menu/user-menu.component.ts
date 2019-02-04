import { Component, OnInit, Input, HostListener, ElementRef } from '@angular/core';
import { AuthenticationService } from "../../_services/authentication.service";
import { Router } from "@angular/router";
import { User } from "../../interfaces/user";

@Component({
  selector: 'cdk-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss']
})
export class UserMenuComponent implements OnInit {
	isOpen: boolean = false;
  currentUserData:User = JSON.parse(localStorage.getItem('currentUser')).user;
  profileLink: string = '/dashboard/profile/';


  	@Input() currentUser = this.currentUserData;
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


  	constructor(private elementRef: ElementRef,
                private authService: AuthenticationService,
                private router: Router) { }


  	ngOnInit() {
  	}

  	logout() {
  	  this.authService.logout();
      this.router.navigate(['/login']);
    }
}
