import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';
import { CampaignPlayersInfoComponent } from './campaign-players-info.component';

describe('CampaignPlayersInfoComponent', () => {
  let component: CampaignPlayersInfoComponent;
  let fixture: ComponentFixture<CampaignPlayersInfoComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        imports: [
          FontAwesomeModule,
          SharedModule
        ],
        declarations: [CampaignPlayersInfoComponent]
      })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignPlayersInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });
});
