import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {User} from "../interfaces/user";
import {ProfileService} from "./profile.service";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  profileForm: FormGroup;
  currentUser:User = JSON.parse(localStorage.getItem('currentUser')).user;

  constructor(private fb: FormBuilder, private profileService: ProfileService) {
    this.initForm()
  }

  ngOnInit() {
  }

  initForm() {
    this.profileForm = this.fb.group({
      id: this.currentUser.id,
      first_name: [this.currentUser.first_name, Validators.required],
      last_name: [this.currentUser.last_name, Validators.required],
      email: [this.currentUser.email, Validators.required],
      username: [this.currentUser.username, Validators.required],
      birthday: this.currentUser.birthday,
      tax_number: [this.currentUser.tax_number, Validators.required],
      phone: [this.currentUser.phone, Validators.required],
      additional_info: this.currentUser.additional_info,
    //  need bank info
    })
  }

  save(){
    console.log('This is save method');
    if (!this.profileForm.invalid) {
      console.log('Form Valid');
      console.log(this.profileForm);
      this.profileService.update_profile(this.profileForm.value).subscribe(() => {
        console.log('In subscribe!')
      })
    }
  }

}
