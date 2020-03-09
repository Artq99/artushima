import { async, ComponentFixture, TestBed, tick, fakeAsync } from '@angular/core/testing';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

import { MessagesService } from '../../services/messages.service';

import {
  MessagesComponent,
  MESSAGE_TIMEOUT
} from './messages.component';

import { MessageLevel } from 'src/app/core/model/message-level';

describe('MessagesComponent', () => {

  let fixture: ComponentFixture<MessagesComponent>;
  let messagesComponent: MessagesComponent;
  let messagesService: MessagesService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MessagesComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MessagesComponent);
    messagesComponent = fixture.componentInstance;
    fixture.detectChanges();
    messagesService = TestBed.get(MessagesService);
  });

  it('should create', () => {

    // then
    expect(messagesComponent).toBeTruthy();
  });

  it('should display an info message', () => {

    // when
    messagesService.showMessage('test message', MessageLevel.INFO);
    fixture.detectChanges()

    // then
    let messagesDE: DebugElement = fixture.debugElement.query(By.css('.art-message-box'));
    expect(messagesDE.children.length).toEqual(1);
    expect(messagesDE.children[0].classes['alert-primary']).toBeTruthy();
    expect(messagesDE.children[0].nativeElement.textContent).toContain('test message');
  });

  it('should display a warning message', () => {

    // when
    messagesService.showMessage('test message', MessageLevel.WARNING);
    fixture.detectChanges();

    // then
    let messagesDE: DebugElement = fixture.debugElement.query(By.css('.art-message-box'));
    expect(messagesDE.children.length).toEqual(1);
    expect(messagesDE.children[0].classes['alert-warning']).toBeTruthy();
    expect(messagesDE.children[0].nativeElement.textContent).toContain('test message');
  });

  it('should display an error message', () => {

    // when
    messagesService.showMessage('test message', MessageLevel.ERROR);
    fixture.detectChanges();

    // then
    let messageDE: DebugElement = fixture.debugElement.query(By.css('.art-message-box'));
    expect(messageDE.children.length).toEqual(1);
    expect(messageDE.children[0].classes['alert-danger']).toBeTruthy();
    expect(messageDE.children[0].nativeElement.textContent).toContain('test message');
  });

  it('should remove a message after timeout', fakeAsync(() => {

    // given
    let messageDE: DebugElement = fixture.debugElement.query(By.css('.art-message-box'));

    // when
    messagesService.showMessage('test message', MessageLevel.INFO);

    // then
    fixture.detectChanges()
    expect(messageDE.children.length).toEqual(1);

    tick(MESSAGE_TIMEOUT + 1);

    fixture.detectChanges();
    expect(messageDE.children.length).toEqual(0);
  }));
});
