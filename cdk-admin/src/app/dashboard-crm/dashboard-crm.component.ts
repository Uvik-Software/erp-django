import { Component, OnInit } from '@angular/core';
import {User} from "../interfaces/user";
import {DashboardReportService} from "./dashboard-crm.service";

@Component({
    selector: 'app-dashboard-crm',
    templateUrl: './dashboard-crm.component.html',
    styleUrls: ['./dashboard-crm.component.scss']
})

export class DashboardCrmComponent implements OnInit {

    public dashCard = [
        { colorDark: '#5C6BC0', colorLight: '#7986CB', number: 0, title: 'DEVELOPERS', icon: 'code' },
        { colorDark: '#42A5F5', colorLight: '#64B5F6', number: 0, title: 'MANAGERS', icon: 'person' },
        { colorDark: '#26A69A', colorLight: '#4DB6AC', number: 0, title: 'CLIENTS', icon: 'people' },
        { colorDark: '#66BB6A', colorLight: '#81C784', number: 0, title: 'PROJECTS', icon: 'folder' }
    ];

    tableData = [
        { country: 'India', sales: 5400, percentage: '40%' },
        { country: 'Us', sales: 3200, percentage: '30.33%' },
        { country: 'Australia', sales: 2233, percentage: '18.056%' },
        { country: 'Spaim', sales: 600, percentage: '6%' },
        { country: 'China', sales: 200, percentage: '4.50%' },
        { country: 'Brazil', sales: 100, percentage: '2.50%' },
    ];

    constructor(private dashboardReportService: DashboardReportService) { }

    ngOnInit() {
      this.get_report_data()
    }

    get_report_data() {
      this.dashboardReportService.get_report().subscribe((response) => {
        this.dashCard[0].number = response.data.number_of_developers;
        this.dashCard[1].number = response.data.number_of_managers;
        this.dashCard[2].number = response.data.number_of_clients;
        this.dashCard[3].number = response.data.number_of_projects;
      })
    }


}
