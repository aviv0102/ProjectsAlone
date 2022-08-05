
import java.awt.Color;
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class FinalFourBack implements Sprite {
    /** drawing the Background to the screen.
     * @param d the drawSurface*/
    public void drawOn(DrawSurface d) {
        d.setColor(Color.cyan);

        d.fillRectangle(0, 0, 800, 600);
        d.setColor(Color.white);
        for (int i = 1; i <= 50; i += 5) {
            d.drawLine(90 + i, 410, 75 + i, 600);
        }
        for (int i = 1; i <= 50; i += 5) {
            d.drawLine(590 + i, 510, 575 + i, 600);
        }
        d.setColor(Color.white);
        d.fillCircle(590, 505, 15);
        d.fillCircle(600, 520, 20);
        d.setColor(Color.lightGray);
        d.fillCircle(610, 495, 20);
        d.setColor(Color.gray);
        d.fillCircle(625, 505, 25);
        d.fillCircle(618, 525, 15);
        d.setColor(Color.white);
        d.fillCircle(90, 405, 15);
        d.fillCircle(100, 420, 20);
        d.setColor(Color.lightGray);
        d.fillCircle(110, 395, 20);
        d.setColor(Color.gray);
        d.fillCircle(125, 405, 25);
        d.fillCircle(118, 425, 15);

    }
    /** the time passed empty function.*/
    public void timePassed(double dt) {
    }
    /** adding the backGround to the sprite's.
     * @param g the game*/
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
}
