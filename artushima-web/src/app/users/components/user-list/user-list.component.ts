import { Component, OnInit } from '@angular/core';

import { AuthService } from 'src/app/core/services/auth.service';
import { UserService } from '../../services/user.service';

import { User } from '../../model/user';

/**
 * The component showing a list of all users.
 */
@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {

  /**
   * Should the user be able to navigate to the user-creator?
   */
  public hasRoleCreateUser: boolean = false;

  /**
   * The list of all users.
   */
  public users: User[] = [];

  public constructor(
    private authService: AuthService,
    private userService: UserService
  ) { }

  public ngOnInit() {
    this.resolveRoles();
    this.loadUsers();
  }

  /**
   * Resolve the user roles that determine the visibility of some of
   * the component elements.
   */
  private resolveRoles(): void {
    this.hasRoleCreateUser = this.authService.hasUserGotRoles(['role_create_user']);
  }

  /**
   * Loads the users from the backend.
   */
  private loadUsers(): void {
    this.userService.getUserList()
      .subscribe(response => this.users = response);
  }
}
