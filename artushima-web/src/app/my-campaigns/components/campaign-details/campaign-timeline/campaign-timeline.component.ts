import { Component } from '@angular/core';
import { IconDefinition, faHistory } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component showing the timeline of a campaign.
 *
 * TODO this is just a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-timeline',
  templateUrl: './campaign-timeline.component.html',
  styleUrls: ['./campaign-timeline.component.scss']
})
export class CampaignTimelineComponent {

  /** The Icon: History. */
  public iconHistory: IconDefinition = faHistory;

}
