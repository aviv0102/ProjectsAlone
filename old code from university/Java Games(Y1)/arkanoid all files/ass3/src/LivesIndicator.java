import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class LivesIndicator implements Sprite {
    //members:
    private Counter lives;
    /** the constructor.
     * @param lives the lives */
    public LivesIndicator(Counter lives) {
        this.lives = lives;
    }
    /** add the indicator to the sprite.
     * @param g the game.
     */
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
    /**draw the lives to the screen.
     * @param d the draw surface*/
    public void drawOn(DrawSurface d) {
        d.drawText(200, 15, "Lives:", 15);
        d.drawText(250, 15, Integer.toString(lives.getValue()), 15);
    }
    /**the time passed method.
     * @param dt the speed by time*/
    public void timePassed(double dt) {

    }

}
