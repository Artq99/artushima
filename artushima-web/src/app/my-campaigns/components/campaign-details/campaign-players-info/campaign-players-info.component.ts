import { Component } from '@angular/core';
import { IconDefinition, faUsers } from '@fortawesome/free-solid-svg-icons';

/**
 * The component displaying the information about users (players) participating
 * in the campaign.
 *
 * This is a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-players-info',
  templateUrl: './campaign-players-info.component.html',
  styleUrls: ['./campaign-players-info.component.scss']
})
export class CampaignPlayersInfoComponent {

  /** The icon for users. */
  public iconPlayers: IconDefinition = faUsers;
}
