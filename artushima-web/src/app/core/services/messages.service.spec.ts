import { TestBed } from '@angular/core/testing';

import { MessagesService } from './messages.service';

import { MessageLevel } from 'src/app/core/model/message-level';
import { Message } from 'src/app/core/model/message';

describe('MessagesService', () => {

  let messagesService: MessagesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});

    messagesService = TestBed.get(MessagesService);
  });

  it('should be created', () => {

    // then
    expect(messagesService).toBeTruthy();
  });

  describe('showMessage', () => {

    it('should emit a new message', () => {

      // when then
      messagesService.messages$
        .subscribe(message => expect(message).toEqual(new Message('test message', MessageLevel.INFO)));
      messagesService.showMessage('test message', MessageLevel.INFO);
    });
  });
});
