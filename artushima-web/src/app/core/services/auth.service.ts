import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject, BehaviorSubject } from 'rxjs';
import { first } from 'rxjs/operators';

import { MessagesService } from './messages.service';

import { RequestStatus } from 'src/app/core/model/request-status';
import { AuthLoginRequest } from 'src/app/core/model/auth-login-request';
import { AuthLoginResponse } from 'src/app/core/model/auth-login-response';
import { AuthLogoutResponse } from 'src/app/core/model/auth-logout-response';
import { CurrentUser } from 'src/app/core/model/current-user';
import { DecodedToken } from 'src/app/core/model/decoded-token';
import { MessageLevel } from 'src/app/core/model/message-level';

export const URL_AUTH_LOGIN = '/api/auth/login';
export const URL_AUTH_LOGOUT = '/api/auth/logout';
export const KEY_CURRENT_USER = 'currentUser';
export const DEFAULT_POST_AUTH_REDIRECT_ROUTE = 'dashboard';
export const MSG_LOGIN = 'Zalogowano: ';
export const MSG_LOGOUT = 'Wylogowano: ';
export const MSG_AUTH_ERROR = 'Błąd autentykacji.';

/**
 * A service for the user authentication management.
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private redirectRoute: string;
  private currentUserBehaviorSubject: BehaviorSubject<CurrentUser>;

  /**
   * The Observable that provides data of the currently logged in user.
   */
  public currentUser$: Observable<CurrentUser>;

  public constructor(
    private httpClient: HttpClient,
    private messagesService: MessagesService
  ) {
    this.currentUserBehaviorSubject = new BehaviorSubject(this.getCurrentUserFromLocalStorage());
    this.currentUser$ = this.currentUserBehaviorSubject.asObservable();
  }

  public get postAuthRedirectRoute() {

    let route = this.redirectRoute;
    if (route === undefined) {
      return DEFAULT_POST_AUTH_REDIRECT_ROUTE;
    } else {
      this.redirectRoute = undefined;
      return route;
    }
  }

  public set postAuthRedirectRoute(route: string) {

    this.redirectRoute = route;
  }

  /**
   * Indicates the state of the user authentication.
   *
   * @returns true if the user has been authenticated, false otherwise
   */
  public isUserLoggedIn(): boolean {

    let decodedToken: DecodedToken = this.getDecodedToken();

    if (decodedToken === undefined) {
      return false;
    }

    if (this.checkIfTokenExpired(decodedToken)) {
      this.clearCurrentUser();
      return false;
    }

    return true;
  }

  /**
   * Checks if the currently logged in user has the required roles.
   *
   * @param requiredRoles a list with the roles that allow authentication
   *
   * @returns true if the user has one of the required roles, false otherwise
   */
  public hasUserGotRoles(requiredRoles: string[]): boolean {

    if (requiredRoles === undefined) {
      return true;
    }

    let currentUser: CurrentUser = this.getCurrentUserFromLocalStorage();

    if (currentUser === undefined) {
      return false;
    }

    let result: boolean = false;

    currentUser.roles.forEach((role) => {
      if (requiredRoles.includes(role)) {
        result = true;
      }
    });

    return result;
  }

  /**
   * Validates, if the authentication token in the local storage has not
   * expired.
   */
  public validateInitialLogin(): void {

    let decodedToken: DecodedToken = this.getDecodedToken();

    if ((decodedToken !== undefined) && (this.checkIfTokenExpired(decodedToken))) {
      this.clearCurrentUser();
    }
  }

  /**
   * Returns the authentication token of the currently logged in user.
   *
   * @returns the authentication token
   */
  public getAuthToken(): string {

    let currentUser: CurrentUser = this.getCurrentUserFromLocalStorage();

    if (currentUser !== undefined) {
      return currentUser.token;
    } else {
      return undefined;
    }
  }

  /**
   * Sends a request to the backend to authenticate a user.
   *
   * @param userName the user's name
   * @param password the user's password
   *
   * @returns an observable emitting the request status
   */
  public login(userName: string, password: string): Observable<RequestStatus> {

    let requestBody: AuthLoginRequest = new AuthLoginRequest(userName, password);
    let authLogin$: Observable<AuthLoginResponse> = this.createAuthLogin$(requestBody);

    let responseSubject: Subject<RequestStatus> = new Subject<RequestStatus>();
    let response$: Observable<RequestStatus> = responseSubject.asObservable();

    authLogin$
      .pipe(first())
      .subscribe(
        response => {
          if (response.status === RequestStatus.SUCCESS) {
            this.setCurrentUser(response.currentUser);
            this.messagesService.showMessage(`${MSG_LOGIN}${response.currentUser.userName}`, MessageLevel.INFO);
          } else {
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }

          responseSubject.next(response.status);
          responseSubject.complete();
        },
        error => {
          this.messagesService.showMessage(MSG_AUTH_ERROR, MessageLevel.ERROR);
          responseSubject.next(RequestStatus.FAILURE);
          responseSubject.complete();
        });

    return response$;
  }

  /**
   * Sends a request to the backend to blacklist the current user's token
   * and removes it from the local storage.
   *
   * @returns an observable emitting the request status
   */
  public logout(): Observable<RequestStatus> {

    let authLogut$ = this.createAuthLogout$();

    let responseSubject: Subject<RequestStatus> = new Subject<RequestStatus>();
    let response$: Observable<RequestStatus> = responseSubject.asObservable();

    authLogut$
      .pipe(first())
      .subscribe(
        response => {
          if (response.status === RequestStatus.SUCCESS) {
            this.messagesService.showMessage(
              `${MSG_LOGOUT}${this.getCurrentUserFromLocalStorage().userName}`,
              MessageLevel.INFO
            );
            this.clearCurrentUser();
          } else {
            this.messagesService.showMessage(response.message, MessageLevel.ERROR);
          }

          responseSubject.next(response.status);
          responseSubject.complete()
        },
        error => {
          this.messagesService.showMessage(MSG_AUTH_ERROR, MessageLevel.ERROR);
          responseSubject.next(RequestStatus.FAILURE);
          responseSubject.complete();
        }
      );

    return response$;
  }

  private setCurrentUser(currentUser: CurrentUser): void {

    localStorage.setItem(KEY_CURRENT_USER, JSON.stringify(currentUser));
    this.currentUserBehaviorSubject.next(currentUser);
  }

  private clearCurrentUser(): void {

    localStorage.removeItem(KEY_CURRENT_USER);
    this.currentUserBehaviorSubject.next(undefined);
  }

  private createAuthLogin$(requestBody: AuthLoginRequest): Observable<AuthLoginResponse> {

    return this.httpClient.post<AuthLoginResponse>(URL_AUTH_LOGIN, requestBody);
  }

  private createAuthLogout$() {

    return this.httpClient.post<AuthLogoutResponse>(URL_AUTH_LOGOUT, {});
  }

  private getCurrentUserFromLocalStorage(): CurrentUser {

    let currentUser: CurrentUser = JSON.parse(localStorage.getItem('currentUser'));

    if (currentUser === null) {
      return undefined;
    }

    return currentUser;
  }

  private getDecodedToken(): DecodedToken {

    let currentUser: CurrentUser = this.getCurrentUserFromLocalStorage();

    if (currentUser === undefined) {
      return undefined;
    }

    return new DecodedToken(currentUser.token);
  }

  private checkIfTokenExpired(token: DecodedToken): boolean {

    let now: Date = new Date();

    if (token.exp.valueOf() < now.valueOf()) {
      return true;
    } else {
      return false;
    }
  }

}
