import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

// Components
import { MyCampaignsListComponent } from './my-campaigns-list.component';

// Model
import { MyCampaignsListElement } from '../../model/my-campaigns.model';

describe('MyCampaignsListComponent', () => {

  // test data
  let campaign1: MyCampaignsListElement = new MyCampaignsListElement();
  campaign1.id = 1;
  campaign1.campaignName = 'Campaign 1';

  let campaing2: MyCampaignsListElement = new MyCampaignsListElement();
  campaing2.id = 2;
  campaing2.campaignName = 'Campaign 2';

  let myCampaingsList: MyCampaignsListElement[] = [
    campaign1,
    campaing2
  ]

  // The fixture
  let fixture: ComponentFixture<MyCampaignsListComponent>;

  // the component under test
  let myCampaignsListComponent: MyCampaignsListComponent;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        declarations: [
          MyCampaignsListComponent
        ],
        imports: [
          HttpClientTestingModule
        ]
      })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MyCampaignsListComponent);
    myCampaignsListComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(myCampaignsListComponent).toBeTruthy();
  });

  it('should display the list of campaigns', () => {
    // given
    myCampaignsListComponent.myCampaigns = myCampaingsList;

    // when
    fixture.detectChanges();

    // then
    let myCampaignsListTableBody: DebugElement = fixture.debugElement.query(By.css('#my-campaigns-list-table-body'));
    expect(myCampaignsListTableBody.children.length).toEqual(2);

    let campaignRow1: DebugElement = myCampaignsListTableBody.children[0];
    let campaignRow2: DebugElement = myCampaignsListTableBody.children[1];

    const COL_ID = 0;
    const COL_CAMPAIGN_NAME = 1;

    expect(campaignRow1.children[COL_ID].nativeElement.textContent).toContain(campaign1.id);
    expect(campaignRow1.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(campaign1.campaignName);
    expect(campaignRow2.children[COL_ID].nativeElement.textContent).toContain(campaing2.id);
    expect(campaignRow2.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(campaing2.campaignName);
  });
});
