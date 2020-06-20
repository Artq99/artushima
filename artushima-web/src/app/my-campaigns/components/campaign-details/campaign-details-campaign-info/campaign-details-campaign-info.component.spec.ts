import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignDetailsCampaignInfoComponent } from './campaign-details-campaign-info.component';
import { By } from '@angular/platform-browser';

describe('CampaignDetailsCampaignInfoComponent', () => {
  let component: CampaignDetailsCampaignInfoComponent;
  let fixture: ComponentFixture<CampaignDetailsCampaignInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CampaignDetailsCampaignInfoComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignDetailsCampaignInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });

  it('should show the campaign title', () => {
    // given
    const title: string = 'Test Campaign';
    let titleElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-info_title'))
      .nativeElement;

    // when
    component.campaignTitle = title;
    fixture.detectChanges();

    // then
    expect(titleElement.textContent).toEqual(title);
  });

  it('should show the campaign ID', () => {
    // given
    const id: number = 1234567890;
    let idElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-info_id'))
      .nativeElement;

    // when
    component.campaignId = id;
    fixture.detectChanges();

    // then
    expect(idElement.textContent).toEqual('ID: 1234567890');
  });

  it('should show the date of the campaign creation', () => {
    // given
    const date: Date = new Date(2020, 0, 1);
    let dateElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-info_created-on'))
      .nativeElement;

    // when
    component.campaignCreatedOn = date;
    fixture.detectChanges();

    // then
    expect(dateElement.textContent).toEqual('Utworzono: 01.01.2020');
  });
});
