import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from '../shared/shared.module';

// Components
import { MyCampaignsListComponent } from './components/my-campaigns-list/my-campaigns-list.component';
import { StartCampaignComponent } from './components/start-campaign/start-campaign.component';
import { CampaignDetailsComponent } from './components/campaign-details/campaign-details.component';
import { CampaignInfoComponent } from './components/campaign-details/campaign-info/campaign-info.component';
import { GmInfoComponent } from './components/campaign-details/gm-info/gm-info.component';
import { InGameTimeInfoComponent } from './components/campaign-details/in-game-time-info/in-game-time-info.component';
import { CampaignTimelineComponent } from './components/campaign-details/campaign-timeline/campaign-timeline.component';
import { CampaignPlayersInfoComponent } from './components/campaign-details/campaign-players-info/campaign-players-info.component';

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
    CampaignInfoComponent,
    GmInfoComponent,
    InGameTimeInfoComponent,
    CampaignTimelineComponent,
    CampaignPlayersInfoComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    FontAwesomeModule,
    SharedModule
  ]
})
export class MyCampaignsModule { }
