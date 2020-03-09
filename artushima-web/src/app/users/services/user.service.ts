import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { first } from 'rxjs/operators';

import { MessagesService } from 'src/app/core/services/messages.service';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { UsersListResponse } from '../model/users-list-response';
import { User } from '../model/user';

export const URL_USERS_LIST = '/api/users/list';

export const MSG_APP_ERROR = 'Błąd aplikacji.';

/**
 * The service for user management.
 */
@Injectable({
  providedIn: 'root'
})
export class UserService {

  public constructor(
    private httpClient: HttpClient,
    private messagesService: MessagesService
  ) { }

  /**
   * Returns the list of all users.
   *
   * @returns an observable emitting the list of all users
   */
  public getUserList(): Observable<User[]> {

    let usersList$: Observable<UsersListResponse> = this.createUsersList$();

    let responseSubject: Subject<User[]> = new Subject<User[]>();
    let response$: Observable<User[]> = responseSubject.asObservable();

    usersList$
      .pipe(first())
      .subscribe(
        response => {
          if (response.status === RequestStatus.SUCCESS) {
            responseSubject.next(response.users);
          } else {
            responseSubject.next([]);
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }
          responseSubject.complete();
        },
        () => {
          responseSubject.next([]);
          responseSubject.complete();
          this.messagesService.showMessage(MSG_APP_ERROR, MessageLevel.ERROR);
        }
      );

    return response$;
  }

  private createUsersList$(): Observable<UsersListResponse> {

    return this.httpClient.get<UsersListResponse>(URL_USERS_LIST);
  }
}
