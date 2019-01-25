import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  profileForm: FormGroup;

  constructor(private fb: FormBuilder) { }

  ngOnInit() {
  }

  initForm() {
    this.profileForm = this.fb.group({
      first_name: [],
      last_name: [],
      email: [],
      username: [],
      birthday: [],
      tax_number: [],
      phone: [],
      additional_info: [],
    //  need bank info
    })
  }

}
