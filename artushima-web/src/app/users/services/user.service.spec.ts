import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, TestRequest, HttpTestingController } from '@angular/common/http/testing';

import { UserService, URL_USERS_LIST, URL_USERS_ADD, MSG_APP_ERROR } from './user.service';
import { MessagesService } from 'src/app/core/services/messages.service';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { UsersListResponse } from '../model/users-list-response';
import { User } from '../model/user';
import { UsersAddRequest } from '../model/users-add-request';
import { UsersAddResponse } from '../model/users-add-response';

describe('UserService', () => {

  // test data
  const TEST_USER_1 = new User();
  TEST_USER_1.id = 1;
  TEST_USER_1.userName = 'test_user_1';

  const TEST_USER_2 = new User();
  TEST_USER_2.id = 2;
  TEST_USER_2.userName = 'test_user_2';

  const TEST_USER_LIST = [
    TEST_USER_1,
    TEST_USER_2
  ];

  const TEST_ERR_MSG = 'test error message';

  const TEST_USERS_LIST_RESPONSE_SUCCESS = new UsersListResponse();
  TEST_USERS_LIST_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
  TEST_USERS_LIST_RESPONSE_SUCCESS.message = '';
  TEST_USERS_LIST_RESPONSE_SUCCESS.users = TEST_USER_LIST;

  const TEST_USERS_LIST_RESPONSE_FAILURE = new UsersListResponse();
  TEST_USERS_LIST_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_USERS_LIST_RESPONSE_FAILURE.message = TEST_ERR_MSG;

  const TEST_USERS_ADD_REQUEST = new UsersAddRequest();
  TEST_USERS_ADD_REQUEST.userName = "test_user_1";
  TEST_USERS_ADD_REQUEST.password = "test_password";
  TEST_USERS_ADD_REQUEST.roles = [
    'test_role_1',
    'test_role_2'
  ]

  const TEST_USERS_ADD_RESPONSE_SUCCESS = new UsersAddResponse();
  TEST_USERS_ADD_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
  TEST_USERS_ADD_RESPONSE_SUCCESS.message = '';

  const TEST_USERS_ADD_RESPONSE_FAILURE = new UsersAddResponse();
  TEST_USERS_ADD_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_USERS_ADD_RESPONSE_FAILURE.message = TEST_ERR_MSG;

  let httpTestingController: HttpTestingController;
  let userService: UserService;
  let messagesService: MessagesService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ]
    });

    httpTestingController = TestBed.get(HttpTestingController);
    userService = TestBed.get(UserService);
    messagesService = TestBed.get(MessagesService);
  });

  it('should be created', () => {
    // then
    expect(userService).toBeTruthy();
  });

  describe('getUserList', () => {

    it('should return a list of all users', () => {
      // given
      spyOn(messagesService, 'showMessage');

      // when then
      userService.getUserList()
        .subscribe(response => expect(response).toEqual(TEST_USER_LIST));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_LIST);
      request.flush(TEST_USERS_LIST_RESPONSE_SUCCESS);

      httpTestingController.verify();
      expect(messagesService.showMessage).toHaveBeenCalledTimes(0);
    });

    it('should return empty list, when the request status is a failure', () => {
      // given
      spyOn(messagesService, 'showMessage');

      // when then
      userService.getUserList()
        .subscribe(response => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_LIST);
      request.flush(TEST_USERS_LIST_RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(messagesService.showMessage).toHaveBeenCalledWith(TEST_ERR_MSG, MessageLevel.ERROR);
    });

    it('should process HTTP error', () => {
      // given
      spyOn(messagesService, 'showMessage');

      // when then
      userService.getUserList()
        .subscribe(response => expect(response).toEqual([]));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_LIST);
      request.error(new ErrorEvent('error'), { status: 404 });

      httpTestingController.verify();
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_APP_ERROR, MessageLevel.ERROR);
    });
  });

  describe('createNewUser', () => {

    it('should create a new user', () => {
      // given
      spyOn(messagesService, 'showMessage');

      let userName: string = TEST_USERS_ADD_REQUEST.userName;
      let password: string = TEST_USERS_ADD_REQUEST.password;
      let roles: string[] = TEST_USERS_ADD_REQUEST.roles;

      // when then
      userService.createNewUser(userName, password, roles)
        .subscribe(response => expect(response).toEqual(RequestStatus.SUCCESS));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_ADD);
      request.flush(TEST_USERS_ADD_RESPONSE_SUCCESS);

      httpTestingController.verify()
      expect(messagesService.showMessage).toHaveBeenCalledTimes(0);
    });

    it('should process a failed response', () => {
      // given
      spyOn(messagesService, 'showMessage');

      let userName: string = TEST_USERS_ADD_REQUEST.userName;
      let password: string = TEST_USERS_ADD_REQUEST.password;
      let roles: string[] = TEST_USERS_ADD_REQUEST.roles;

      // when then
      userService.createNewUser(userName, password, roles)
        .subscribe(response => expect(response).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_ADD);
      request.flush(TEST_USERS_ADD_RESPONSE_FAILURE);

      httpTestingController.verify();
      expect(messagesService.showMessage).toHaveBeenCalledWith(TEST_ERR_MSG, MessageLevel.ERROR);
    });

    it('should process a HTTP error', () => {
      // given
      spyOn(messagesService, 'showMessage');

      let userName: string = TEST_USERS_ADD_REQUEST.userName;
      let password: string = TEST_USERS_ADD_REQUEST.password;
      let roles: string[] = TEST_USERS_ADD_REQUEST.roles;

      // when then
      userService.createNewUser(userName, password, roles)
        .subscribe(response => expect(response).toEqual(RequestStatus.FAILURE));

      let request: TestRequest = httpTestingController.expectOne(URL_USERS_ADD);
      request.error(new ErrorEvent(TEST_ERR_MSG), { status: 404 });

      httpTestingController.verify();
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_APP_ERROR, MessageLevel.ERROR);
    });
  });
});
