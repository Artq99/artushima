import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { CampaignDetailsComponent } from './campaign-details.component';
import { CampaignDetailsCampaignInfoComponent } from './campaign-details-campaign-info/campaign-details-campaign-info.component';
import { GmInfoComponent } from './gm-info/gm-info.component';

describe('CampaignDetailsComponent', () => {
  let component: CampaignDetailsComponent;
  let fixture: ComponentFixture<CampaignDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        FontAwesomeModule
      ],
      declarations: [
        CampaignDetailsComponent,
        // TODO Child components - should they be mocked?
        CampaignDetailsCampaignInfoComponent,
        GmInfoComponent
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
