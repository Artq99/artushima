import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignTimelineComponent } from './campaign-timeline.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';

describe('CampaignTimelineComponent', () => {
  let component: CampaignTimelineComponent;
  let fixture: ComponentFixture<CampaignTimelineComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FontAwesomeModule,
        SharedModule
      ],
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
