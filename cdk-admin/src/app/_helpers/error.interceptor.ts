import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { AuthenticationService } from 'app/_services/authentication.service';
import {Router} from "@angular/router";
import { ToastrManager } from 'ng6-toastr-notifications';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    constructor(private authenticationService: AuthenticationService, private router: Router,
                private toastr: ToastrManager) {}

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
          if (err.status === 400) {
            this.toastr.errorToastr(err.error['message'], err.error['title']);
          }
          if (err.status === 403) {
            this.toastr.errorToastr("You don't have permissions for this option", 'Permissions Error!');
          }
          if (err.status == 500){
            this.toastr.errorToastr("Something went wrong in the backend server", 'Server Error!');
          }

          const error = err.error.message || err.statusText;
          return throwError(error);
        }))
    }
}
