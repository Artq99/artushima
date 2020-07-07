import { DefaultIconPipe } from './default-icon.pipe';
import { IconDefinition, faJedi, faInfoCircle } from '@fortawesome/free-solid-svg-icons';

describe('DefaultIconPipe', () => {
  let pipe: DefaultIconPipe;

  beforeEach(() => {
    pipe = new DefaultIconPipe();
  })

  it('should be created', () => {
    // then
    expect(pipe).toBeTruthy();
  });

  describe('transform', () => {

    it('should return the same icon when it is provided', () => {
      // given
      const icon: IconDefinition = faJedi;

      // when
      let resultIcon: IconDefinition = pipe.transform(icon);

      // then
      expect(resultIcon).toEqual(icon);
    });

    it('should return the default icon when none is provided', () => {
      // when
      let resultIcon: IconDefinition = pipe.transform(null);

      // then
      expect(resultIcon).toEqual(faInfoCircle);
    });
  });
});
