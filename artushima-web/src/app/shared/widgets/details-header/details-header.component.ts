import { Component, Input } from '@angular/core';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

/**
 * The header for a details page.
 *
 * Requires the icon and the title as input. Additional information can be
 * passed as body for the component and the elements can be tags with
 * the 'col-' classes, since the component is a fluid-container itself
 * and the elements will be enveloped in a div-tag with the 'row' class.
 */
@Component({
  selector: 'artushima-details-header',
  templateUrl: './details-header.component.html',
  styleUrls: ['./details-header.component.scss']
})
export class DetailsHeaderComponent {

  /** The icon. */
  @Input()
  public icon: IconDefinition;

  /** The text for the title. */
  @Input()
  public title: string;

  /** The ID that should be assigned to the 'span' tag containing the title. */
  @Input()
  public titleId: string;
}
