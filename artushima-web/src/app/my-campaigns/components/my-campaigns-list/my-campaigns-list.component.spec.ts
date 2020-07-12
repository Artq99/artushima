import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DebugElement } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { MyCampaignsListElement } from '../../model/my-campaigns-list-response.model';
import { MyCampaignsListComponent } from './my-campaigns-list.component';

describe('MyCampaignsListComponent', () => {

  // test data
  const campaign1: MyCampaignsListElement = new MyCampaignsListElement();
  campaign1.id = 1;
  campaign1.campaignName = 'Campaign 1';

  const campaing2: MyCampaignsListElement = new MyCampaignsListElement();
  campaing2.id = 2;
  campaing2.campaignName = 'Campaign 2';

  const myCampaingsList: MyCampaignsListElement[] = [
    campaign1,
    campaing2
  ];

  let fixture: ComponentFixture<MyCampaignsListComponent>;
  let component: MyCampaignsListComponent;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        declarations: [
          MyCampaignsListComponent
        ],
        imports: [
          HttpClientTestingModule,
          RouterTestingModule,
          FontAwesomeModule
        ]
      })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MyCampaignsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should display the list of campaigns', () => {
    // given
    component.myCampaigns = myCampaingsList;

    // when
    fixture.detectChanges();

    // then
    const myCampaignsListTableBody: DebugElement = fixture.debugElement.query(By.css('#my-campaigns-list-table-body'));
    expect(myCampaignsListTableBody.children.length).toEqual(2);

    const campaignRow1: DebugElement = myCampaignsListTableBody.children[0];
    const campaignRow2: DebugElement = myCampaignsListTableBody.children[1];

    const COL_ID = 0;
    const COL_CAMPAIGN_NAME = 1;

    expect(campaignRow1.children[COL_ID].nativeElement.textContent).toContain(campaign1.id);
    expect(campaignRow1.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(campaign1.campaignName);
    expect(campaignRow2.children[COL_ID].nativeElement.textContent).toContain(campaing2.id);
    expect(campaignRow2.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(campaing2.campaignName);
  });

  // TODO Tests for the button navigating to the campaign details
});
