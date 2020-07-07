import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';

// Components
import { CampaignDetailsComponent } from './campaign-details.component';
import { CampaignInfoComponent } from './campaign-info/campaign-info.component';
import { GmInfoComponent } from './gm-info/gm-info.component';
import { InGameTimeInfoComponent } from './in-game-time-info/in-game-time-info.component';
import { CampaignTimelineComponent } from './campaign-timeline/campaign-timeline.component';

describe('CampaignDetailsComponent', () => {
  let component: CampaignDetailsComponent;
  let fixture: ComponentFixture<CampaignDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        FontAwesomeModule,
        SharedModule
      ],
      declarations: [
        CampaignDetailsComponent,
        CampaignInfoComponent,
        GmInfoComponent,
        InGameTimeInfoComponent,
        CampaignTimelineComponent
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
