import { Component } from '@angular/core';
import { faHistory, IconDefinition } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component showing the timeline of a campaign.
 *
 * @todo this is just a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-timeline',
  templateUrl: './campaign-timeline.component.html',
  styleUrls: ['./campaign-timeline.component.scss']
})
export class CampaignTimelineComponent {

  /** The icon for the header. */
  public iconHistory: IconDefinition = faHistory;

}
