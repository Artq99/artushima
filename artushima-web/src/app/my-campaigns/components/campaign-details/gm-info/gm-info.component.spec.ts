import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { GmInfoComponent } from './gm-info.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

describe('GmInfoComponent', () => {
  let component: GmInfoComponent;
  let fixture: ComponentFixture<GmInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FontAwesomeModule],
      declarations: [GmInfoComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GmInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should show the game master\'s name', () => {
    // given
    const gmName: string = "Test Mistrz Gry";
    let gmNameElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#gm-info_gm-name'))
      .nativeElement;

    // when
    component.gmName = gmName;
    fixture.detectChanges();

    // then
    expect(gmNameElement.textContent).toEqual(gmName);
  });
});
