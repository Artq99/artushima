import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { NavbarComponent } from './navbar.component';

describe('NavbarComponent', () => {

  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;
  let router: Router;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NavbarComponent],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        FontAwesomeModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    router = TestBed.get(Router);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('homeOnClick', () => {

    it('should navigate to the dashboard', () => {

      // given
      spyOn(router, 'navigate');

      // when
      component.homeOnClick();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['dashboard']);
    });
  });

  describe('logInOnClick', () => {

    it('should navigate to the login page', () => {

      // given
      spyOn(router, 'navigate');

      // when
      component.logInOnClick();

      // then
      expect(router.navigate).toHaveBeenCalledWith(['login']);
    });
  });
});
