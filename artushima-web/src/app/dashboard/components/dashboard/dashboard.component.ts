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

  public constructor(
    private authService: AuthService
  ) { }

  public ngOnInit() {
    this.hasRoleShowUsers = this.authService.hasUserGotRoles(['role_show_users']);
  }

}
