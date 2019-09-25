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

    this.authService.login(this.userName, this.password).subscribe(data => console.log(data));
  }

}
