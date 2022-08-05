import java.awt.Color;

import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class DirectHitBack implements Sprite {
    /** drawing the Background to the screen.
     * @param d the drawSurface*/
    public void drawOn(DrawSurface d) {
        d.setColor(Color.black);
        d.fillRectangle(0, 0, 800, 600);
        d.setColor(Color.blue);
        d.drawCircle(400, 100, 70);
        d.drawCircle(400, 100, 50);
        d.drawCircle(400, 100, 30);
        d.drawLine(300, 100, 500, 100);
        d.drawLine(400, 0, 400, 200);
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
