import { Component, OnInit } from '@angular/core';

/**
 * The component displaying a form for starting a new campaign with
 * the currently logged-in user as a game master.
 */
@Component({
  selector: 'app-start-campaign',
  templateUrl: './start-campaign.component.html',
  styleUrls: ['./start-campaign.component.scss']
})
export class StartCampaignComponent implements OnInit {

  /**
   * @inheritdoc
   */
  public constructor() { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void { }

}
