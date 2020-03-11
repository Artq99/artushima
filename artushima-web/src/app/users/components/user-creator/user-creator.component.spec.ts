import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';

import { UserCreatorComponent } from './user-creator.component';

describe('UserCreatorComponent', () => {

  let component: UserCreatorComponent;
  let fixture: ComponentFixture<UserCreatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [UserCreatorComponent],
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        FormsModule
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    // then
    expect(component).toBeTruthy();
  });
});
