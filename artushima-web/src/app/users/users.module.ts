import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserListComponent } from './components/user-list/user-list.component';

/**
 * The feature module containing functionalities related to user management.
 */
@NgModule({
  declarations: [UserListComponent],
  imports: [
    CommonModule
  ],
  exports: [
    UserListComponent
  ]
})
export class UsersModule { }
