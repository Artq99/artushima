import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { NavbarComponent } from './components/navbar/navbar.component';

/**
 * A module containing core application functionalities, including singleton
 * services, guards, interceptors and general purpose components, like navbar.
 */
@NgModule({
  declarations: [
    NavbarComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    HttpClientModule,
    FontAwesomeModule
  ],
  exports: [
    NavbarComponent
  ]
})
export class CoreModule { }
