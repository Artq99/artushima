import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

/**
 * The component showing campaign details.
 */
@Component({
  selector: 'app-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.scss']
})
export class CampaignDetailsComponent implements OnInit {

  /**
   * The ID of the campaign.
   */
  private campaignId: number;

  /**
   * @inheritdoc
   *
   * @param router the router
   * @param activatedRoute the activated route that led to this component
   */
  public constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) { }

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    this.campaignId = +this.activatedRoute.snapshot.paramMap.get('id');
    // TODO load the campaign of the given id
    console.log(this.campaignId);
  }
}
