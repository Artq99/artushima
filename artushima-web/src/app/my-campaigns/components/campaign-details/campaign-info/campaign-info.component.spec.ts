import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';
import { CampaignInfoComponent } from './campaign-info.component';


describe('CampaignInfoComponent', () => {
  let component: CampaignInfoComponent;
  let fixture: ComponentFixture<CampaignInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FontAwesomeModule,
        SharedModule
      ],
      declarations: [CampaignInfoComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampaignInfoComponent);
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
      .query(By.css('#campaign-info_campaign-title'))
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
      .query(By.css('#campaign-info_campaign-id'))
      .nativeElement;

    // when
    component.campaignId = id;
    fixture.detectChanges();

    // then
    expect(idElement.textContent).toEqual('1234567890');
  });

  it('should show the date of the campaign creation', () => {
    // given
    const date: Date = new Date(2020, 0, 1);
    let dateElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-info_campaign-created-on'))
      .nativeElement;

    // when
    component.campaignCreatedOn = date;
    fixture.detectChanges();

    // then
    expect(dateElement.textContent).toEqual('01.01.2020');
  });
});
