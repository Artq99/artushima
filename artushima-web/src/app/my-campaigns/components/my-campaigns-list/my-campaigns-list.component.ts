import { Component, OnInit } from '@angular/core';
import { MyCampaignsListElement } from '../../model/my-campaigns-list-element';
import { MyCampaignsService } from '../../services/my-campaigns.service';

/**
 * The component showing the list of campaigns belonging to the game master.
 */
@Component({
  selector: 'app-my-campaigns-list',
  templateUrl: './my-campaigns-list.component.html',
  styleUrls: ['./my-campaigns-list.component.scss']
})
export class MyCampaignsListComponent implements OnInit {

  /**
   * The list of all campaigns belonging to the currently logged in game
   * master.
   */
  public myCampaigns: MyCampaignsListElement[] = [];

  /**
   * @inheritdoc
   *
   * @param myCampaignsService the my-campaigns service
   */
  public constructor(
    private myCampaignsService: MyCampaignsService
  ) { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    this.loadMyCampaigns();
  }

  /**
   * Loads the campaigns from the backend.
   */
  private loadMyCampaigns(): void {
    this.myCampaignsService.getMyCampaignsList()
      .subscribe(response => this.myCampaigns = response);
  }

}
