import { Component, Input } from '@angular/core';
import { IconDefinition, faBook, faCalendarPlus, faHashtag } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component showing basic information of a campaign.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-info',
  templateUrl: './campaign-info.component.html',
  styleUrls: ['./campaign-info.component.scss']
})
export class CampaignInfoComponent {

  /** The book icon. */
  public iconBook: IconDefinition = faBook;

  /** The hashtag icon. */
  public iconHashtag: IconDefinition = faHashtag;

  /** The calendar icon. */
  public iconCalendar: IconDefinition = faCalendarPlus;

  /** The campaign title. */
  @Input()
  public campaignTitle: string;

  /** The campaign ID. */
  @Input()
  public campaignId: number;

  /** The date of campaign creation. */
  @Input()
  public campaignCreatedOn: Date;
}
