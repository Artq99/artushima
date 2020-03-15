import { TestBed } from '@angular/core/testing';
import { HttpTestingController, TestRequest, HttpClientTestingModule } from '@angular/common/http/testing';

import { MessagesService } from 'src/app/core/services/messages.service';
import { MyCampaignsService, URL_MY_CAMPAIGNS_LIST, MSG_APP_ERROR } from './my-campaigns.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { MyCampaignsListResponse } from '../model/my-campaigns-list-response';
import { MyCampaignsListElement } from '../model/my-campaigns-list-element';

describe('MyCampaignsService', () => {

  // dependencies
  let httpTestingController: HttpTestingController;
  let messageService: MessagesService;

  // the service under test
  let myCampaignsService: MyCampaignsService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });

    httpTestingController = TestBed.get(HttpTestingController);
    messageService = TestBed.get(MessagesService);
    myCampaignsService = TestBed.get(MyCampaignsService);
  });

  it('should be created', () => {
    // then
    expect(myCampaignsService).toBeTruthy();
  });

  describe('getMyCampaignsList', () => {

    // test data
    const CAMPAIGN_1 = new MyCampaignsListElement();
    CAMPAIGN_1.id = 1;
    CAMPAIGN_1.campaignName = 'Campaign 1';

    const CAMPAIGN_2 = new MyCampaignsListElement();
    CAMPAIGN_2.id = 2;
    CAMPAIGN_2.campaignName = 'Campaign 2';

    const MY_CAMPAIGNS_LIST = [
      CAMPAIGN_1,
      CAMPAIGN_2
    ]

    const RESPONSE_SUCCESS = new MyCampaignsListResponse();
    RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
    RESPONSE_SUCCESS.message = '';
    RESPONSE_SUCCESS.myCampaigns = MY_CAMPAIGNS_LIST;

    const RESPONSE_FAILURE = new MyCampaignsListResponse();
    RESPONSE_FAILURE.status = RequestStatus.FAILURE;
    RESPONSE_FAILURE.message = 'Test error message';

    it('should return a list of campaigns belonging to the currently logged in game master', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.getMyCampaignsList()
        .subscribe(response => expect(response).toEqual(MY_CAMPAIGNS_LIST));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.flush(RESPONSE_SUCCESS);

      httpTestingController.verify();
      expect(messageService.showMessage).not.toHaveBeenCalled();
    });

    it('should return an empty list, when the request status is a failure', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.getMyCampaignsList()
        .subscribe(response => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.flush(RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalledWith(RESPONSE_FAILURE.message, MessageLevel.ERROR);
    });

    it('should process an HTTP error', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.getMyCampaignsList()
        .subscribe(response => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify()
      expect(messageService.showMessage).toHaveBeenCalledWith(MSG_APP_ERROR, MessageLevel.ERROR);
    });
  });
});
