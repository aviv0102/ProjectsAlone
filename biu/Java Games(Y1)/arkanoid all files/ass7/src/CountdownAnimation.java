
import biuoop.DrawSurface;
import java.awt.Color;
/**
* @author Aviv Shisman 206558157
*/

public class CountdownAnimation implements Animation {
    //the memebers:
    private double numOfSeconds;
    private SpriteCollection gameScreen;
    private boolean stop;
    /** the constructor.
     * @param numOfSeconds the number of seconds the pause run.
     * @param gameScreen the sprite collection which will be displayed*/
    public CountdownAnimation(double numOfSeconds, SpriteCollection gameScreen) {
        this.numOfSeconds = numOfSeconds;
        this.gameScreen = gameScreen;
    }
    /** running the countdown screen.
     * @param d the drawSurface
     * @param dt the speed by sec*/
    public void doOneFrame(DrawSurface d, double dt) {
        biuoop.Sleeper sleeper = new biuoop.Sleeper();
        gameScreen.drawAllOn(d);
        d.setColor(Color.yellow);
        if (this.numOfSeconds <= 0.0) {
            String s = "Go! :)";
            d.drawText(d.getWidth() / 2, d.getHeight() / 2, s, 30);
        } else {
            d.drawText(d.getWidth() / 2, d.getHeight() / 2
                    , String.valueOf((int) this.numOfSeconds), 30);
        }
        sleeper.sleepFor(700);
        if (this.numOfSeconds < 0.0) {
            this.stop = true;
        }
        if (this.numOfSeconds >= 0) {
            this.numOfSeconds -= 1;
        }

    }
    /** stoping the animation.
     * @return if to stop*/
    public boolean shouldStop() {
        return this.stop;
    }

}
