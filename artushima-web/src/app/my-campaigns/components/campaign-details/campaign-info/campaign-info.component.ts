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

  /** The icon for the ID of a campaign. */
  public iconId: IconDefinition = faHashtag;

  /** The icon for the creation date of a campaign. */
  public iconCreationDate: IconDefinition = faCalendarPlus;

  /** The icon for the game master's name. */
  public iconGameMasterName: IconDefinition = faCrown;

  /** The ID of a campaign. */
  @Input()
  public id: number;

  /** The creation date of a campaign. */
  @Input()
  public creationDate: Date;

  /** The game master's name of a campaign. */
  @Input()
  public gameMasterName: string;
}
