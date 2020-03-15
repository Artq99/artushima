import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MyCampaignsListComponent } from './my-campaigns-list.component';

describe('MyCampaignsListComponent', () => {

  let component: MyCampaignsListComponent;
  let fixture: ComponentFixture<MyCampaignsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MyCampaignsListComponent]
    }).compileComponents();
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
});
