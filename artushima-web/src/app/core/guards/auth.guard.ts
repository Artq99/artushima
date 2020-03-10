import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { MessageLevel } from 'src/app/core/model/message-level';

import { AuthService } from '../services/auth.service';
import { MessagesService } from '../services/messages.service';

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
    private authService: AuthService,
    private messagesService: MessagesService
  ) { }

  public canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

    if (!this.authService.isUserLoggedIn()) {
      this.authService.postAuthRedirectRoute = this.createRedirectRoute(next);
      this.router.navigate(["login"]);
      return false;

    } else if (next.data !== undefined && !this.authService.hasUserGotRoles(next.data.roles)) {
      this.messagesService.showMessage("Nie masz odpowiednich uprawnień.", MessageLevel.ERROR);
      this.router.navigate(["dashboard"]);
      return false;

    } else {
      return true;
    }
  }

  private createRedirectRoute(next: ActivatedRouteSnapshot): string {

    let redirectRoute: string = next.url[0].path;
    next.url.forEach(segment => {
      if (segment !== next.url[0]) {
        redirectRoute += '/' + segment.path
      }
    });

    return redirectRoute;
  }

}
