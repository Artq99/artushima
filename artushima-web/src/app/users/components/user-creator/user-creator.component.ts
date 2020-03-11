import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../../services/user.service';
import { MessagesService } from 'src/app/core/services/messages.service';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';

/**
 * All the existing roles.
 *
 * The list must be the same as at the backend.
 */
export const ROLES = [
  'role_show_users',
  'role_create_user'
]

/**
 * Descriptions for the roles.
 */
export const ROLES_DESCRIPTION = [
  'Wyświetlanie listy użytkowników',
  'Tworzenie nowych użytkowników'
]

/**
 * The editor of the user data.
 */
@Component({
  selector: 'app-user-editor',
  templateUrl: './user-creator.component.html',
  styleUrls: ['./user-creator.component.scss']
})
export class UserCreatorComponent implements OnInit {

  public roles: string[];
  public rolesDescriptions: string[];

  @Input()
  public userName: string;

  @Input()
  public password: string;

  @Input()
  public rolesSelection: boolean[];

  public constructor(
    private router: Router,
    private userService: UserService,
    private messagesService: MessagesService
  ) { }

  public ngOnInit() {
    this.roles = [];
    this.rolesDescriptions = [];
    this.rolesSelection = [];

    for (let i in ROLES) {
      this.roles.push(ROLES[i]);
      this.rolesSelection.push(false);
      this.rolesDescriptions.push(ROLES_DESCRIPTION[i])
    }
  }

  /**
   * A callback function for the submit button of the form for creating a new user.
   */
  public createOnClick(): void {
    let selectedRoles: string[] = [];

    for (let i in this.rolesSelection) {
      if (this.rolesSelection[i]) {
        selectedRoles.push(ROLES[i]);
      }
    }

    this.userService.createNewUser(this.userName, this.password, selectedRoles)
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.messagesService.showMessage('Użytkownik dodany!', MessageLevel.INFO);
          this.router.navigate(['users', 'list']);
        }
      });
  }

}
