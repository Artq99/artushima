import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faBook, IconDefinition } from '@fortawesome/free-solid-svg-icons';
import { Observable } from 'rxjs';
import { CurrentUser } from 'src/app/core/model/current-user';
import { AuthService } from 'src/app/core/services/auth.service';
import { CampaignDetails } from '../../model/campaign-details.model';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service/my-campaigns-adapter.service';

/**
 * The component showing the details of a campaign.
 */
@Component({
  selector: 'artushima-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.scss']
})
export class CampaignDetailsComponent implements OnInit {

  /** The icon of a book for the header. */
  public iconBook: IconDefinition = faBook;

  /** The observable of the currently logged in user. */
  public currentUser$: Observable<CurrentUser>;

  /** The observable of the data. */
  public campaignDetails$: Observable<CampaignDetails>;

  /**
   * @inheritdoc
   *
   * @param router the router
   * @param activatedRoute the activated route
   */
  public constructor(
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private myCampaignsAdapterService: MyCampaignsAdapterService
  ) { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    const campaignId = +this.activatedRoute.snapshot.paramMap.get('id');
    this.currentUser$ = this.authService.currentUser$;
    this.campaignDetails$ = this.myCampaignsAdapterService.getCampaignDetails(campaignId);
  }
}
