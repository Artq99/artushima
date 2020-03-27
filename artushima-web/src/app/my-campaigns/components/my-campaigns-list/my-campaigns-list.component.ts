import { Component, OnInit } from '@angular/core';

import { AuthService } from 'src/app/core/services/auth.service';
import { MyCampaignsService } from '../../services/my-campaigns.service';

import { MyCampaignsListElement } from '../../model/my-campaigns-list-element';

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
   * The role allowing a user to start a campaign.
   */
  public hasRoleStartCampaign: boolean = false;

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
    private authService: AuthService,
    private myCampaignsService: MyCampaignsService
  ) { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    this.resolveRoles();
    this.loadMyCampaigns();
  }

  /**
   * Sets the values of the currently logged-in user's roles. They determine
   * if some elements of the component should be rendered.
   */
  public resolveRoles(): void {
    this.hasRoleStartCampaign = this.authService.hasUserGotRoles(['role_start_campaign']);
  }

  /**
   * Loads the campaigns from the backend.
   */
  private loadMyCampaigns(): void {
    this.myCampaignsService.getMyCampaignsList()
      .subscribe(response => this.myCampaigns = response);
  }

}
