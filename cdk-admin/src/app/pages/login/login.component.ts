import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
// import { AuthService } from '../../core/auth.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {AuthenticationService} from "../../_services/authentication.service";
import { first } from 'rxjs/operators';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})


export class LoginComponent implements OnInit {

  userForm: FormGroup;
  formErrors = {
    'username': '',
    'password': ''
  };
  validationMessages = {
    'username': {
      'required': 'Please enter your username',
      'username': 'please enter your vaild username'
    },
    'password': {
      'required': 'please enter your password',
      'pattern': 'The password must contain numbers and letters',
      'minlength': 'Please enter more than 4 characters',
      'maxlength': 'Please enter less than 25 characters',
    }
  };

  constructor(private router: Router,
              private fb: FormBuilder,
              private authService: AuthenticationService) {
  }

  ngOnInit() {
    this.buildForm();
  }

  buildForm() {
    this.userForm = this.fb.group({
      'username': ['', [
        Validators.required,
      ]
      ],
      'password': ['', [
        Validators.minLength(6),
        Validators.maxLength(25)
      ]
      ],
    });

    this.userForm.valueChanges.subscribe(data => this.onValueChanged(data));
    this.onValueChanged();
  }

  onValueChanged(data?: any) {
    // if (!this.userForm) {
    //   return;
    // }
    // const form = this.userForm;
    // for (const field in this.formErrors) {
    //   if (Object.prototype.hasOwnProperty.call(this.formErrors, field)) {
    //     this.formErrors[field] = '';
    //     const control = form.get(field);
    //     if (control && control.dirty && !control.valid) {
    //       const messages = this.validationMessages[field];
    //       for (const key in control.errors) {
    //         if (Object.prototype.hasOwnProperty.call(control.errors, key)) {
    //           this.formErrors[field] += messages[key] + ' ';
    //         }
    //       }
    //     }
    //   }
    // }
  }
  login() {
    this.authService.login(this.userForm.value.username, this.userForm.value.password).pipe(first()).subscribe(users => {
      this.router.navigate(['/dashboard']);
        });
  }
}

