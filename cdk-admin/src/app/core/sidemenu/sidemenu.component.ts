import { Component, OnInit, Input } from '@angular/core';
import { menus_admin, menus_dev, menus_man } from './menu-element';

@Component({
  selector: 'cdk-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})
export class SidemenuComponent implements OnInit {

    @Input() iconOnly:boolean = false;
    user: any;
    public menus = [];

    constructor() {
      this.user = JSON.parse(localStorage.getItem('currentUser'));
      if (this.user.user.is_staff) {
        this.menus = menus_admin
      } else if (this.user.user.type == "MANAGER"){
        this.menus = menus_man
      } else {
        this.menus = menus_dev
      }
    }

    ngOnInit() {

    }

}
