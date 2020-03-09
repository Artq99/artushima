import { Component, OnInit } from '@angular/core';

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

  private users: User[] = [];

  public constructor(private userService: UserService) { }

  public ngOnInit() {
    this.userService.getUserList()
      .subscribe(response => this.users = response);
  }

}
