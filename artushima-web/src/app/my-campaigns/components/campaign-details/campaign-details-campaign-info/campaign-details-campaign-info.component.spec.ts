import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignDetailsCampaignInfoComponent } from './campaign-details-campaign-info.component';

describe('CampaignDetailsCampaignInfoComponent', () => {
  let component: CampaignDetailsCampaignInfoComponent;
  let fixture: ComponentFixture<CampaignDetailsCampaignInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CampaignDetailsCampaignInfoComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignDetailsCampaignInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
