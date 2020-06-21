import { Component, Input } from '@angular/core';
import { IconDefinition, faUserCircle } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component of the CampaignDetailsComponent, that shows the info on
 * the game master running the campaign.
 */
@Component({
  selector: 'artushima-campaign-details-gm-info',
  templateUrl: './gm-info.component.html',
  styleUrls: ['./gm-info.component.scss']
})
export class GmInfoComponent {

  /**
   * The icon that appears in front of the game master's name.
   */
  public iconGM: IconDefinition = faUserCircle;

  /**
   * The game master's name.
   */
  @Input()
  public gmName: string;
}
