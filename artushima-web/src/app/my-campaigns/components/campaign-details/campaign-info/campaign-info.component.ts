import { Component, Input } from '@angular/core';
import { faCalendarPlus, faCrown, faHashtag, IconDefinition } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component showing basic information of a campaign.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-info',
  templateUrl: './campaign-info.component.html',
  styleUrls: ['./campaign-info.component.scss']
})
export class CampaignInfoComponent {

  /** The hashtag icon. */
  public iconHashtag: IconDefinition = faHashtag;

  /** The calendar icon. */
  public iconCalendar: IconDefinition = faCalendarPlus;

  /** The game master icon. */
  public iconGM: IconDefinition = faCrown;

  /** The campaign ID. */
  @Input()
  public campaignId: number;

  /** The date of campaign creation. */
  @Input()
  public campaignCreatedOn: Date;

  /** Campaign game master. */
  @Input()
  public campaignGM: string;
}
