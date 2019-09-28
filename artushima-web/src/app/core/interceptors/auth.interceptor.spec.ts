import { TestBed } from "@angular/core/testing";
import { AuthInterceptor } from './auth.interceptor';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AuthService } from '../services/auth.service';
import { HttpHandler, HttpRequest } from '@angular/common/http';

describe('AuthInterceptor', () => {

  let authService: AuthService;
  let authInterceptor: AuthInterceptor;
  let httpHandler: HttpHandler;

  beforeEach(() => {

    TestBed.configureTestingModule({
      providers: [AuthInterceptor],
      imports: [
        HttpClientTestingModule
      ]
    });

    authService = TestBed.get(AuthService);
    authInterceptor = TestBed.get(AuthInterceptor);
    httpHandler = TestBed.get(HttpHandler);
  });

  it('should be created', () => {

    // then
    expect(authInterceptor).toBeTruthy();
  });

  describe('intercept', () => {

    it('should add the authorization header', () => {

      // given
      spyOn(authService, 'getAuthToken')
        .and.returnValue('test_token');

      spyOn(httpHandler, 'handle');

      let request: HttpRequest<any> = new HttpRequest<any>('GET', 'test_url');
      let request_clone: HttpRequest<any> = new HttpRequest<any>('GET', 'test_url');

      spyOn(request, 'clone')
        .and.returnValue(request_clone);

      // when
      authInterceptor.intercept(request, httpHandler);

      // then
      expect(request.clone).toHaveBeenCalledWith({
        setHeaders: {
          Authorization: 'Bearer test_token'
        }
      });
      expect(httpHandler.handle).toHaveBeenCalledWith(request_clone);
    });

    it('should not add the authorization header when the user has not been authenticated', () => {

      // given
      spyOn(authService, 'getAuthToken')
        .and.returnValue(undefined);

      spyOn(httpHandler, 'handle');

      let request: HttpRequest<any> = new HttpRequest<any>('GET', 'test_url');

      spyOn(request, 'clone');

      // when
      authInterceptor.intercept(request, httpHandler);

      // then
      expect(request.clone).not.toHaveBeenCalled();
      expect(httpHandler.handle).toHaveBeenCalledWith(request);
    });
  });
});
