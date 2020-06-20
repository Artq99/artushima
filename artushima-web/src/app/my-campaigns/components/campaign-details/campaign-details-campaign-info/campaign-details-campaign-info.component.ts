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

  @Input()
  public campaignTitle: string;

  @Input()
  public campaignId: number;

  @Input()
  public campaignCreatedOn: Date;
}
