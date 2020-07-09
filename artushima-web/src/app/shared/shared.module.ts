import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DefaultIconPipe } from './pipes/default-icon/default-icon.pipe';
import { HeaderComponent } from './widgets/header/header.component';
import { SectionComponent } from './widgets/section/section.component';

/**
 * The module for shared resources.
 */
@NgModule({
  declarations: [
    // Pipes
    DefaultIconPipe,
    // Components
    HeaderComponent,
    SectionComponent
  ],
  imports: [
    CommonModule,
    FontAwesomeModule
  ],
  exports: [
    // Pipes
    DefaultIconPipe,
    // Components
    HeaderComponent,
    SectionComponent
  ]
})
export class SharedModule { }
