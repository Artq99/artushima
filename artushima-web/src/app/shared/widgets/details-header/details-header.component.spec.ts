import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailsHeaderComponent } from './details-header.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SharedModule } from '../../shared.module';

describe('DetailsHeaderComponent', () => {
  let component: DetailsHeaderComponent;
  let fixture: ComponentFixture<DetailsHeaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FontAwesomeModule,
        SharedModule
      ],
      declarations: [DetailsHeaderComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DetailsHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });
});
