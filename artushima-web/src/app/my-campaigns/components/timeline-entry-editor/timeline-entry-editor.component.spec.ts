import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { async, ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { MessageLevel } from 'src/app/core/model/message-level';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessagesService } from 'src/app/core/services/messages.service';
import { SharedModule } from 'src/app/shared/shared.module';
import { MSG_TIMELINE_ENTRY_CREATED } from '../../constants/my-campaings.messages';
import { TimelineEntryModel } from '../../model/timeline-entry.model';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service/my-campaigns-adapter.service';
import { TimelineEntryEditorComponent } from './timeline-entry-editor.component';

@Component({
  template: '',
})
class MockCampaignDetailsComponent {}

describe('TimelineEntryEditorComponent', () => {
  let component: TimelineEntryEditorComponent;
  let fixture: ComponentFixture<TimelineEntryEditorComponent>;
  let activatedRoute: ActivatedRoute;
  let adapterMock: jasmine.SpyObj<MyCampaignsAdapterService>;
  let messagesServiceMock: jasmine.SpyObj<MessagesService>;
  let router: Router;
  let location: Location;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        RouterTestingModule.withRoutes([
          { path: 'my_campaigns/campaign_details/:id', component: MockCampaignDetailsComponent },
        ]),
        SharedModule,
      ],
      providers: [
        {
          provide: MyCampaignsAdapterService,
          useValue: jasmine.createSpyObj('MyCampaignsAdapterService', ['createTimelineEntry']),
        },
        {
          provide: MessagesService,
          useValue: jasmine.createSpyObj('MessagesService', ['showMessage']),
        },
      ],
      declarations: [TimelineEntryEditorComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimelineEntryEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    activatedRoute = TestBed.inject(ActivatedRoute);
    adapterMock = TestBed.inject(MyCampaignsAdapterService) as jasmine.SpyObj<MyCampaignsAdapterService>;
    messagesServiceMock = TestBed.inject(MessagesService) as jasmine.SpyObj<MessagesService>;
    router = TestBed.inject(Router);
    location = TestBed.inject(Location);

    fixture.ngZone.run(() => router.initialNavigation());
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  describe('onSubmit', () => {
    it('should send a request and show a message', fakeAsync(() => {
      fixture.ngZone.run(() => {
        // given
        const campaignId: number = 99;
        const timelineEntry: TimelineEntryModel = {
          title: 'Test title',
          sessionDate: '2020-01-01',
          summaryText: 'Text text',
        } as TimelineEntryModel;

        component.entryFormGroup.controls['title'].setValue(timelineEntry.title);
        component.entryFormGroup.controls['sessionDate'].setValue(timelineEntry.sessionDate);
        component.entryFormGroup.controls['summaryText'].setValue(timelineEntry.summaryText);

        spyOn(activatedRoute.snapshot.paramMap, 'get').and.returnValue(`${campaignId}`);
        component.ngOnInit();
        adapterMock.createTimelineEntry.and.returnValue(of(RequestStatus.SUCCESS));

        // when
        component.onSubmit();
        tick();

        // then
        expect(adapterMock.createTimelineEntry).toHaveBeenCalledWith(campaignId, timelineEntry);
        expect(messagesServiceMock.showMessage).toHaveBeenCalledWith(MSG_TIMELINE_ENTRY_CREATED, MessageLevel.INFO);
        expect(location.path()).toEqual('/my_campaigns/campaign_details/99');
      });
    }));
  });
});
