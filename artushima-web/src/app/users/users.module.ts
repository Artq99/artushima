import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { UserListComponent } from './components/user-list/user-list.component';
import { UserCreatorComponent } from './components/user-creator/user-creator.component';

/**
 * The feature module containing functionalities related to user management.
 */
@NgModule({
  declarations: [
    UserListComponent,
    UserCreatorComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  exports: [
    UserListComponent
  ]
})
export class UsersModule { }
