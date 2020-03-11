import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DashboardComponent } from './components/dashboard/dashboard.component';

/**
 * The feature module containing the functionalities related to the dashboard
 * - the main page of the application.
 */
@NgModule({
  declarations: [DashboardComponent],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [
    DashboardComponent
  ]
})
export class DashboardModule { }
