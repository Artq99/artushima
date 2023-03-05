import { Component, Input } from '@angular/core';
import { APP_ICON_CONFIG } from 'src/app/core/constants/icon-config';
import { TimelineEntryModel } from 'src/app/my-campaigns/model/timeline-entry.model';

/**
 * The child component showing the timeline of a campaign.
 *
 * @todo this is just a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-timeline',
  templateUrl: './campaign-timeline.component.html',
  styleUrls: ['./campaign-timeline.component.scss'],
})
export class CampaignTimelineComponent {
  /** Icon configuration. */
  public iconConfig = APP_ICON_CONFIG;

  /**
   * The campaign timeline.
   */
  @Input()
  public timeline: TimelineEntryModel[];
}
