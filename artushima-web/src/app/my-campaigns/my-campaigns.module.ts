import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyCampaignsListComponent } from './components/my-campaigns-list/my-campaigns-list.component';

/**
 * A feature module with functionalities for game masters.
 *
 * Enables the users with appropriate rights to view their campaigns, create
 * new ones and manage existing.
 */
@NgModule({
  declarations: [MyCampaignsListComponent],
  imports: [
    CommonModule
  ]
})
export class MyCampaignsModule { }
