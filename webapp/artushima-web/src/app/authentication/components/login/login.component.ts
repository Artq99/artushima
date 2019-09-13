import { Component } from '@angular/core';
import { take } from 'rxjs/operators';
import { BackendService } from 'src/app/core/services/backend.service';
import { AuthService } from 'src/app/core/services/auth.service';
import { AuthTokenRequest } from 'src/app/model/auth-token.request';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  userName: string;
  password: string;

  constructor(
    private backendService: BackendService,
    private authService: AuthService
  ) { }

  loginOnClick() {

    let authTokenRequest: AuthTokenRequest = new AuthTokenRequest(this.userName, this.password);

    this.backendService.getAuthToken(authTokenRequest)
      .pipe(take(1))
      .subscribe(response => {
        if (response.status === "success") {
          this.authService.setAuthToken(response.token);
        } else {
          // TODO change into an alert, when the alert component will be ready
          console.log(response.message);
        }
      });
  }

}
