import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { AuthService } from 'src/app/core/services/auth.service';

import { LoginComponent } from './login.component';
import { Observable } from 'rxjs';
import { RequestStatus } from 'src/app/core/model/request-status';

describe('LoginComponent', () => {

  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let router: Router;
  let authService: AuthService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [LoginComponent],
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        FormsModule,
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    router = TestBed.get(Router);
    authService = TestBed.get(AuthService);
  });

  it('should be created', () => {

    // then
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {

    it('should navigate to the dashboard if the user has alredy been authenticated', () => {

      // given
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(true);

      spyOn(router, 'navigate');

      // when
      component.ngOnInit();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['dashboard']);
    });

    it('should do nothing if the user has not been authenticated', () => {

      // given
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(false);

      spyOn(router, 'navigate');

      // when
      component.ngOnInit();

      // then
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });

  describe('loginOnClick', () => {

    it('should navigate to the previous location after the user has been authenticated', () => {

      // given
      component.userName = 'testUser';
      component.password = 'password';

      spyOn(authService, 'login')
        .and.returnValue(new Observable(observer => {
          observer.next(RequestStatus.SUCCESS);
          observer.complete();
        }));

      spyOnProperty(authService, 'postAuthRedirectRoute', 'get')
        .and.returnValue('previous_url');

      spyOn(router, 'navigate');

      // when
      component.loginOnClick();

      // then
      expect(authService.login).toHaveBeenCalledWith('testUser', 'password');
      expect(router.navigate).toHaveBeenCalledWith(['previous_url']);
    });

    it('should clear password form after the user authentication has not been successful', () => {

      // given
      component.userName = 'testUser';
      component.password = 'password';

      spyOn(authService, 'login')
        .and.returnValue(new Observable(observer => {
          observer.next(RequestStatus.FAILURE);
          observer.complete();
        }));

      spyOn(router, 'navigate');

      // when
      component.loginOnClick();

      // then
      expect(authService.login).toHaveBeenCalledWith('testUser', 'password');
      expect(component.password).toEqual('');
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });
});
