import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from 'src/app/shared/shared.module';
import { CampaignInfoComponent } from './campaign-info.component';

describe('CampaignInfoComponent', () => {
  let component: CampaignInfoComponent;
  let fixture: ComponentFixture<CampaignInfoComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
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

  it('should show the ID of a campaign', () => {
    // given
    const id: number = 1234567890;
    const idElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__campaign-info__id'))
      .nativeElement;

    // when
    component.id = id;
    fixture.detectChanges();

    // then
    expect(idElement.textContent).toEqual('1234567890');
  });

  it('should show the creation date of a campaign', () => {
    // given
    const date: Date = new Date(2020, 0, 1);
    const dateElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__campaign-info__creationDate'))
      .nativeElement;

    // when
    component.creationDate = date;
    fixture.detectChanges();

    // then
    expect(dateElement.textContent).toEqual('01.01.2020');
  });

  it('should show the game master\'s name', () => {
    // given
    const gameMasterName: string = 'Test GM';
    const gameMasterNameElement: HTMLElement = fixture
      .debugElement
      .query(By.css('#campaign-details__campaign-info__gameMasterName'))
      .nativeElement;

    // when
    component.gameMasterName = gameMasterName;
    fixture.detectChanges();

    // then
    expect(gameMasterNameElement.textContent).toEqual(gameMasterName);
  });
});
