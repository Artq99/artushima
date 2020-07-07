import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { DetailsHeaderComponent } from './widgets/details-header/details-header.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DefaultIconPipe } from './pipes/default-icon/default-icon.pipe';

/**
 * The module for shared resources.
 */
@NgModule({
  declarations: [
    // Components
    DetailsHeaderComponent,
    // Pipes
    DefaultIconPipe],
  imports: [
    CommonModule,
    FontAwesomeModule
  ],
  exports: [
    // Components
    DetailsHeaderComponent,
    // Pipes
    DefaultIconPipe]
})
export class SharedModule { }
