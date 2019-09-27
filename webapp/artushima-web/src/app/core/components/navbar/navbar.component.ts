import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
  IconDefinition,
  faBiohazard,
  faSignInAlt,
  faSignOutAlt,
  faUserCircle
} from '@fortawesome/free-solid-svg-icons';

import { CurrentUser } from 'src/app/model/current-user';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  @Input()
  public currentUser: CurrentUser = undefined;

  // icons
  public iconBiohazard: IconDefinition = faBiohazard;
  public iconSignIn: IconDefinition = faSignInAlt;
  public iconSignOut: IconDefinition = faSignOutAlt;
  public iconUser: IconDefinition = faUserCircle;

  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(currentUser => {
      this.currentUser = currentUser;
    });
  }

  public homeOnClick() {
    this.router.navigate(['dashboard']);
  }

  public logInOnClick() {
    this.router.navigate(['login'])
  }

  public logOutOnClick() {
    if (this.currentUser !== undefined) {
      this.currentUser = undefined;
    } else {
      this.currentUser = new CurrentUser();
      this.currentUser.userName = "testUser";
    }
  }

}
