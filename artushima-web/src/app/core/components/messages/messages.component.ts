import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { Subscription } from 'rxjs';

import { MessagesService } from '../../services/messages.service';

import { Message } from 'src/app/core/model/message';

export const MESSAGE_TIMEOUT = 5000;

/**
 * The component responsible for displaying messages (alerts).
 */
@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.scss']
})
export class MessagesComponent implements OnInit, OnDestroy {

  private messagesSubscription: Subscription;

  @Input()
  public messages: Message[] = [];

  public constructor(private messagesService: MessagesService) { }

  public ngOnInit() {

    this.messagesSubscription = this.messagesService.messages$.subscribe(
      message => {
        this.messages.push(message);
        setTimeout(
          () => {
            let index: number = this.messages.indexOf(message);
            if (index !== -1) {
              this.messages.splice(index, 1);
            }
          },
          MESSAGE_TIMEOUT
        );
      }
    );
  }

  public ngOnDestroy() {

    this.messagesSubscription.unsubscribe();
  }

}
