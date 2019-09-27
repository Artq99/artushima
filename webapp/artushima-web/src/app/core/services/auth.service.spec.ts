import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController, TestRequest } from '@angular/common/http/testing'

import { AuthenticationModule } from 'src/app/authentication/authentication.module';
import { DashboardModule } from 'src/app/dashboard/dashboard.module';

import { AuthService, URL_AUTH_LOGIN, KEY_CURRENT_USER } from './auth.service';

import { AuthLoginResponse } from 'src/app/model/auth-login-response';
import { CurrentUser } from 'src/app/model/current-user';
import { RequestStatus } from 'src/app/model/request-status';

describe('AuthService', () => {

  // test data
  const TEST_USER: CurrentUser = new CurrentUser();
  TEST_USER.userName = 'testUser';
  TEST_USER.role = 'role_player';
  TEST_USER.token = 'test_token';

  const TEST_RESPONSE_SUCCESS: AuthLoginResponse = new AuthLoginResponse();
  TEST_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
  TEST_RESPONSE_SUCCESS.currentUser = TEST_USER;

  const TEST_RESPONSE_FAILURE: AuthLoginResponse = new AuthLoginResponse();
  TEST_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_RESPONSE_FAILURE.message = 'Error';

  let httpTestingController: HttpTestingController;
  let authService: AuthService;

  beforeEach(() => {

    TestBed.configureTestingModule({
      providers: [AuthService],
      imports: [
        HttpClientTestingModule,
        DashboardModule,
        AuthenticationModule
      ]
    })

    httpTestingController = TestBed.get(HttpTestingController);
    authService = TestBed.get(AuthService);
  });

  it('should be created', () => {

    // then
    expect(authService).toBeTruthy();
  });

  describe('isUserLoggedIn', () => {

    it('should return true when the user has been authenticated', () => {

      // given
      spyOn(localStorage, 'getItem').and.returnValue(JSON.stringify(TEST_USER));

      // when
      let result: boolean = authService.isUserLoggedIn();

      // then
      expect(result).toBeTruthy();
    });

    it('should return false when the user has not been authenticated', () => {

      // given
      spyOn(localStorage, 'getItem').and.returnValue(null);

      // when
      let result: boolean = authService.isUserLoggedIn();

      // then
      expect(result).toBeFalsy();
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

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.SUCCESS));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.flush(TEST_RESPONSE_SUCCESS);

      httpTestingController.verify();
      expect(localStorage.setItem).toHaveBeenCalledWith(KEY_CURRENT_USER, JSON.stringify(TEST_USER));
    });

    it('should process failed response', () => {

      // given
      spyOn(localStorage, 'setItem');

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.flush(TEST_RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(localStorage.setItem).not.toHaveBeenCalled();
    });

    it('should process http error', () => {

      // given
      spyOn(localStorage, 'setItem');

      // when then
      authService.login('testUser', 'password')
        .subscribe(status => expect(status).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_AUTH_LOGIN);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(localStorage.setItem).not.toHaveBeenCalled();
    });
  });
});
