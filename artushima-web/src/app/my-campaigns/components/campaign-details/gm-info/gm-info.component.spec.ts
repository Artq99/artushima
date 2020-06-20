import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GmInfoComponent } from './gm-info.component';

describe('GmInfoComponent', () => {
  let component: GmInfoComponent;
  let fixture: ComponentFixture<GmInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
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
});
