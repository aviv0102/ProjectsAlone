
import biuoop.DrawSurface;
import java.awt.Image;
/**
* @author Aviv Shisman 206558157
*/
public class ImgBack implements Sprite {
    //members:
    private Image image;
    /**the constructor.
     * @param image the image we get.
     */
    public ImgBack(Image image) {
        this.image = image;
    }
    /**adding to game...
     * @param g the game.
     */
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
    /**drawing the image background.
     * @param surface the surface of drawing
     */
    public void drawOn(DrawSurface surface) {
        surface.drawImage(0, 0, image);
    }
    /**the time passed method...
     * @param dt the speed by time
     */
    public void timePassed(double dt) {
    }
}
