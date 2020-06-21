import { Component, Input } from '@angular/core';
import { IconDefinition, faClock } from '@fortawesome/free-solid-svg-icons';

/**
 * The child component that displays information about the in-game time of
 * the campaign.
 */
@Component({
  selector: 'artushima-campaign-details-in-game-time-info',
  templateUrl: './in-game-time-info.component.html',
  styleUrls: ['./in-game-time-info.component.scss']
})
export class InGameTimeInfoComponent {

  /** Clock icon. */
  public iconClock: IconDefinition = faClock;

  /** The in-game date when the campaign started. */
  @Input()
  public beginDate: Date;

  /** The number of days that passed since the begin date. */
  @Input()
  public passedDays: number;

  /** The current in-game date. */
  @Input()
  public currentDate: Date;
}
