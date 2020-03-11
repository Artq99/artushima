import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { BehaviorSubject, Observable } from 'rxjs';

import { UserService } from '../../services/user.service';
import { MessagesService } from 'src/app/core/services/messages.service';

import { UserCreatorComponent, MSG_USER_ADDED } from './user-creator.component';
import { RequestStatus } from 'src/app/core/model/request-status';
import { MessageLevel } from 'src/app/core/model/message-level';

describe('UserCreatorComponent', () => {

  // test data
  const USER_NAME = 'test_user';
  const PASSWORD = 'password';
  const ROLES_SELECTION = [true, false];

  let component: UserCreatorComponent;
  let fixture: ComponentFixture<UserCreatorComponent>;
  let router: Router;
  let userService: UserService;
  let messagesService: MessagesService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [UserCreatorComponent],
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        FormsModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    router = TestBed.get(Router);
    userService = TestBed.get(UserService);
    messagesService = TestBed.get(MessagesService);
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  describe('createOnClick', () => {

    it('should navigate to the user list after a successful user creation', () => {
      // given
      let responseSubject: BehaviorSubject<RequestStatus> = new BehaviorSubject<RequestStatus>(RequestStatus.SUCCESS);
      let response$: Observable<RequestStatus> = responseSubject.asObservable();

      spyOn(userService, 'createNewUser')
        .and.returnValue(response$);
      spyOn(messagesService, 'showMessage');
      spyOn(router, 'navigate');

      component.userName = USER_NAME;
      component.password = PASSWORD;
      component.rolesSelection = ROLES_SELECTION;

      // when
      component.createOnClick();

      // then
      expect(userService.createNewUser).toHaveBeenCalledWith(USER_NAME, PASSWORD, ['role_show_users']);
      expect(messagesService.showMessage).toHaveBeenCalledWith(MSG_USER_ADDED, MessageLevel.INFO);
      expect(router.navigate).toHaveBeenCalledWith(['users', 'list']);
    });

    it('should not proceed if the creation of a new user was unsuccessful', () => {
      // given
      let responseSubject: BehaviorSubject<RequestStatus> = new BehaviorSubject<RequestStatus>(RequestStatus.FAILURE);
      let response$ = responseSubject.asObservable();

      spyOn(userService, 'createNewUser')
        .and.returnValue(response$);
      spyOn(messagesService, 'showMessage');
      spyOn(router, 'navigate');

      component.userName = USER_NAME;
      component.password = PASSWORD;
      component.rolesSelection = ROLES_SELECTION;

      // when
      component.createOnClick();

      // then
      expect(userService.createNewUser).toHaveBeenCalledWith(USER_NAME, PASSWORD, ['role_show_users']);
      expect(messagesService.showMessage).not.toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });
});
