import java.awt.Color;

import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class Green3Back implements Sprite {
    /** drawing the Background to the screen.
     * @param d the drawSurface*/
    public void drawOn(DrawSurface d) {
        d.setColor(Color.GREEN);
        d.fillRectangle(0, 0, 800, 600);
        d.setColor(Color.black);
        d.fillRectangle(40, 450, 100, 150);
        d.setColor(Color.white);
        int k = 0;
        int h = 0;
        for (int i = 1; i <= 25; i++) {
            d.fillRectangle(45 + h, 455 + k, 10, 25);
            h += 20;
            if (i % 5 == 0) {
                h = 0;
                k += 30;
            }
        }
        d.setColor(Color.DARK_GRAY);
        d.fillRectangle(75, 410, 30, 40);
        d.setColor(Color.black);
        d.fillRectangle(85, 260, 10, 150);
        d.setColor(Color.orange);
        d.fillCircle(90, 247, 13);
        d.setColor(Color.red);
        d.fillCircle(90, 247, 10);
        d.setColor(Color.yellow);
        d.fillCircle(90, 247, 5);

    }
    /** the time passed empty function.
     * @param dt the speed*/
    public void timePassed(double dt) {
    }
    /** adding the backGround to the sprite's.
     * @param g the game*/
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
}
