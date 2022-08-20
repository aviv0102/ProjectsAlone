import java.awt.Color;

import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class SunnyDayBack implements Sprite {
    /** drawing the Background to the screen.
     * @param d the drawSurface*/
    public void drawOn(DrawSurface d) {
        d.setColor(Color.white);
        d.fillRectangle(0, 0, 800, 600);
        d.setColor(Color.decode("#efe7b0"));
        d.fillCircle(150, 150, 50);
        d.setColor(Color.decode("#ecd749"));
        d.fillCircle(150, 150, 40);
        d.setColor(Color.decode("#ffe148"));
        d.fillCircle(150, 150, 30);
        for (int i = 25; i < 720; i += 15) {
            d.setColor(Color.decode("#efe7b0"));
            d.drawLine(150, 150, 0 + i, 250);
        }

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
