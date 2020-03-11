import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UserListComponent } from './user-list.component';
import { UserService } from '../../services/user.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { User } from '../../model/user';
import { BehaviorSubject, Subject, Observable } from 'rxjs';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

describe('UserListComponent', () => {

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

  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;
  let userService: UserService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [UserListComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    userService = TestBed.get(UserService);
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should display a list of users', () => {
    // given
    let userSubject: BehaviorSubject<User[]> = new BehaviorSubject<User[]>(TEST_USER_LIST);
    let user$: Observable<User[]> = userSubject.asObservable();

    spyOn(userService, 'getUserList')
      .and.returnValue(user$);

    // when
    component.ngOnInit();
    fixture.detectChanges();

    // then
    let usersDE: DebugElement = fixture.debugElement.query(By.css('tbody'));
    expect(usersDE.children.length).toEqual(2);
    expect(usersDE.children[0].children[0].nativeElement.textContent).toContain(TEST_USER_1.id);
    expect(usersDE.children[0].children[1].nativeElement.textContent).toContain(TEST_USER_1.userName)
    expect(usersDE.children[1].children[0].nativeElement.textContent).toContain(TEST_USER_2.id);
    expect(usersDE.children[1].children[1].nativeElement.textContent).toContain(TEST_USER_2.userName)
  });

  it('should render the button redirecting to the user-creator', () => {
    // given
    component.hasRoleCreateUser = true;

    // when
    fixture.detectChanges();

    // then
    expect(fixture.debugElement.query(By.css('#btn-redirect-users-add'))).toBeTruthy();
  });

  it('should not render the button redirecting to the user-creator, when the user lacks appropriate roles', () => {
    // given
    component.hasRoleCreateUser = false;

    // when
    fixture.detectChanges();

    // then
    expect(fixture.debugElement.query(By.css('#btn-redirect-users-add'))).toBeFalsy();
  });
});
