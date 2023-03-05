import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { catchError, first, map, take, tap } from 'rxjs/operators';
import { API_CONFIG } from 'src/app/core/constants/api-config';
import { MSG_APP_ERROR } from 'src/app/core/constants/core.messages';
import { MessageLevel } from 'src/app/core/model/message-level';
import { RequestStatus } from 'src/app/core/model/request-status';
import { ResponseModel } from 'src/app/core/model/response.model';
import { MessagesService } from 'src/app/core/services/messages.service';
import {
  URL_MY_CAMPAIGNS_DETAILS,
  URL_MY_CAMPAIGNS_LIST,
  URL_MY_CAMPAIGNS_START,
} from '../../constants/my-campaigns.constants';
import { CampaignDetails, CampaignDetailsResponse } from '../../model/campaign-details.model';
import { MyCampaignsListElement, MyCampaignsListResponse } from '../../model/my-campaigns-list-response.model';
import { MyCampaignsStartRequest } from '../../model/my-campaigns-start-request.model';
import { MyCampaignsStartResponse } from '../../model/my-campaigns-start-response.model';
import { CreateTimelineEntryResponse, GetTimelineResponse, TimelineEntryModel } from '../../model/timeline-entry.model';

/**
 * The adapter-service for retrieving campaigns data from the backend.
 */
@Injectable({
  providedIn: 'root',
})
export class MyCampaignsAdapterService {
  /**
   * @inheritdoc
   *
   * @param httpClient the HTTP client
   * @param messagesService the service responsible for displaying messages
   */
  public constructor(private httpClient: HttpClient, private messagesService: MessagesService) {}

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

    myCampaignsList$.pipe(first()).subscribe(
      // on a valid response
      (response) => {
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
    request.beginDate = beginDate;

    // Creating the request object.
    let startCampaign$: Observable<MyCampaignsStartResponse> = this.httpClient.post<MyCampaignsStartResponse>(
      URL_MY_CAMPAIGNS_START,
      request
    );

    // Creating the response subject and observable.
    let responseSubject: Subject<RequestStatus> = new Subject<RequestStatus>();
    let response$: Observable<RequestStatus> = responseSubject.asObservable();

    startCampaign$.pipe(first()).subscribe(
      // on a valid response
      (response) => {
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

  /**
   * Sends a request for details of a campaign of the given ID.
   *
   * @param campaignId the ID of a campaign
   */
  public getCampaignDetails(campaignId: number): Observable<CampaignDetails> {
    const url: string = `${URL_MY_CAMPAIGNS_DETAILS}/${campaignId}`;
    return this.httpClient.get<CampaignDetailsResponse>(url).pipe(
      take(1),
      map((response) => {
        if (response.status === RequestStatus.SUCCESS) {
          return response.campaignDetails;
        } else {
          this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          return undefined;
        }
      }),
      catchError((error) => this.handleError(error))
    );
  }

  /**
   * Sends a POST request to create a timeline entry for a given campaign.
   *
   * @param campaignId the campaign ID
   * @param timelineEntry the timeline entry data
   * @returns Observable of the request status
   */
  public createTimelineEntry(campaignId: number, timelineEntry: TimelineEntryModel): Observable<RequestStatus> {
    const url = `${API_CONFIG.myCampaigns.endpoint}/${campaignId}${API_CONFIG.myCampaigns.timelineEntry}`;

    return this.httpClient.post<CreateTimelineEntryResponse>(url, timelineEntry).pipe(
      take(1),
      tap((r) => this.handleFailure(r)),
      map((r) => r.status),
      catchError((err) => this.handleError(err))
    );
  }

  /**
   * Sends a GET request to retrieve the timeline of a given campaign.
   *
   * @param campaignId the campaign ID
   * @returns Observable of the campaign timeline
   */
  public getTimeline(campaignId: number): Observable<TimelineEntryModel[]> {
    const url = `${API_CONFIG.myCampaigns.endpoint}/${campaignId}${API_CONFIG.myCampaigns.timeline}`;

    return this.httpClient.get<GetTimelineResponse>(url).pipe(
      take(1),
      tap((r) => this.handleFailure(r)),
      map((r) => (r.timeline ? r.timeline : [])),
      catchError((err) => this.handleError(err))
    );
  }

  /**
   * Shows the response message as an error if the request was not successful.
   *
   * @param response the backend response
   */
  private handleFailure(response: ResponseModel) {
    if (response.status !== RequestStatus.SUCCESS) {
      this.messagesService.showMessage(response.message, MessageLevel.ERROR);
    }
  }

  /**
   * Shows a message with an appropriate message and returns an observable of undefined.
   *
   * @param error an error
   */
  private handleError(error: any): Observable<any> {
    const message: string = error.error instanceof ErrorEvent ? 'Błąd przetwarzania odpowiedzi.' : 'Błąd aplikacji.';
    this.messagesService.showMessage(message, MessageLevel.ERROR);
    return of(undefined);
  }
}
