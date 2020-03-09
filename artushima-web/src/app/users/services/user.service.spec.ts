import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, TestRequest, HttpTestingController } from '@angular/common/http/testing';

import { UserService, URL_USERS_LIST, MSG_APP_ERROR } from './user.service';
import { MessagesService } from 'src/app/core/services/messages.service';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';
import { UsersListResponse } from '../model/users-list-response';
import { User } from '../model/user';

describe('UserServiceService', () => {

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

  const TEST_RESPONSE_SUCCESS = new UsersListResponse();
  TEST_RESPONSE_SUCCESS.status = RequestStatus.SUCCESS;
  TEST_RESPONSE_SUCCESS.message = '';
  TEST_RESPONSE_SUCCESS.users = TEST_USER_LIST;

  const TEST_ERR_MSG = 'test error message';

  const TEST_RESPONSE_FAILURE = new UsersListResponse();
  TEST_RESPONSE_FAILURE.status = RequestStatus.FAILURE;
  TEST_RESPONSE_FAILURE.message = TEST_ERR_MSG;

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
      request.flush(TEST_RESPONSE_SUCCESS);

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
      request.flush(TEST_RESPONSE_FAILURE);

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
});
