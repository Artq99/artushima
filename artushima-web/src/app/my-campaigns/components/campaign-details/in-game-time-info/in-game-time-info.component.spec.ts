import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InGameTimeInfoComponent } from './in-game-time-info.component';

describe('InGameTimeInfoComponent', () => {
  let component: InGameTimeInfoComponent;
  let fixture: ComponentFixture<InGameTimeInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
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
});
