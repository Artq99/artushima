import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { DashboardComponent } from './dashboard.component';
import { By } from '@angular/platform-browser';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardComponent],
      imports: [
        HttpClientTestingModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should render the user-list card', () => {
    // given
    component.hasRoleShowUsers = true;

    // when
    fixture.detectChanges();

    // then
    expect(fixture.debugElement.query(By.css('#user-list-card'))).toBeTruthy();
  });

  it('should not render the user-list card', () => {
    // given
    component.hasRoleShowUsers = false;

    // when
    fixture.detectChanges();

    // then
    expect(fixture.debugElement.query(By.css('#user-list-card'))).toBeFalsy();
  });
});
