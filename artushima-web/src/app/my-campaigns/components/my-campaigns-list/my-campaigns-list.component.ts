import { Component, OnInit } from '@angular/core';
import { faInfoCircle, IconDefinition } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from 'src/app/core/services/auth.service';
import { MyCampaignsListElement } from '../../model/my-campaigns-list-response.model';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service/my-campaigns-adapter.service';

/**
 * The component showing the list of campaigns belonging to the game master.
 */
@Component({
  selector: 'app-my-campaigns-list',
  templateUrl: './my-campaigns-list.component.html',
  styleUrls: ['./my-campaigns-list.component.scss']
})
export class MyCampaignsListComponent implements OnInit {

  /** The icon for the button leading to the campaign details. */
  public iconDetails: IconDefinition = faInfoCircle;

  /** The role allowing a user to start a campaign. */
  public hasRoleStartCampaign: boolean = false;

  /** The list of all campaigns belonging to the currently logged in game master. */
  public myCampaigns: MyCampaignsListElement[] = [];

  /**
   * @inheritdoc
   *
   * @param authService the service for user-authentication
   * @param myCampaignsAdapterService the my-campaigns adapter service for
   *          retrieving the campaigns data from the backend
   */
  public constructor(
    private authService: AuthService,
    private myCampaignsAdapterService: MyCampaignsAdapterService
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
    this.myCampaignsAdapterService.getMyCampaignsList()
      .subscribe(response => this.myCampaigns = response);
  }
}
