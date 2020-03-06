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
      let activatedRouteSnapshot: ActivatedRouteSnapshot = new ActivatedRouteSnapshot();
      activatedRouteSnapshot.url = [new UrlSegment('test_route', {})];
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(true);

      // when
      let result = authGuard.canActivate(activatedRouteSnapshot, undefined);

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

    it('should return true when the user has authenticated and has got required roles', () => {

      // given
      let activatedRouteSnapshot: ActivatedRouteSnapshot = new ActivatedRouteSnapshot();
      activatedRouteSnapshot.url = [new UrlSegment('test_route', {})];
      activatedRouteSnapshot.data = { roles: ["test_role"] };
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(true);
      spyOn(authService, 'hasUserGotRoles')
        .and.returnValue(true);

      // when
      let result = authGuard.canActivate(activatedRouteSnapshot, undefined);

      // then
      expect(result).toBeTruthy();
      expect(authService.hasUserGotRoles).toHaveBeenCalledWith(['test_role']);
    });

    it('should return false when the user has not got required roles', () => {

      // given
      let activatedRouteSnapshot: ActivatedRouteSnapshot = new ActivatedRouteSnapshot();
      activatedRouteSnapshot.url = [new UrlSegment('test_route', {})];
      activatedRouteSnapshot.data = { roles: ["test_role"] };
      spyOn(authService, 'isUserLoggedIn')
        .and.returnValue(true);
      spyOn(authService, 'hasUserGotRoles')
        .and.returnValue(false);

      // when
      let result = authGuard.canActivate(activatedRouteSnapshot, undefined);

      // then
      expect(result).toBeFalsy();
      expect(authService.hasUserGotRoles).toHaveBeenCalledWith(['test_role']);
    });
  });
});
