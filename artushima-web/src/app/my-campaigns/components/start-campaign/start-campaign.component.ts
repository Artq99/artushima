import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { MessagesService } from 'src/app/core/services/messages.service';
import { MyCampaignsService } from '../../services/my-campaigns.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';

/**
 * The default date for a campaign to begin with.
 * The date is the last mentioned date in the Neuroshima Handbook 1.5.
 */
export const DEFAULT_CAMPAIGN_START_DATE = '2053-11-18';

/**
 * The message displayed as a campaign has been successfuly created.
 */
export const MSG_CAMPAIGN_CREATED = 'Kampania została utworzona.';

/**
 * The component displaying a form for starting a new campaign with
 * the currently logged-in user as the game master.
 */
@Component({
  selector: 'app-start-campaign',
  templateUrl: './start-campaign.component.html',
  styleUrls: ['./start-campaign.component.scss']
})
export class StartCampaignComponent {

  @Input()
  public campaignName: string;

  @Input()
  public beginDate: string = DEFAULT_CAMPAIGN_START_DATE;

  /**
   * @inheritdoc
   *
   * @param router the router
   * @param messagesService the service for displaying messages
   * @param myCampaignsService the service for managing the GM's campaigns
   */
  public constructor(
    private router: Router,
    private messagesService: MessagesService,
    private myCampaignsService: MyCampaignsService
  ) { }

  /**
   * The callback function for the button 'start'.
   */
  public startOnClick(): void {
    this.myCampaignsService.startCampaign(this.campaignName, this.beginDate)
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.messagesService.showMessage(MSG_CAMPAIGN_CREATED, MessageLevel.INFO);
          // TODO: After the successful response the user should be redirected to the campaign's page.
          this.router.navigate(['my_campaigns', 'list']);
        }
      });
  }

}
