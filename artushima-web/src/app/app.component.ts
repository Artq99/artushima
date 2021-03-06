import { Component, OnInit } from '@angular/core';
import { AuthService } from './core/services/auth.service';

/**
 * The master component of the application.
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  public constructor(private authService: AuthService) { }

  public ngOnInit(): void {

    this.authService.validateInitialLogin();
  }
}
