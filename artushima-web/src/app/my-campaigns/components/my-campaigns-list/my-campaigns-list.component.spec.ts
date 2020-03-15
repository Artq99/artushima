import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MyCampaignsListComponent } from './my-campaigns-list.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MyCampaignsListElement } from '../../model/my-campaigns-list-element';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

describe('MyCampaignsListComponent', () => {

  // test data
  const CAMPAIGN_1 = new MyCampaignsListElement();
  CAMPAIGN_1.id = 1;
  CAMPAIGN_1.campaignName = 'Campaign 1';

  const CAMPAIGN_2 = new MyCampaignsListElement();
  CAMPAIGN_2.id = 2;
  CAMPAIGN_2.campaignName = 'Campaign 2';

  const MY_CAMPAIGNS_LIST = [
    CAMPAIGN_1,
    CAMPAIGN_2
  ]

  let fixture: ComponentFixture<MyCampaignsListComponent>;

  // the component under test
  let myCampaignsListComponent: MyCampaignsListComponent;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MyCampaignsListComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();
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
    myCampaignsListComponent.myCampaigns = MY_CAMPAIGNS_LIST;

    // when
    fixture.detectChanges();

    // then
    let myCampaignsListTableBody: DebugElement = fixture.debugElement.query(By.css('#my-campaigns-list-table-body'));
    expect(myCampaignsListTableBody.children.length).toEqual(2);

    let campaignRow1: DebugElement = myCampaignsListTableBody.children[0];
    let campaignRow2: DebugElement = myCampaignsListTableBody.children[1];

    const COL_ID = 0;
    const COL_CAMPAIGN_NAME = 1;

    expect(campaignRow1.children[COL_ID].nativeElement.textContent).toContain(CAMPAIGN_1.id);
    expect(campaignRow1.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(CAMPAIGN_1.campaignName);
    expect(campaignRow2.children[COL_ID].nativeElement.textContent).toContain(CAMPAIGN_2.id);
    expect(campaignRow2.children[COL_CAMPAIGN_NAME].nativeElement.textContent).toContain(CAMPAIGN_2.campaignName);
  });
});
