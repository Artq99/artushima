import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { first } from 'rxjs/operators';

import { MessagesService } from 'src/app/core/services/messages.service';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { UsersListResponse } from '../model/users-list-response';
import { User } from '../model/user';
import { UsersAddResponse } from '../model/users-add-response';
import { UsersAddRequest } from '../model/users-add-request';

export const URL_USERS_LIST = '/api/users/list';
export const URL_USERS_ADD = '/api/users/add';

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

  public createNewUser(userName: string, password: string, roles: string[]): Observable<RequestStatus> {

    let request: UsersAddRequest = new UsersAddRequest();
    request.userName = userName;
    request.password = password;
    request.roles = roles;

    let usersAdd$: Observable<UsersAddResponse> = this.createUsersAdd$(request);

    let responseSubject: Subject<RequestStatus> = new Subject<RequestStatus>();
    let response$: Observable<RequestStatus> = responseSubject.asObservable();

    usersAdd$
      .pipe(first())
      .subscribe(
        response => {
          responseSubject.next(response.status);
          responseSubject.complete()

          if (response.status === RequestStatus.FAILURE) {
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }
        },
        () => {
          responseSubject.next(RequestStatus.FAILURE);
          responseSubject.complete()
          this.messagesService.showMessage(MSG_APP_ERROR, MessageLevel.ERROR);
        }
      );

    return response$;
  }

  private createUsersList$(): Observable<UsersListResponse> {

    return this.httpClient.get<UsersListResponse>(URL_USERS_LIST);
  }

  private createUsersAdd$(request: UsersAddRequest): Observable<UsersAddResponse> {

    return this.httpClient.post<UsersAddResponse>(URL_USERS_ADD, request);
  }
}
