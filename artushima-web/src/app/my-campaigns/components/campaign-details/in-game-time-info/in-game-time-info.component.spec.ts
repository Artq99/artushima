import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';
import { InGameTimeInfoComponent } from './in-game-time-info.component';

describe('InGameTimeInfoComponent', () => {
  let component: InGameTimeInfoComponent;
  let fixture: ComponentFixture<InGameTimeInfoComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        imports: [
          FontAwesomeModule,
          SharedModule
        ],
        declarations: [InGameTimeInfoComponent]
      })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InGameTimeInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should show the start date', () => {
    // given
    const startDate: Date = new Date(2053, 10, 18);
    const startDateElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__in-game-time-info__startDate'))
      .nativeElement;

    // when
    component.startDate = startDate;
    fixture.detectChanges();

    // then
    expect(startDateElement.textContent).toEqual('18.11.2053');
  });

  it('should show the number of days that passed', () => {
    // given
    const passedDays: number = 10;
    const passedDaysElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__in-game-time-info__passedDays'))
      .nativeElement;

    // when
    component.passedDays = passedDays;
    fixture.detectChanges();

    // then
    expect(passedDaysElement.textContent).toEqual('10');
  });

  it('should show the current date', () => {
    // given
    const currentDate: Date = new Date(2020, 10, 28);
    const currentDateElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__in-game-time-info__currentDate'))
      .nativeElement;

    // when
    component.currentDate = currentDate;
    fixture.detectChanges();

    // then
    expect(currentDateElement.textContent).toEqual('28.11.2020');
  });
});
