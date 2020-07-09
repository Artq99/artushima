import { Component, Input } from '@angular/core';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

/**
 * The header widget.
 *
 * Displays an icon and a title. Additionaly it is possible to give an ID
 * for the span tag containing the title (for testing purposes).
 */
@Component({
  selector: 'artushima-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  /** The icon. */
  @Input()
  public icon: IconDefinition;

  /** The title. */
  @Input()
  public title: string;

  /** The ID for the span tag with title. */
  @Input()
  public titleId: string;
}
