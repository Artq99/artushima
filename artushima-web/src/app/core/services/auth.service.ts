import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject, BehaviorSubject } from 'rxjs';
import { first } from 'rxjs/operators';

import { RequestStatus } from 'src/app/model/request-status';
import { AuthLoginRequest } from 'src/app/model/auth-login-request';
import { AuthLoginResponse } from 'src/app/model/auth-login-response';
import { AuthLogoutResponse } from 'src/app/model/auth-logout-response';
import { CurrentUser } from 'src/app/model/current-user';

export const URL_AUTH_LOGIN = '/api/auth/login';
export const URL_AUTH_LOGOUT = '/api/auth/logout';
export const KEY_CURRENT_USER = 'currentUser';
export const DEFAULT_POST_AUTH_REDIRECT_ROUTE = 'dashboard';

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

    return this.getCurrentUserFromLocalStorage() !== undefined;
  }

  /**
   * Returns the authentication token of the currently logged in user.
   *
   * @returns the authentication token
   */
  public getAuthToken(): string {

    if (this.isUserLoggedIn()) {
      return this.getCurrentUserFromLocalStorage().token;
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
            localStorage.setItem(KEY_CURRENT_USER, JSON.stringify(response.currentUser));
            this.currentUserBehaviorSubject.next(response.currentUser);
          } else {
            // TODO change into message
            console.log(response.message);
          }

          responseSubject.next(response.status);
          responseSubject.complete();
        },
        error => {
          // TODO change into message
          console.log(error);
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
            localStorage.removeItem(KEY_CURRENT_USER);
            this.currentUserBehaviorSubject.next(undefined);
          } else {
            // TODO change into message
            console.log(response.message);
          }

          responseSubject.next(response.status);
          responseSubject.complete()
        },
        error => {
          // TODO change into message
          console.log(error);
          responseSubject.next(RequestStatus.FAILURE);
          responseSubject.complete();
        }
      );

    return response$;
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

}
