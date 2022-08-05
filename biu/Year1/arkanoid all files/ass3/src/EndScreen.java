
import biuoop.DrawSurface;
import biuoop.KeyboardSensor;

/**
* @author Aviv Shisman 206558157
*/
public class EndScreen implements Animation {
    //the members:
    private boolean stop;
    private Counter score;
    private int result;
    /** the constructor.
     * @param k the KeyboardSensor
     * @param s the counter
     * @param result if the player won or not */
    public EndScreen(KeyboardSensor k, Counter s, int result) {
        this.stop = false;
        this.score = s;
        this.result = result;
    }
    /**running the end screen.
     * @param d the drawSurface
     * @param dt the speed by sec*/
    public void doOneFrame(DrawSurface d, double dt) {
        if (result == 1) {
            d.drawText(20, d.getHeight() / 6,
                    "Thank you for playing!, Your score is:"
            + Integer.toString(score.getValue()), 40);
        }
        if (result == 0) {
            d.drawText(10, d.getHeight() / 6, "Game Over. Your score is :"
        + Integer.toString(score.getValue()), 32);
        }
        d.drawText(150, 555, "Press Space to Continue", 30);
    }
    /** if the animation should stop stops it.
     * @return the answer */
    /**telling the animation runner to stop.
     * @return to stop or not*/
    public boolean shouldStop() {
        this.stop = true;
        return this.stop;
    }
}
