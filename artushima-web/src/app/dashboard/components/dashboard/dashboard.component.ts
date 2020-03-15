import { Component, OnInit } from '@angular/core';

import { AuthService } from 'src/app/core/services/auth.service';

/**
 * The dashboard component - the main page of the application.
 */
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  /**
   * Should the user-list card be rendered?
   */
  public hasRoleShowUsers: boolean = false;

  /**
   * Should the card with game master functionalities be rendered?
   */
  public hasRoleShowOwnedCampaigns: boolean = false;

  /**
   * @inheritdoc
   *
   * @param authService the authentication service
   */
  public constructor(
    private authService: AuthService
  ) { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    this.resolveRoles();
  }

  /**
   * Checks if the currently logged in user has the rols that determine
   * rendering of some of the elements.
   */
  private resolveRoles(): void {
    this.hasRoleShowUsers = this.authService.hasUserGotRoles(['role_show_users']);
    this.hasRoleShowOwnedCampaigns = this.authService.hasUserGotRoles(['role_show_owned_campaigns']);
  }

}
