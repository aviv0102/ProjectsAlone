
import biuoop.DrawSurface;
/**
 * @author Aviv Shisman 206558157
 */
public interface Sprite {
    /** drawing to the screen an object.
     * @param d the surface*/
    void drawOn(DrawSurface d);
    /**notify the object that time has passed.
     * and it will act appon it
     * @param dt the speed by time */
    void timePassed(double dt);
    /**a method to add an object to game.
     * @param g the game */
    void addToGame(GameLevel g);
}