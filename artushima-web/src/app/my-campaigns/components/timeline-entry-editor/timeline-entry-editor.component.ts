import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { IconDefinition } from '@fortawesome/fontawesome-common-types';
import { faFeatherAlt } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-timeline-entry-editor',
  templateUrl: './timeline-entry-editor.component.html',
  styles: []
})
export class TimelineEntryEditorComponent {

  /** The icon for the header. */
  public iconSummarizeSession: IconDefinition = faFeatherAlt;

  /** The form group for the new entry. */
  public entryFormGroup = new FormGroup({
    title: new FormControl('', [Validators.required]),
    sessionDate: new FormControl('', [Validators.required]),
    summaryText: new FormControl('')
  });

  /**
   * The callback for the onSubmit event.
   */
  public onSubmit(): void {
    console.log(this.entryFormGroup.getRawValue());
  }
}
