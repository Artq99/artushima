import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { AuthService } from '../services/auth.service';

/**
 * A guard that ensures, that only an authenitcated user can access a given
 * route. If the user has not been authenticated, it redirects to the login
 * page.
 */
@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  public constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  public canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

    if (this.authService.isUserLoggedIn()) {
      return true;
    } else {
      this.authService.postAuthRedirectRoute = next.url[0].path;
      this.router.navigate(["login"]);
      return false;
    }
  }

}
