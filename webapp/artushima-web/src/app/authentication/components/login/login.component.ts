import { Component } from '@angular/core';
import { first } from 'rxjs/operators';
import { BackendService } from 'src/app/core/services/backend.service';
import { AuthService } from 'src/app/core/services/auth.service';
import { AuthTokenRequest } from 'src/app/model/auth-token.request';
import { Router } from '@angular/router';

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
    private backendService: BackendService,
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

    let authTokenRequest: AuthTokenRequest = new AuthTokenRequest(this.userName, this.password);

    this.backendService.getAuthToken(authTokenRequest)
      .pipe(first())
      .subscribe(
        response => {
          if (response.status === "success") {
            this.authService.setCurrentUser(response.currentUser);

            if (this.authService.redirectRoute) {
              this.router.navigate([this.authService.redirectRoute]);
            } else {
              this.router.navigate(["dashboard"]);
            }
          } else {
            // TODO change into an alert, when the alert component will be ready
            console.log(response.message);
          }
        },
        // TODO change into an alert, when the alert component will be ready
        error => console.log(error)
      );
  }

}
