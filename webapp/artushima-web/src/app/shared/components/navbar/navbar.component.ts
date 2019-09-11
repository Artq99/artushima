import { Component, OnInit } from '@angular/core';
import { IconDefinition, faBiohazard, faSignInAlt, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  /**
   * The biohazard icon.
   */
  iconBiohazard: IconDefinition = faBiohazard;

  /**
   * The icon indicating the state of the authentication.
   */
  iconLogInOut: IconDefinition;

  // The icons for the authentication state.
  private iconSignIn: IconDefinition = faSignInAlt;
  private iconSignOut: IconDefinition = faSignOutAlt

  constructor() { }

  ngOnInit() {
    // TODO this must be changen when the required components will be ready.
    this.iconLogInOut = this.iconSignIn;
  }

  /**
   * This method is only temorary.
   */
  logInOutOnClick() {
    if (this.iconLogInOut === this.iconSignIn) {
      this.iconLogInOut = this.iconSignOut;
    } else {
      this.iconLogInOut = this.iconSignIn;
    }
  }

}
