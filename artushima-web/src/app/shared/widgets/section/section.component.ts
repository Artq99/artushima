import { Component, Input } from '@angular/core';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

/**
 * The component that shows a formated section block of the page.
 */
@Component({
  selector: 'artushima-section',
  templateUrl: './section.component.html',
  styleUrls: ['./section.component.scss']
})
export class SectionComponent {

  /** The icon. */
  @Input()
  public icon: IconDefinition;

  /** The title. */
  @Input()
  public title: string;
}
