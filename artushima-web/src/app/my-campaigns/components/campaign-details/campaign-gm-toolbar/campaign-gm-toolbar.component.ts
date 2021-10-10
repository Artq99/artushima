import { Component, Input, OnInit } from '@angular/core';
import { APP_ICON_CONFIG } from 'src/app/core/constants/icon-config';

/**
 * Toolbar with tools for the game master of the campaign.
 */
@Component({
  selector: 'artushima-campaign-details-campaign-gm-toolbar',
  templateUrl: './campaign-gm-toolbar.component.html',
})
export class CampaignGmToolbarComponent implements OnInit {
  /** The campaign ID. */
  @Input()
  public campaignId: number;

  /** Icon configuration. */
  public iconConfig = APP_ICON_CONFIG;

  public createTimelineEntryURL: string;

  public ngOnInit() {
    this.createTimelineEntryURL = `/my_campaigns/${this.campaignId}/timeline/entry`;
  }
}
