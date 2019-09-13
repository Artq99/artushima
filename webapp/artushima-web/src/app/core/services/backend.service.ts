import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthTokenRequest } from 'src/app/model/auth-token.request';
import { AuthTokenResponse } from 'src/app/model/auth-token.response';

const authLoginUrl: string = "/api/auth/login";

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private httpClient: HttpClient) { }

  getAuthToken(authTokenRequest: AuthTokenRequest): Observable<AuthTokenResponse> {

    return this.httpClient.post<AuthTokenResponse>(authLoginUrl, authTokenRequest);
  }
}
