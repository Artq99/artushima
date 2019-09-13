import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private authToken: string;

  constructor() { }

  isUserLoggedIn(): boolean {

    if (this.authToken) {
      return true;
    } else {
      return false;
    }
  }

  setAuthToken(token: string) {
    this.authToken = token;
  }

}
