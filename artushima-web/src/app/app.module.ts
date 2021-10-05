import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { DashboardModule } from './dashboard/dashboard.module';
import { CoreModule } from './core/core.module';
import { UsersModule } from './users/users.module';
import { MyCampaignsModule } from './my-campaigns/my-campaigns.module';

import { AuthGuard } from './core/guards/auth.guard';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/components/dashboard/dashboard.component';
import { LoginComponent } from './core/components/login/login.component';
import { UserListComponent } from './users/components/user-list/user-list.component';
import { UserCreatorComponent } from './users/components/user-creator/user-creator.component';
import { MyCampaignsListComponent } from './my-campaigns/components/my-campaigns-list/my-campaigns-list.component';
import { StartCampaignComponent } from './my-campaigns/components/start-campaign/start-campaign.component';
import { CampaignDetailsComponent } from './my-campaigns/components/campaign-details/campaign-details.component';
import { TimelineEntryEditorComponent } from './my-campaigns/components/timeline-entry-editor/timeline-entry-editor.component';

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
    component: UserCreatorComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_create_user'] }
  },
  {
    path: 'my_campaigns/list',
    component: MyCampaignsListComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_show_owned_campaigns'] }
  },
  {
    path: 'my_campaigns/start',
    component: StartCampaignComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_start_campaign'] }
  },
  {
    path: 'my_campaigns/campaign_details/:id',
    component: CampaignDetailsComponent,
    canActivate: [AuthGuard],
    // TODO add appropriate role
    data: { roles: ['role_show_owned_campaigns'] }
  },
  {
    path: 'my_campaigns/:id/timeline/entry',
    component: TimelineEntryEditorComponent,
    canActivate: [AuthGuard],
    data: { roles: ['role_create_session_summary'] }
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
    UsersModule,
    MyCampaignsModule
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
