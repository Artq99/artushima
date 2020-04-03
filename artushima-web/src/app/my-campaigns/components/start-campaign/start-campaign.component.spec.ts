import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, BehaviorSubject, Observable } from 'rxjs';

// Components
import { StartCampaignComponent } from './start-campaign.component';

// Services
import { MessagesService } from 'src/app/core/services/messages.service';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service';

// Constants
import { DEFAULT_CAMPAIGN_START_DATE } from '../../constants/my-campaigns.constants';
import { MSG_CAMPAIGN_CREATED } from '../../constants/my-campaings.messages';

// Model
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';

describe('StartCampaignComponent', () => {

  // The dependencies
  let router: Router;
  let messagesService: MessagesService;
  let myCampaignsAdapterService: MyCampaignsAdapterService;

  // The component under test
  let startCampaignComponent: StartCampaignComponent;

  // The fixture
  let fixture: ComponentFixture<StartCampaignComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        declarations: [
          StartCampaignComponent
        ],
        imports: [
          RouterTestingModule,
          HttpClientTestingModule,
          FormsModule
        ]
      })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StartCampaignComponent);
    router = TestBed.get(Router);
    messagesService = TestBed.get(MessagesService);
    myCampaignsAdapterService = TestBed.get(MyCampaignsAdapterService);

    startCampaignComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(startCampaignComponent).toBeTruthy();
  });

  describe('startOnClick', () => {

    // test data
    let campaignName: string = 'Test campaign';

    it('should navigate to the campaign list after a successful response', () => {
      // given
      let responseSubject: Subject<RequestStatus> = new BehaviorSubject<RequestStatus>(RequestStatus.SUCCESS);
      let response$: Observable<RequestStatus> = responseSubject.asObservable();

      spyOn(myCampaignsAdapterService, 'startCampaign')
        .and.returnValue(response$);
      spyOn(messagesService, 'showMessage');
      spyOn(router, 'navigate');

      startCampaignComponent.campaignName = campaignName;

      // when
      startCampaignComponent.startOnClick();

      // then
      expect(myCampaignsAdapterService.startCampaign).toHaveBeenCalledWith(campaignName, DEFAULT_CAMPAIGN_START_DATE);
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_CAMPAIGN_CREATED, MessageLevel.INFO);
      expect(router.navigate).toHaveBeenCalledWith(['my_campaigns', 'list']);
    });

    it('should not navigate anywhere if the response was unsuccessful', () => {
      // given
      let responseSubject: Subject<RequestStatus> = new BehaviorSubject<RequestStatus>(RequestStatus.FAILURE);
      let response$: Observable<RequestStatus> = responseSubject.asObservable();

      spyOn(myCampaignsAdapterService, 'startCampaign')
        .and.returnValue(response$);
      spyOn(messagesService, 'showMessage');
      spyOn(router, 'navigate');

      startCampaignComponent.campaignName = campaignName;

      // when
      startCampaignComponent.startOnClick();

      // then
      expect(myCampaignsAdapterService.startCampaign).toHaveBeenCalledWith(campaignName, DEFAULT_CAMPAIGN_START_DATE);
      expect(messagesService.showMessage).not.toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });
});
