import { MessageLevel } from './message-level';

/**
 * The class for the data of a message shown to the user.
 */
export class Message {

  public text: string;
  public level: MessageLevel;

  public constructor(text: string, level: MessageLevel) {

    this.text = text;
    this.level = level;
  }
}
