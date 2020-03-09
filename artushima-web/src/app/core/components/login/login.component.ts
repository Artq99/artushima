import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'src/app/core/services/auth.service';

import { RequestStatus } from 'src/app/core/model/request-status';

/**
 * The component containing a form for user authentication.
 */
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  @Input()
  public userName: string;

  @Input()
  public password: string;

  public constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  public ngOnInit() {

    // if the user has been already authenticated, navigate to the dashboard
    if (this.authService.isUserLoggedIn()) {
      this.router.navigate(["dashboard"]);
    }
  }

  /**
   * The callback for the button 'login'.
   */
  public loginOnClick() {

    this.authService.login(this.userName, this.password)
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.router.navigate([this.authService.postAuthRedirectRoute]);
        } else {
          this.password = '';
        }
      });
  }

}
