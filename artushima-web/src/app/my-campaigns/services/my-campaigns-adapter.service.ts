import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { first } from 'rxjs/operators';

// Services
import { MessagesService } from 'src/app/core/services/messages.service';

// Constants
import {
  URL_MY_CAMPAIGNS_LIST,
  URL_MY_CAMPAIGNS_START
} from '../constants/my-campaigns.constants';
import { MSG_APP_ERROR } from 'src/app/core/constants/core.messages';

// Model
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { MyCampaignsListElement, MyCampaignsListResponse } from '../model/my-campaigns-list-response.model';
import { MyCampaignsStartRequest } from '../model/my-campaigns-start-request.model';
import { MyCampaignsStartResponse } from '../model/my-campaigns-start-response.model';

/**
 * The adapter-service for retrieving campaigns data from the backend.
 */
@Injectable({
  providedIn: 'root'
})
export class MyCampaignsAdapterService {

  /**
   * @inheritdoc
   *
   * @param httpClient the HTTP client
   * @param messagesService the service responsible for displaying messages
   */
  public constructor(
    private httpClient: HttpClient,
    private messagesService: MessagesService
  ) { }

  /**
   * Returns the list of campaigns belonging to the currently logged in game master.
   *
   * @returns an observable emitting the list of campaigns
   */
  public getMyCampaignsList(): Observable<MyCampaignsListElement[]> {
    // Creating the request object.
    let myCampaignsList$: Observable<MyCampaignsListResponse> =
      this.httpClient.get<MyCampaignsListResponse>(URL_MY_CAMPAIGNS_LIST);

    // Creating the response subject and observable.
    let responseSubject: Subject<MyCampaignsListElement[]> = new Subject<MyCampaignsListElement[]>();
    let response$: Observable<MyCampaignsListElement[]> = responseSubject.asObservable();

    myCampaignsList$
      .pipe(first())
      .subscribe(
        // on a valid response
        response => {
          if (response.status === RequestStatus.SUCCESS) {
            responseSubject.next(response.myCampaigns);
          } else {
            responseSubject.next([]);
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }
          responseSubject.complete();
        },
        // on error
        () => {
          responseSubject.next([]);
          responseSubject.complete();
          this.messagesService.showMessage(MSG_APP_ERROR, MessageLevel.ERROR);
        }
      );

    return response$;
  }

  /**
   * Sends a request for starting a new campaign with the currently logged-in user as the game master.
   *
   * @param campaignName the name of the new campaign
   * @param beginDate the starting date of the new campaign
   * @returns an observable emitting the status of the finished request
   */
  public startCampaign(campaignName: string, beginDate: string): Observable<RequestStatus> {
    // Creating the request body.
    let request: MyCampaignsStartRequest = new MyCampaignsStartRequest();
    request.campaignName = campaignName;
    request.beginDate = beginDate

    // Creating the request object.
    let startCampaign$: Observable<MyCampaignsStartResponse> =
      this.httpClient.post<MyCampaignsStartResponse>(URL_MY_CAMPAIGNS_START, request);

    // Creating the response subject and observable.
    let responseSubject: Subject<RequestStatus> = new Subject<RequestStatus>();
    let response$: Observable<RequestStatus> = responseSubject.asObservable();

    startCampaign$
      .pipe(first())
      .subscribe(
        // on a valid response
        response => {
          if (response.status === RequestStatus.FAILURE) {
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }
          responseSubject.next(response.status);
          responseSubject.complete();
        },
        // on error
        () => {
          this.messagesService.showMessage(MSG_APP_ERROR, MessageLevel.ERROR);
          responseSubject.next(RequestStatus.FAILURE);
          responseSubject.complete();
        }
      );

    return response$;
  }
}