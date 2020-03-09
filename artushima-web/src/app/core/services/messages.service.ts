import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

import { Message } from 'src/app/core/model/message';
import { MessageLevel } from 'src/app/core/model/message-level';

/**
 * The service for managing messages (alerts) shown to the user.
 */
@Injectable({
  providedIn: 'root'
})
export class MessagesService {

  private messagesSubject: Subject<Message>;

  /**
   * The observable that emits messages.
   */
  public messages$: Observable<Message>;

  public constructor() {

    this.messagesSubject = new Subject<Message>();
    this.messages$ = this.messagesSubject.asObservable();
  }

  /**
   * Show a new message.
   *
   * @param text the text of a new message
   * @param level the severity level of the new message
   */
  public showMessage(text: string, level: MessageLevel): void {

    let message: Message = new Message(text, level);
    this.messagesSubject.next(message);
  }
}
