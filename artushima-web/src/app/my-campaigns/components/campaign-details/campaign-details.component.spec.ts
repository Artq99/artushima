import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';
import { CampaignDetailsComponent } from './campaign-details.component';
import { CampaignInfoComponent } from './campaign-info/campaign-info.component';
import { CampaignPlayersInfoComponent } from './campaign-players-info/campaign-players-info.component';
import { CampaignTimelineComponent } from './campaign-timeline/campaign-timeline.component';
import { InGameTimeInfoComponent } from './in-game-time-info/in-game-time-info.component';

describe('CampaignDetailsComponent', () => {
  let component: CampaignDetailsComponent;
  let fixture: ComponentFixture<CampaignDetailsComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        imports: [
          RouterTestingModule,
          FontAwesomeModule,
          SharedModule
        ],
        declarations: [
          CampaignDetailsComponent,
          CampaignInfoComponent,
          CampaignPlayersInfoComponent,
          CampaignTimelineComponent,
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
