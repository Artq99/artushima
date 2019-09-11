import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NavbarComponent } from './components/navbar/navbar.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [NavbarComponent],
  imports: [
    CommonModule,
    FontAwesomeModule
  ],
  exports: [
    NavbarComponent
  ]
})
export class SharedModule { }
