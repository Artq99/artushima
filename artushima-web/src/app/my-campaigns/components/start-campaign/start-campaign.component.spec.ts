import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StartCampaignComponent } from './start-campaign.component';

describe('StartCampaignComponent', () => {

  let startCampaignComponent: StartCampaignComponent;
  let fixture: ComponentFixture<StartCampaignComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [StartCampaignComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StartCampaignComponent);
    startCampaignComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(startCampaignComponent).toBeTruthy();
  });
});
