import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRouteSnapshot, UrlSegment } from '@angular/router';

import { AuthService } from '../services/auth.service';

import { AuthGuard } from './auth.guard';

describe('AuthGuard', () => {

  let authGuard: AuthGuard;
  let authService: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        AuthService,
        AuthGuard
      ],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
      ]
    });

    authGuard = TestBed.get(AuthGuard);
    authService = TestBed.get(AuthService);
  });

  it('should be created', () => {

    // then
    expect(authGuard).toBeTruthy();
  });

  describe('canActivate', () => {

    it('should return true when the user has authenticated', () => {

      // given
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(true);

      // when
      let result = authGuard.canActivate(undefined, undefined);

      // then
      expect(result).toBeTruthy();
    });

    it('should return false when the user has not authenticated', () => {

      // given
      let activatedRouteSnapshot: ActivatedRouteSnapshot = new ActivatedRouteSnapshot();
      activatedRouteSnapshot.url = [new UrlSegment('test_route', {})];
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(false);

      // when
      let result = authGuard.canActivate(activatedRouteSnapshot, undefined);

      // then
      expect(result).toBeFalsy();
    });
  });
});
