import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

// Components
import { MyCampaignsListComponent } from './components/my-campaigns-list/my-campaigns-list.component';
import { StartCampaignComponent } from './components/start-campaign/start-campaign.component';
import { CampaignDetailsComponent } from './components/campaign-details/campaign-details.component';
import { CampaignDetailsCampaignInfoComponent } from './components/campaign-details/campaign-details-campaign-info/campaign-details-campaign-info.component';
import { GmInfoComponent } from './components/campaign-details/gm-info/gm-info.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

/**
 * A feature module with functionalities for game masters.
 *
 * Enables the users with appropriate rights to view their campaigns, create
 * new ones and manage existing.
 */
@NgModule({
  declarations: [
    MyCampaignsListComponent,
    StartCampaignComponent,
    CampaignDetailsComponent,
    CampaignDetailsCampaignInfoComponent,
    GmInfoComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    FontAwesomeModule
  ]
})
export class MyCampaignsModule { }
