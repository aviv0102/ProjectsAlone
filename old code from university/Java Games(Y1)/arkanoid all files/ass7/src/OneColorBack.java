
import biuoop.DrawSurface;
import java.awt.Color;
/**
* @author Aviv Shisman 206558157
*/
public class OneColorBack implements Sprite {
    //member:
    private Color color;
    /** the constructor.
     * @param color the color of the background.
     */
    public OneColorBack(Color color) {
        this.color = color;
    }
    /** adding the background as sprite to game.
     * @param g the game
     */
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
    /**drawing the background.
     * @param surface the surface for drawing
     */
    public void drawOn(DrawSurface surface) {
        surface.setColor(color);
        surface.fillRectangle(0, 0, surface.getWidth(), surface.getHeight());
    }
    /** time passed method...
     * @param dt the speed by time
     */
    public void timePassed(double dt) {
    }
}