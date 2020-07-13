import { HttpClientTestingModule, HttpTestingController, TestRequest } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { MSG_APP_ERROR } from 'src/app/core/constants/core.messages';
import { MessageLevel } from 'src/app/core/model/message-level';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessagesService } from 'src/app/core/services/messages.service';
import {
  URL_MY_CAMPAIGNS_LIST,
  URL_MY_CAMPAIGNS_START
} from '../../constants/my-campaigns.constants';
import { MyCampaignsListElement, MyCampaignsListResponse } from '../../model/my-campaigns-list-response.model';
import { MyCampaignsStartRequest } from '../../model/my-campaigns-start-request.model';
import { MyCampaignsStartResponse } from '../../model/my-campaigns-start-response.model';
import { MyCampaignsAdapterService } from './my-campaigns-adapter.service';

describe('MyCampaignsAdapterService', () => {

  // dependencies
  let httpTestingController: HttpTestingController;
  let messageService: MessagesService;

  // the service under test
  let myCampaignsService: MyCampaignsAdapterService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ]
    });

    httpTestingController = TestBed.get(HttpTestingController);
    messageService = TestBed.get(MessagesService);
    myCampaignsService = TestBed.get(MyCampaignsAdapterService);
  });

  it('should be created', () => {
    // then
    expect(myCampaignsService).toBeTruthy();
  });

  describe('getMyCampaignsList', () => {

    // test data
    let campaign1: MyCampaignsListElement = new MyCampaignsListElement();
    campaign1.id = 1;
    campaign1.campaignName = 'Campaign 1';

    let campaign2: MyCampaignsListElement = new MyCampaignsListElement();
    campaign2.id = 2;
    campaign2.campaignName = 'Campaign 2';

    let myCampaignsList: MyCampaignsListElement[] = [
      campaign1,
      campaign2
    ]

    let responseBodySuccess: MyCampaignsListResponse = new MyCampaignsListResponse();
    responseBodySuccess.status = RequestStatus.SUCCESS;
    responseBodySuccess.message = '';
    responseBodySuccess.myCampaigns = myCampaignsList;

    let responseBodyFailure: MyCampaignsListResponse = new MyCampaignsListResponse();
    responseBodyFailure.status = RequestStatus.FAILURE;
    responseBodyFailure.message = 'Test error message';

    it('should return a list of campaigns belonging to the currently logged in game master', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.getMyCampaignsList()
        .subscribe(response => expect(response).toEqual(myCampaignsList));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.flush(responseBodySuccess);

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
      request.flush(responseBodyFailure);

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalledWith(responseBodyFailure.message, MessageLevel.ERROR);
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

  describe('startCampaign', () => {

    // test data
    let campaignName: string = 'Test campaign';
    let beginDate: string = '2053-11-18';

    let requestBody: MyCampaignsStartRequest = new MyCampaignsStartRequest();
    requestBody.campaignName = campaignName;
    requestBody.beginDate = beginDate;

    let responseBodySuccess: MyCampaignsStartResponse = new MyCampaignsStartResponse();
    responseBodySuccess.status = RequestStatus.SUCCESS;

    let responseBodyFailure: MyCampaignsStartResponse = new MyCampaignsStartResponse();
    responseBodyFailure.status = RequestStatus.FAILURE;
    responseBodyFailure.message = 'Error message';

    it('should send a request for starting a new campaign', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.startCampaign(campaignName, beginDate)
        .subscribe(response => expect(response).toEqual(RequestStatus.SUCCESS));

      let testRequest: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_START);
      testRequest.flush(responseBodySuccess);

      httpTestingController.verify();
      expect(testRequest.request.body).toEqual(requestBody);
      expect(messageService.showMessage).not.toHaveBeenCalled();
    });

    it('should return the status failure', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.startCampaign(campaignName, beginDate)
        .subscribe(response => expect(response).toEqual(RequestStatus.FAILURE));

      let testRequest: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_START);
      testRequest.flush(responseBodyFailure);

      httpTestingController.verify();
      expect(testRequest.request.body).toEqual(requestBody);
      expect(messageService.showMessage).toHaveBeenCalledWith(responseBodyFailure.message, MessageLevel.ERROR);
    });

    it('should process an HTTP error', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      myCampaignsService.startCampaign(campaignName, beginDate)
        .subscribe(response => expect(response).toEqual(RequestStatus.FAILURE));

      let testRequest: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_START);
      testRequest.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(testRequest.request.body).toEqual(requestBody);
      expect(messageService.showMessage).toHaveBeenCalledWith(MSG_APP_ERROR, MessageLevel.ERROR);
    });
  });
});
