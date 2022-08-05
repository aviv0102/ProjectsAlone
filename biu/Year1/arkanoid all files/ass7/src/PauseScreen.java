import biuoop.DrawSurface;

/**
* @author Aviv Shisman 206558157
*/
public class PauseScreen implements Animation {
    //memebers:
    private boolean stop;
    /**the constructor.*/
    public PauseScreen() {
        this.stop = false;
    }
    /** drawing the pause screen.
     *@param d the draw surface
     *@param dt ...*/
    public void doOneFrame(DrawSurface d, double dt) {
        d.drawText(10, d.getHeight() / 2, "paused -- press space to continue", 32);

    }
    /**telling the animation runner to stop.
     * @return to stop or not*/
    public boolean shouldStop() {
        this.stop = true;
        return this.stop;
    }
}