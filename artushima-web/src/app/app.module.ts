import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { DashboardModule } from './dashboard/dashboard.module';
import { CoreModule } from './core/core.module';
import { UsersModule } from './users/users.module';

import { AuthGuard } from './core/guards/auth.guard';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/components/dashboard/dashboard.component';
import { LoginComponent } from './core/components/login/login.component';
import { UserListComponent } from './users/components/user-list/user-list.component';
import { UserEditorComponent } from './users/components/user-editor/user-editor.component';

/**
 * The definitions of all the routes existing in the application.
 */
export const appRoutes: Routes = [
  {
    path: "dashboard",
    component: DashboardComponent,
    canActivate: [AuthGuard]
  },
  {
    path: "login",
    component: LoginComponent
  },
  {
    path: "users/list",
    component: UserListComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_show_users'] }
  },
  {
    path: 'users/add',
    component: UserEditorComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_create_user'] }
  },
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  }
]

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    CoreModule,
    DashboardModule,
    UsersModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
