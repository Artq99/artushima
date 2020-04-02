import { Component, OnInit, Input } from '@angular/core';

/**
 * The default date for a campaign to begin with.
 * The date is the last mentioned date in the Neuroshima Handbook 1.5.
 */
export const DEFAULT_CAMPAIGN_START_DATE = "2053-11-18";

/**
 * The component displaying a form for starting a new campaign with
 * the currently logged-in user as the game master.
 */
@Component({
  selector: 'app-start-campaign',
  templateUrl: './start-campaign.component.html',
  styleUrls: ['./start-campaign.component.scss']
})
export class StartCampaignComponent implements OnInit {

  @Input()
  public campaignName: string;

  @Input()
  public beginDate: string = DEFAULT_CAMPAIGN_START_DATE;

  /**
   * @inheritdoc
   */
  public constructor() { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void { }

  /**
   * The callback function for the button 'start'.
   */
  public startOnClick(): void {
    console.log(this.campaignName);
    console.log(this.beginDate);
  }

}
