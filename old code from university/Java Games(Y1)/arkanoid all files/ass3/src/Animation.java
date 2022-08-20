
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public interface Animation {
   /** drawing one frame on the screen.
   * @param d the drawsurface.
   * @param dt the speed. */
    void doOneFrame(DrawSurface d, double dt);
   /** telling the animationrunner if he need to stop.
   * @return the result */
   boolean shouldStop();
}