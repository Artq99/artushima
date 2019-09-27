import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'src/app/core/services/auth.service';

import { RequestStatus } from 'src/app/model/request-status';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  /**
   * The variable for the input field for the user name.
   */
  userName: string;

  /**
   * The variable for the input field for the password.
   */
  password: string;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {

    // if the user has been already authenticated, navigate to the dashboard
    if (this.authService.isUserLoggedIn()) {
      this.router.navigate(["dashboard"]);
    }
  }

  /**
   * The callback for the button 'login'.
   */
  loginOnClick() {

    this.authService.login(this.userName, this.password)
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.router.navigate([this.authService.postAuthRedirectRoute]);
        } else {
          // TODO change this into a message
          console.log("Login status failure.");
        }
      });
  }

}
