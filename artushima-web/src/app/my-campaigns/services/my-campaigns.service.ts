import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { first } from 'rxjs/operators';

import { MessagesService } from 'src/app/core/services/messages.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { MyCampaignsListElement } from '../model/my-campaigns-list-element';
import { MyCampaignsListResponse } from '../model/my-campaigns-list-response';

/**
 * The URL of the endpoint providing with the list of the campaigns belonging
 * to the currently logged in game master.
 */
export const URL_MY_CAMPAIGNS_LIST = '/api/my_campaigns/list';

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
}
