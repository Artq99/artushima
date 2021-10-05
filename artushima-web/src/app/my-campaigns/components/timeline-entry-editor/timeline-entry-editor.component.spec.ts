import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TimelineEntryEditorComponent } from './timeline-entry-editor.component';

describe('TimelineEntryEditorComponent', () => {
  let component: TimelineEntryEditorComponent;
  let fixture: ComponentFixture<TimelineEntryEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TimelineEntryEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimelineEntryEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
