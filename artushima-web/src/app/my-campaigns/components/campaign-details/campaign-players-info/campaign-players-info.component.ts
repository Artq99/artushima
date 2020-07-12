import { Component } from '@angular/core';
import { faUsers, IconDefinition } from '@fortawesome/free-solid-svg-icons';

/**
 * The component displaying the information about users (players) participating
 * in the campaign.
 *
 * @todo This is a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-players-info',
  templateUrl: './campaign-players-info.component.html',
  styleUrls: ['./campaign-players-info.component.scss']
})
export class CampaignPlayersInfoComponent {

  /** The icon for the header. */
  public iconPlayers: IconDefinition = faUsers;
}
