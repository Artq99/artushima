import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { take } from 'rxjs/operators';
import { APP_ICON_CONFIG } from 'src/app/core/constants/icon-config';
import { MessageLevel } from 'src/app/core/model/message-level';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessagesService } from 'src/app/core/services/messages.service';
import { MSG_TIMELINE_ENTRY_CREATED } from '../../constants/my-campaings.messages';
import { TimelineEntryModel } from '../../model/timeline-entry.model';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service/my-campaigns-adapter.service';

/**
 * Editor for the entries of the campaign timeline.
 */
@Component({
  selector: 'artushima-timeline-entry-editor',
  templateUrl: './timeline-entry-editor.component.html',
  styles: [],
})
export class TimelineEntryEditorComponent implements OnInit {
  /** The campaign ID. */
  private campaignId: number;

  /** The form group for the new entry. */
  public entryFormGroup = new FormGroup({
    title: new FormControl('', [Validators.required]),
    sessionDate: new FormControl('', [Validators.required]),
    summaryText: new FormControl(''),
  });

  /** Icon configuration. */
  public iconConfig = APP_ICON_CONFIG;

  /**
   * @inheritdoc
   *
   * @param router the router
   * @param activatedRoute the activated route
   * @param myCampaignsAdapter the module adapter
   * @param messagesService the messages service
   */
  public constructor(
    private readonly router: Router,
    private readonly activatedRoute: ActivatedRoute,
    private readonly myCampaignsAdapter: MyCampaignsAdapterService,
    private readonly messagesService: MessagesService
  ) {}

  /**
   * @inheritdoc
   */
  public ngOnInit(): void {
    this.campaignId = +this.activatedRoute.snapshot.paramMap.get('id');
  }

  /**
   * The callback for the onSubmit event.
   */
  public onSubmit(): void {
    const timelineEntry = this.entryFormGroup.getRawValue() as TimelineEntryModel;
    this.myCampaignsAdapter
      .createTimelineEntry(this.campaignId, timelineEntry)
      .pipe(take(1))
      .subscribe((status: RequestStatus) => {
        if (status === RequestStatus.SUCCESS) {
          this.messagesService.showMessage(MSG_TIMELINE_ENTRY_CREATED, MessageLevel.INFO);
          this.router.navigate(['my_campaigns', 'campaign_details', `${this.campaignId}`]);
        }
      });
  }
}
