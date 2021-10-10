import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { of } from 'rxjs';
import { AuthService } from 'src/app/core/services/auth.service';
import { SharedModule } from 'src/app/shared/shared.module';
import { CampaignDetails } from '../../model/campaign-details.model';
import { MyCampaignsAdapterService } from '../../services/my-campaigns-adapter.service/my-campaigns-adapter.service';
import { CampaignDetailsComponent } from './campaign-details.component';
import { CampaignGmToolbarComponent } from './campaign-gm-toolbar/campaign-gm-toolbar.component';
import { CampaignInfoComponent } from './campaign-info/campaign-info.component';
import { CampaignPlayersInfoComponent } from './campaign-players-info/campaign-players-info.component';
import { CampaignTimelineComponent } from './campaign-timeline/campaign-timeline.component';
import { InGameTimeInfoComponent } from './in-game-time-info/in-game-time-info.component';

describe('CampaignDetailsComponent', () => {
  let component: CampaignDetailsComponent;
  let fixture: ComponentFixture<CampaignDetailsComponent>;
  let activatedRoute: ActivatedRoute;

  const myCampaignsAdapterServiceMock: any = jasmine.createSpyObj('MyCampaignsAdapterServiceMock', [
    'getCampaignDetails',
  ]);

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, FontAwesomeModule, SharedModule],
      declarations: [
        CampaignDetailsComponent,
        CampaignInfoComponent,
        CampaignGmToolbarComponent,
        CampaignPlayersInfoComponent,
        CampaignTimelineComponent,
        InGameTimeInfoComponent,
      ],
      providers: [
        { provide: AuthService, useClass: jasmine.createSpy('AuthService') },
        { provide: MyCampaignsAdapterService, useValue: myCampaignsAdapterServiceMock },
      ],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    activatedRoute = TestBed.inject(ActivatedRoute);
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should request the data by the correct ID', () => {
      // given
      const campaignDetails: CampaignDetails = {
        id: 99,
        title: 'Test Campaign',
        creationDate: new Date(2020, 1, 1),
        startDate: new Date(2055, 1, 1),
        passedDays: 10,
        currentDate: new Date(2055, 1, 11),
        gameMasterId: 88,
        gameMasterName: 'Test GM',
      };

      myCampaignsAdapterServiceMock.getCampaignDetails.and.returnValue(of(campaignDetails));
      spyOn(activatedRoute.snapshot.paramMap, 'get').and.returnValue('99');

      // when
      component.ngOnInit();

      // then
      expect(myCampaignsAdapterServiceMock.getCampaignDetails).toHaveBeenCalledWith(99);
    });
  });
});
