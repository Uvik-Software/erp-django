import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth.component';
import { DashboardCrmComponent } from '../dashboard-crm/dashboard-crm.component';
import { AuthGuard } from "../_guards";

export const appRoutes: Routes = [{
    path: 'dashboard', component: AuthComponent, canActivate: [AuthGuard], children: [
        { path: '', component: DashboardCrmComponent },
        { path: 'material-widgets', loadChildren: '../material-widgets/material-widgets.module#MaterialWidgetsModule' },
        { path: 'tables', loadChildren: '../tables/tables.module#TablesModule' },
        { path: 'maps', loadChildren: '../maps/maps.module#MapsModule' },
        { path: 'charts', loadChildren: '../charts/charts.module#ChartsModule' },
        { path: 'pages', loadChildren: '../pages/pages.module#PagesModule' },
        { path: 'guarded-routes', loadChildren: '../guarded-routes/guarded-routes.module#GuardedRoutesModule' },
        { path: 'scrumboard', loadChildren: '../scrumboard/scrumboard.module#ScrumboardModule' },
        { path: 'developers', loadChildren: '../developers/developers.module#DevelopersModule' },
        { path: 'clients', loadChildren: '../clients/clients.module#ClientsModule' },
        { path: 'managers', loadChildren: '../managers/managers.module#ManagersModule' },
        { path: 'projects', loadChildren: '../projects/projects.module#ProjectsModule' },
        { path: 'vacations', loadChildren: '../vacations/vacations.module#VacationsModule' },
        { path: 'users', loadChildren: '../users/users.module#UsersModule' },
        { path: 'owners', loadChildren: '../owners/owners.module#OwnersModule' },
        { path: 'profile', loadChildren: '../profile/profile.module#ProfileModule' },
    ]
}];
