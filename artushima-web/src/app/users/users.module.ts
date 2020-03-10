import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserListComponent } from './components/user-list/user-list.component';
import { UserEditorComponent } from './components/user-editor/user-editor.component';

/**
 * The feature module containing functionalities related to user management.
 */
@NgModule({
  declarations: [
    UserListComponent,
    UserEditorComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    UserListComponent
  ]
})
export class UsersModule { }
