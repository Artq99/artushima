import { TestBed } from '@angular/core/testing';

import { MyCampaignsService } from './my-campaigns.service';

describe('MyCampaignsService', () => {

  let myCampaignsService: MyCampaignsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});

    myCampaignsService = TestBed.get(MyCampaignsService);
  });

  it('should be created', () => {
    // then
    expect(myCampaignsService).toBeTruthy();
  });
});
