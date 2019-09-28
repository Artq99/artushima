import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './components/login/login.component';

/**
 * The feature module containing authentication functionalities.
 */
@NgModule({
  declarations: [LoginComponent],
  imports: [
    CommonModule,
    FormsModule
  ],
  exports: [
    LoginComponent
  ]
})
export class AuthenticationModule { }
