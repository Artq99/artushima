import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController, TestRequest } from '@angular/common/http/testing'

import { AuthenticationModule } from 'src/app/authentication/authentication.module';
import { DashboardModule } from 'src/app/dashboard/dashboard.module';

import {
  AuthService,
  URL_AUTH_LOGIN,
  KEY_CURRENT_USER,
  URL_AUTH_LOGOUT,
  MSG_LOGIN,
  MSG_LOGOUT,
  MSG_AUTH_ERROR
} from './auth.service';
import { MessagesService } from './messages.service';

import { AuthLoginResponse } from 'src/app/model/auth-login-response';
import { AuthLogoutResponse } from 'src/app/model/auth-logout-response';
import { CurrentUser } from 'src/app/model/current-user';
import { RequestStatus } from 'src/app/model/request-status';
import { DecodedToken } from 'src/app/model/decoded-token';
import { MessageLevel } from 'src/app/model/message-level';

describe('AuthService', () => {

  // test data
  const TEST_USER: CurrentUser = new CurrentUser();
  TEST_USER.userName = 'testUser';
  TEST_USER.roles = ['role_player'];
  TEST_USER.token = 'test_token';

  const TEST_DECODED_TOKEN_VALID: DecodedToken = new DecodedToken();
  TEST_DECODED_TOKEN_VALID.sub = 'testUser';
  TEST_DECODED_TOKEN_VALID.iat = new Date('2010-01-01');
  TEST_DECODED_TOKEN_VALID.exp = new Date('2090-12-31');

  const TEST_DECODED_TOKEN_EXPIRED: DecodedToken = new DecodedToken();
  TEST_DECODED_TOKEN_EXPIRED.sub = 'testUser';
  TEST_DECODED_TOKEN_EXPIRED.iat = new Date('2010-01-01');
  TEST_DECODED_TOKEN_EXPIRED.exp = new Date('2010-12-31');

  const TEST_AUTH_LOGIN_RESPONSE_SUCCESS: AuthLoginResponse = new AuthLoginResponse();
  TEST_AUTH_LOGIN_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
  TEST_AUTH_LOGIN_RESPONSE_SUCCESS.currentUser = TEST_USER;

  const TEST_AUTH_LOGIN_RESPONSE_FAILURE: AuthLoginResponse = new AuthLoginResponse();
  TEST_AUTH_LOGIN_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_AUTH_LOGIN_RESPONSE_FAILURE.message = 'Error';

  const TEST_AUTH_LOGOUT_RESPONSE_SUCCESS: AuthLogoutResponse = new AuthLogoutResponse();
  TEST_AUTH_LOGOUT_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;

  const TEST_AUTH_LOGOUT_RESPONSE_FAILURE: AuthLogoutResponse = new AuthLogoutResponse();
  TEST_AUTH_LOGOUT_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_AUTH_LOGOUT_RESPONSE_FAILURE.message = 'Error';

  let httpTestingController: HttpTestingController;
  let authService: AuthService;
  let messagesService: MessagesService;

  beforeEach(() => {

    TestBed.configureTestingModule({
      providers: [AuthService],
      imports: [
        HttpClientTestingModule,
        DashboardModule,
        AuthenticationModule
      ]
    });

    httpTestingController = TestBed.get(HttpTestingController);
    authService = TestBed.get(AuthService);
    messagesService = TestBed.get(MessagesService);
  });

  it('should be created', () => {

    // then
    expect(authService).toBeTruthy();
  });

  describe('isUserLoggedIn', () => {

    it('should return true when the user has been authenticated', () => {

      // given
      spyOn<any>(authService, 'getDecodedToken')
        .and.returnValue(TEST_DECODED_TOKEN_VALID);

      // when
      let result: boolean = authService.isUserLoggedIn();

      // then
      expect(result).toBeTruthy();
    });

    it('should return false when the user has not been authenticated', () => {

      // given
      spyOn(localStorage, 'getItem')
        .and.returnValue(null);

      // when
      let result: boolean = authService.isUserLoggedIn();

      // then
      expect(result).toBeFalsy();
    });

    it('should return false when the user has been authenticated, but the token has expired', () => {

      // given
      spyOn<any>(authService, 'getDecodedToken')
        .and.returnValue(TEST_DECODED_TOKEN_EXPIRED);

      // when
      let result: boolean = authService.isUserLoggedIn();

      // then
      expect(result).toBeFalsy();
    });
  });

  describe('validateInitialLogin', () => {

    it('should do nothing if the user has not been authenticated', () => {

      // given
      spyOn<any>(authService, 'getDecodedToken')
        .and.returnValue(undefined);

      let clearCurrentUserSpy: jasmine.Spy = spyOn<any>(authService, 'clearCurrentUser');

      // when
      authService.validateInitialLogin();

      // then
      expect(clearCurrentUserSpy).not.toHaveBeenCalled();
    });

    it('should not remove the current user from the local storage if the token is valid', () => {

      // given
      spyOn<any>(authService, 'getDecodedToken')
        .and.returnValue(TEST_DECODED_TOKEN_VALID);

      let clearCurrentUserSpy: jasmine.Spy = spyOn<any>(authService, 'clearCurrentUser');

      // when
      authService.validateInitialLogin();

      // then
      expect(clearCurrentUserSpy).not.toHaveBeenCalled();
    });

    it('should remove the current user from the local storage it the token has expired', () => {

      // given
      spyOn<any>(authService, 'getDecodedToken')
        .and.returnValue(TEST_DECODED_TOKEN_EXPIRED);

      let clearCurrentUserSpy: jasmine.Spy = spyOn<any>(authService, 'clearCurrentUser');

      // when
      authService.validateInitialLogin();

      // then
      expect(clearCurrentUserSpy).toHaveBeenCalled();
    });
  });

  describe('getAuthToken', () => {

    it('should return a token when the user has been authenticated', () => {

      // given
      spyOn(localStorage, 'getItem').and.returnValue(JSON.stringify(TEST_USER));

      // when
      let result: string = authService.getAuthToken();

      // then
      expect(result).toEqual(TEST_USER.token);
    });

    it('should return undefined when the user has not been authenticated', () => {

      // given
      spyOn(localStorage, 'getItem').and.returnValue(null);

      // when
      let result: string = authService.getAuthToken();

      // then
      expect(result).toEqual(undefined);
    });
  });

  describe('login', () => {

    it('should authenticate a user', () => {

      // given
      spyOn(localStorage, 'setItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.SUCCESS));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.flush(TEST_AUTH_LOGIN_RESPONSE_SUCCESS);

      httpTestingController.verify();
      expect(localStorage.setItem).toHaveBeenCalledWith(KEY_CURRENT_USER, JSON.stringify(TEST_USER));
      expect(messagesService.showMessage).toHaveBeenCalledWith(`${MSG_LOGIN}${TEST_USER.userName}`, MessageLevel.INFO);
    });

    it('should process failed response', () => {

      // given
      spyOn(localStorage, 'setItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.flush(TEST_AUTH_LOGIN_RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(localStorage.setItem).not.toHaveBeenCalled();
      expect(messagesService.showMessage)
        .toHaveBeenCalledWith(TEST_AUTH_LOGIN_RESPONSE_FAILURE.message, MessageLevel.ERROR);
    });

    it('should process http error', () => {

      // given
      spyOn(localStorage, 'setItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(localStorage.setItem).not.toHaveBeenCalled();
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_AUTH_ERROR, MessageLevel.ERROR);
    });
  });

  describe('logout', () => {

    it('should log out a user', () => {

      // given
      spyOn(localStorage, 'getItem')
        .and.returnValue(JSON.stringify(TEST_USER));
      spyOn(localStorage, 'removeItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.logout()
        .subscribe(status => expect(status).toEqual(RequestStatus.SUCCESS));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGOUT);
      request.flush(TEST_AUTH_LOGOUT_RESPONSE_SUCCESS);

      httpTestingController.verify();
      expect(localStorage.removeItem).toHaveBeenCalledWith(KEY_CURRENT_USER);
      expect(messagesService.showMessage)
        .toHaveBeenCalledWith(`${MSG_LOGOUT}${TEST_USER.userName}`, MessageLevel.INFO);
    });

    it('should process failed response', () => {

      // given
      spyOn(localStorage, 'removeItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.logout()
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGOUT);
      request.flush(TEST_AUTH_LOGOUT_RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(localStorage.removeItem).not.toHaveBeenCalled();
      expect(messagesService.showMessage)
        .toHaveBeenCalledWith(TEST_AUTH_LOGOUT_RESPONSE_FAILURE.message, MessageLevel.ERROR);
    });

    it('should process http error', () => {

      // given
      spyOn(localStorage, 'setItem');
      spyOn(messagesService, 'showMessage');

      // when then
      authService.logout()
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGOUT);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(localStorage.setItem).not.toHaveBeenCalled();
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_AUTH_ERROR, MessageLevel.ERROR);
    });
  });
});
