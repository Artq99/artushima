import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { CoreModule } from './core/core.module';
import { AuthenticationModule } from './authentication/authentication.module';
import { DashboardModule } from './dashboard/dashboard.module';

import { AuthService } from './core/services/auth.service';

import { AppComponent } from './app.component';

describe('AppComponent', () => {

  let fixture: ComponentFixture<AppComponent>;
  let component: AppComponent;
  let authService: AuthService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      imports: [
        RouterTestingModule,
        AuthenticationModule,
        CoreModule,
        DashboardModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges()
    authService = TestBed.get(AuthService);
  })

  it('should be created', () => {

    // then
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {

    it('should validate initial login', () => {

      // given
      spyOn(authService, 'validateInitialLogin');

      // when
      component.ngOnInit();

      // then
      expect(authService.validateInitialLogin).toHaveBeenCalled();
    });
  });
});
