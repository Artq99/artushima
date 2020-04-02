import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { first } from 'rxjs/operators';

import { MessagesService } from 'src/app/core/services/messages.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import {
  MyCampaignsListElement,
  MyCampaignsListResponse,
  MyCampaignsStartRequest,
  MyCampaignsStartResponse
} from '../model/my-campaigns.model';

/**
 * The URL of the endpoint providing with the list of the campaigns belonging
 * to the currently logged in game master.
 */
export const URL_MY_CAMPAIGNS_LIST = '/api/my_campaigns/list';

/**
 * The URL of the endpoint creating a new campaign with the currently
 * logged-in user as the game master.
 */
export const URL_MY_CAMPAIGNS_START = '/api/my_campaigns/start';

/**
 * The message shown on application error.
 */
export const MSG_APP_ERROR = 'Błąd aplikacji.';

/**
 * The service with logic behind campaigns from the GM's point of view.
 */
@Injectable({
  providedIn: 'root'
})
export class MyCampaignsService {

  public constructor(
    private httpClient: HttpClient,
    private messagesService: MessagesService
  ) { }

  /**
   * Get the list of campaigns belonging to the currently logged in game master.
   *
   * @returns an observable emitting the list of campaigns
   */
  public getMyCampaignsList(): Observable<MyCampaignsListElement[]> {
    let myCampaignsList$: Observable<MyCampaignsListResponse> =
      this.httpClient.get<MyCampaignsListResponse>(URL_MY_CAMPAIGNS_LIST);
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
