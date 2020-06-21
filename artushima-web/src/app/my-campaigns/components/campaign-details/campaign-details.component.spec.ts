import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { CampaignDetailsComponent } from './campaign-details.component';
import { CampaignInfoComponent } from './campaign-info/campaign-info.component';
import { GmInfoComponent } from './gm-info/gm-info.component';
import { InGameTimeInfoComponent } from './in-game-time-info/in-game-time-info.component';

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
        CampaignInfoComponent,
        GmInfoComponent,
        InGameTimeInfoComponent
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
