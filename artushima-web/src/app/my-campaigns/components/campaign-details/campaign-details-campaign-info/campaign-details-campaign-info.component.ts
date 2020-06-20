import { Component, Input } from '@angular/core';

/**
 * The child component showing basic information of a campaign.
 */
@Component({
  selector: 'app-campaign-details-campaign-info',
  templateUrl: './campaign-details-campaign-info.component.html',
  styleUrls: ['./campaign-details-campaign-info.component.scss']
})
export class CampaignDetailsCampaignInfoComponent {

  /**
   * The campaign title.
   */
  @Input()
  public campaignTitle: string;

  /**
   * The campaign ID.
   */
  @Input()
  public campaignId: number;

  /**
   * The date of campaign creation.
   */
  @Input()
  public campaignCreatedOn: Date;
}
