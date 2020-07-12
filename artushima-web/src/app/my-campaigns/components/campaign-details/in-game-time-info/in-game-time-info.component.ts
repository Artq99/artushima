import { Component, Input } from '@angular/core';
import { faClock, IconDefinition } from '@fortawesome/free-solid-svg-icons';

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

  /** The icon for the header. */
  public iconClock: IconDefinition = faClock;

  /** The in-game date when the campaign started. */
  @Input()
  public startDate: Date;

  /** The number of days that passed since the start date. */
  @Input()
  public passedDays: number;

  /** The current in-game date. */
  @Input()
  public currentDate: Date;
}
