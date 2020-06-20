import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignDetailsComponent } from './campaign-details.component';
import { RouterTestingModule } from '@angular/router/testing';
import { CampaignDetailsCampaignInfoComponent } from './campaign-details-campaign-info/campaign-details-campaign-info.component';

describe('CampaignDetailsComponent', () => {
  let component: CampaignDetailsComponent;
  let fixture: ComponentFixture<CampaignDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      declarations: [
        CampaignDetailsComponent,
        // TODO Child components - should they be mocked?
        CampaignDetailsCampaignInfoComponent
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });
});
