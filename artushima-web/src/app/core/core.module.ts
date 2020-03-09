import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { NavbarComponent } from './components/navbar/navbar.component';
import { MessagesComponent } from './components/messages/messages.component';
import { LoginComponent } from './components/login/login.component';

/**
 * A module containing core application functionalities, including singleton
 * services, guards, interceptors and general purpose components, like navbar.
 */
@NgModule({
  declarations: [
    NavbarComponent,
    MessagesComponent,
    LoginComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    HttpClientModule,
    FormsModule,
    FontAwesomeModule
  ],
  exports: [
    NavbarComponent,
    MessagesComponent,
    LoginComponent
  ]
})
export class CoreModule { }
