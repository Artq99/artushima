import { Injectable } from '@angular/core';
import { CurrentUser } from 'src/app/model/current-user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  /**
   * The variable holding a route to redirect after login.
   */
  redirectRoute: string;

  constructor() { }

  /**
   * Indicates the state of user authentication.
   *
   * @returns true if user has been authenticated, false otherwise.
   */
  public isUserLoggedIn(): boolean {

    if (localStorage.getItem("currentUser")) {
      return true;
    } else {
      return false;
    }
  }

  /**
   * Sets the current user in the local storage to preserve login.
   *
   * @param currentUser
   */
  setCurrentUser(currentUser: CurrentUser) {

    if (currentUser) {
      localStorage.setItem("currentUser", JSON.stringify(currentUser));
    }
  }

}
