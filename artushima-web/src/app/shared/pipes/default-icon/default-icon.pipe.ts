import { Pipe, PipeTransform } from '@angular/core';
import { IconDefinition, faInfoCircle } from '@fortawesome/free-solid-svg-icons';

/**
 * The pipe that evaluates if the given icon is defined. If yes, returns
 * the same icon. Otherwise it returns the default icon.
 */
@Pipe({
  name: 'defaultIcon'
})
export class DefaultIconPipe implements PipeTransform {

  public transform(icon: IconDefinition | null): IconDefinition {
    return icon ? icon : faInfoCircle;
  }

}
