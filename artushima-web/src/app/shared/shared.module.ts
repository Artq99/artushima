import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DefaultIconPipe } from './pipes/default-icon/default-icon.pipe';
import { DetailsHeaderComponent } from './widgets/details-header/details-header.component';
import { SectionComponent } from './widgets/section/section.component';

/**
 * The module for shared resources.
 */
@NgModule({
  declarations: [
    // Components
    DetailsHeaderComponent,
    SectionComponent,
    // Pipes
    DefaultIconPipe
  ],
  imports: [
    CommonModule,
    FontAwesomeModule
  ],
  exports: [
    // Components
    DetailsHeaderComponent,
    SectionComponent,
    // Pipes
    DefaultIconPipe
  ]
})
export class SharedModule { }
