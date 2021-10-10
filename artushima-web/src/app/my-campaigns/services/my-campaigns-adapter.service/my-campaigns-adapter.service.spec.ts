import { HttpClientTestingModule, HttpTestingController, TestRequest } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { take } from 'rxjs/operators';
import { API_CONFIG } from 'src/app/core/constants/api-config';
import { MSG_APP_ERROR } from 'src/app/core/constants/core.messages';
import { MessageLevel } from 'src/app/core/model/message-level';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessagesService } from 'src/app/core/services/messages.service';
import {
  URL_MY_CAMPAIGNS_DETAILS,
  URL_MY_CAMPAIGNS_LIST,
  URL_MY_CAMPAIGNS_START,
} from '../../constants/my-campaigns.constants';
import { CampaignDetailsResponse } from '../../model/campaign-details.model';
import { MyCampaignsListElement, MyCampaignsListResponse } from '../../model/my-campaigns-list-response.model';
import { MyCampaignsStartRequest } from '../../model/my-campaigns-start-request.model';
import { MyCampaignsStartResponse } from '../../model/my-campaigns-start-response.model';
import { CreateTimelineEntryResponse, TimelineEntryModel } from '../../model/timeline-entry.model';
import { MyCampaignsAdapterService } from './my-campaigns-adapter.service';

describe('MyCampaignsAdapterService', () => {
  let service: MyCampaignsAdapterService;
  let httpTestingController: HttpTestingController;
  let messageService: MessagesService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });

    service = TestBed.inject(MyCampaignsAdapterService);
    httpTestingController = TestBed.inject(HttpTestingController);
    messageService = TestBed.inject(MessagesService);
  });

  it('should be created', () => {
    // then
    expect(service).toBeTruthy();
  });

  describe('getMyCampaignsList', () => {
    // test data
    let campaign1: MyCampaignsListElement = new MyCampaignsListElement();
    campaign1.id = 1;
    campaign1.campaignName = 'Campaign 1';

    let campaign2: MyCampaignsListElement = new MyCampaignsListElement();
    campaign2.id = 2;
    campaign2.campaignName = 'Campaign 2';

    let myCampaignsList: MyCampaignsListElement[] = [campaign1, campaign2];

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
      service.getMyCampaignsList().subscribe((response) => expect(response).toEqual(myCampaignsList));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.flush(responseBodySuccess);

      httpTestingController.verify();
      expect(messageService.showMessage).not.toHaveBeenCalled();
    });

    it('should return an empty list, when the request status is a failure', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      service.getMyCampaignsList().subscribe((response) => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.flush(responseBodyFailure);

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalledWith(responseBodyFailure.message, MessageLevel.ERROR);
    });

    it('should process an HTTP error', () => {
      // given
      spyOn(messageService, 'showMessage');

      // when then
      service.getMyCampaignsList().subscribe((response) => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_LIST);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
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
      service
        .startCampaign(campaignName, beginDate)
        .subscribe((response) => expect(response).toEqual(RequestStatus.SUCCESS));

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
      service
        .startCampaign(campaignName, beginDate)
        .subscribe((response) => expect(response).toEqual(RequestStatus.FAILURE));

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
      service
        .startCampaign(campaignName, beginDate)
        .subscribe((response) => expect(response).toEqual(RequestStatus.FAILURE));

      let testRequest: TestRequest = httpTestingController.expectOne(URL_MY_CAMPAIGNS_START);
      testRequest.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(testRequest.request.body).toEqual(requestBody);
      expect(messageService.showMessage).toHaveBeenCalledWith(MSG_APP_ERROR, MessageLevel.ERROR);
    });
  });

  describe('getCampaignDetails', () => {
    it('should get the details of a campaign', () => {
      // given
      const id: number = 99;
      const url: string = `${URL_MY_CAMPAIGNS_DETAILS}/${id}`;
      const campaignDetailsResponse: CampaignDetailsResponse = {
        status: RequestStatus.SUCCESS,
        message: '',
        campaignDetails: {
          id: 99,
          title: 'Test Campaign',
          creationDate: new Date(2020, 1, 1),
          startDate: new Date(2055, 1, 1),
          passedDays: 10,
          currentDate: new Date(2055, 1, 11),
          gameMasterId: 1,
          gameMasterName: 'Test GM',
        },
      };

      spyOn(messageService, 'showMessage');

      // when then
      service
        .getCampaignDetails(id)
        .subscribe((response) => expect(response).toEqual(campaignDetailsResponse.campaignDetails));

      const request: TestRequest = httpTestingController.expectOne(url);
      request.flush(campaignDetailsResponse);

      httpTestingController.verify();
      expect(messageService.showMessage).not.toHaveBeenCalled();
    });

    it('should show message when the request failed', () => {
      // given
      const id: number = 99;
      const url: string = `${URL_MY_CAMPAIGNS_DETAILS}/${id}`;
      const campaignDetailsResponse: CampaignDetailsResponse = {
        status: RequestStatus.FAILURE,
        message: 'Test Message',
      };

      spyOn(messageService, 'showMessage');

      // when then
      service.getCampaignDetails(id).subscribe((response) => expect(response).not.toBeDefined());

      const request: TestRequest = httpTestingController.expectOne(url);
      request.flush(campaignDetailsResponse);

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalledWith(campaignDetailsResponse.message, MessageLevel.ERROR);
    });

    it('should process an HTTP error', () => {
      // given
      const id: number = 99;
      const url: string = `${URL_MY_CAMPAIGNS_DETAILS}/${id}`;

      spyOn(messageService, 'showMessage');

      // when then
      service.getCampaignDetails(id).subscribe((response) => expect(response).not.toBeDefined());

      const request: TestRequest = httpTestingController.expectOne(url);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalled();
    });
  });

  describe('createTimelineEntry', () => {
    it('should create a timeline entry', (done) => {
      // given
      const id: number = 99;
      const timelineEntry: TimelineEntryModel = {
        title: 'Test title',
        sessionDate: '2020-01-01',
        summaryText: 'Test text',
      } as TimelineEntryModel;
      const url: string = `${API_CONFIG.myCampaigns.endpoint}/${id}${API_CONFIG.myCampaigns.timelineEntry}`;
      const response: CreateTimelineEntryResponse = {
        status: RequestStatus.SUCCESS,
        message: '',
        campaignTimelineEntryId: 999,
      } as CreateTimelineEntryResponse;

      spyOn(messageService, 'showMessage');

      // when then
      service
        .createTimelineEntry(id, timelineEntry)
        .pipe(take(1))
        .subscribe((status) => {
          expect(status).toEqual(RequestStatus.SUCCESS);
          done();
        });

      const request: TestRequest = httpTestingController.expectOne(url);
      request.flush(response);

      httpTestingController.verify();
      expect(messageService.showMessage).not.toHaveBeenCalled();
    });

    it('should handle a failure', (done) => {
      // given
      const id: number = 99;
      const timelineEntry: TimelineEntryModel = {
        title: 'Test title',
        sessionDate: '2020-01-01',
        summaryText: 'Test text',
      } as TimelineEntryModel;
      const url: string = `${API_CONFIG.myCampaigns.endpoint}/${id}${API_CONFIG.myCampaigns.timelineEntry}`;
      const response: CreateTimelineEntryResponse = {
        status: RequestStatus.FAILURE,
        message: 'Test message',
      } as CreateTimelineEntryResponse;

      spyOn(messageService, 'showMessage');

      // when then
      service
        .createTimelineEntry(id, timelineEntry)
        .pipe(take(1))
        .subscribe((status) => {
          expect(status).toEqual(RequestStatus.FAILURE);
          done();
        });

      const request: TestRequest = httpTestingController.expectOne(url);
      request.flush(response);

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalledWith(response.message, MessageLevel.ERROR);
    });

    it('should handle an HTTP error', (done) => {
      // given
      const id: number = 99;
      const timelineEntry: TimelineEntryModel = {
        title: 'Test title',
        sessionDate: '2020-01-01',
        summaryText: 'Test text',
      } as TimelineEntryModel;
      const url: string = `${API_CONFIG.myCampaigns.endpoint}/${id}${API_CONFIG.myCampaigns.timelineEntry}`;

      spyOn(messageService, 'showMessage');

      // when then
      service
        .createTimelineEntry(id, timelineEntry)
        .pipe(take(1))
        .subscribe((response) => {
          expect(response).not.toBeDefined();
          done();
        });

      const request: TestRequest = httpTestingController.expectOne(url);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(messageService.showMessage).toHaveBeenCalled();
    });
  });
});
