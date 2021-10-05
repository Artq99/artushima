import { Component, Input, OnInit } from '@angular/core';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faFeatherAlt } from '@fortawesome/free-solid-svg-icons';

/**
 * Toolbar with tools for the game master of the campaign.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-gm-toolbar',
  templateUrl: './campaign-gm-toolbar.component.html'
})
export class CampaignGmToolbarComponent implements OnInit {

  /** Campaign ID */
  @Input()
  public campaignId: number;

  /** The icon for the button leading to the session summary creator. */
  public iconSummarizeSession: IconDefinition = faFeatherAlt;

  public createTimelineEntryURL: string;

  public ngOnInit() {
    this.createTimelineEntryURL = `/my_campaigns/${this.campaignId}/timeline/entry`;
  }
}
