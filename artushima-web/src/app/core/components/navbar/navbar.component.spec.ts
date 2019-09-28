import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { AuthService } from '../../services/auth.service';

import { NavbarComponent } from './navbar.component';

import { RequestStatus } from 'src/app/model/request-status';

describe('NavbarComponent', () => {

  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;
  let router: Router;
  let authService: AuthService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NavbarComponent],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        FontAwesomeModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    router = TestBed.get(Router);
    authService = TestBed.get(AuthService);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('homeOnClick', () => {

    it('should navigate to the dashboard', () => {

      // given
      spyOn(router, 'navigate');

      // when
      component.homeOnClick();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['dashboard']);
    });
  });

  describe('logInOnClick', () => {

    it('should navigate to the login page', () => {

      // given
      spyOn(router, 'navigate');

      // when
      component.logInOnClick();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['login']);
    });
  });

  describe('logOutOnClick', () => {

    it('should navigate to the login page when the user logged out', () => {

      // given
      spyOn(authService, 'logout')
        .and.returnValue(new Observable(observer => {
          observer.next(RequestStatus.SUCCESS);
          observer.complete();
        }));

      spyOn(router, 'navigate');

      // when
      component.logOutOnClick();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['login']);
    });

    it('should do nothing when the logging out was unsuccessful', () => {

      // given
      spyOn(authService, 'logout')
        .and.returnValue(new Observable(observer => {
          observer.next(RequestStatus.FAILURE);
          observer.complete();
        }));

      spyOn(router, 'navigate');

      // when
      component.logOutOnClick();

      // then
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });
});
