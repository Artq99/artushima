import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { first } from 'rxjs/operators';
import {
  IconDefinition,
  faBiohazard,
  faSignInAlt,
  faSignOutAlt,
  faUserCircle
} from '@fortawesome/free-solid-svg-icons';

import { AuthService } from '../../services/auth.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { CurrentUser } from 'src/app/core/model/current-user';

/**
 * The navbar component for the application.
 */
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit, OnDestroy {

  private currentUserSubscription: Subscription;

  @Input()
  public currentUser: CurrentUser = undefined;

  // icons
  public iconBiohazard: IconDefinition = faBiohazard;
  public iconSignIn: IconDefinition = faSignInAlt;
  public iconSignOut: IconDefinition = faSignOutAlt;
  public iconUser: IconDefinition = faUserCircle;

  public constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  public ngOnInit(): void {
    this.currentUserSubscription = this.authService.currentUser$.subscribe(currentUser => {
      this.currentUser = currentUser;
    });
  }

  public ngOnDestroy(): void {
    this.currentUserSubscription.unsubscribe();
  }

  /**
   * The callback function for the button home.
   */
  public homeOnClick() {
    this.router.navigate(['dashboard']);
  }

  /**
   * The callback function for the button login.
   */
  public logInOnClick() {
    this.router.navigate(['login']);
  }

  /**
   * The callback function for the button logout.
   */
  public logOutOnClick() {
    this.authService.logout()
      .pipe(first())
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.router.navigate(['login']);
        }
      });
  }

}
