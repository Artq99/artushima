import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faBook, IconDefinition } from '@fortawesome/free-solid-svg-icons';

/**
 * The component showing the details of a campaign.
 *
 * @todo This is just a stub implementation.
 */
@Component({
  selector: 'artushima-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.scss']
})
export class CampaignDetailsComponent implements OnInit {

  /** The icon of a book for the header. */
  public iconBook: IconDefinition = faBook;

  /** The ID of the campaign. */
  private campaignId: number;

  /**
   * @inheritdoc
   *
   * @param router the router
   * @param activatedRoute the activated route
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
    // console.log(this.campaignId);
  }
}