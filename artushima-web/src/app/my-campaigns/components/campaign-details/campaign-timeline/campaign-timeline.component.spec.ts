import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignTimelineComponent } from './campaign-timeline.component';

describe('CampaignTimelineComponent', () => {
  let component: CampaignTimelineComponent;
  let fixture: ComponentFixture<CampaignTimelineComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CampaignTimelineComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignTimelineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });
});
