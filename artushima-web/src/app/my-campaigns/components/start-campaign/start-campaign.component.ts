import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

// Services
import { MessagesService } from 'src/app/core/services/messages.service';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service';

// Constants
import { DEFAULT_CAMPAIGN_START_DATE } from '../../constants/my-campaigns.constants';
import { MSG_CAMPAIGN_CREATED } from '../../constants/my-campaings.messages';

// Model
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';

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
   * @param myCampaignsAdapterService the adapter-service for retrieving
   *          the campaigns data from the backend
   */
  public constructor(
    private router: Router,
    private messagesService: MessagesService,
    private myCampaignsAdapterService: MyCampaignsAdapterService
  ) { }

  /**
   * The callback function for the button 'start'.
   */
  public startOnClick(): void {
    this.myCampaignsAdapterService.startCampaign(this.campaignName, this.beginDate)
      .subscribe(status => {
        if (status === RequestStatus.SUCCESS) {
          this.messagesService.showMessage(MSG_CAMPAIGN_CREATED, MessageLevel.INFO);
          // TODO: After the successful response the user should be redirected to the campaign's page.
          this.router.navigate(['my_campaigns', 'list']);
        }
      });
  }

}
