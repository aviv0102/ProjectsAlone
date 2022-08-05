import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class ScoreIndicator implements Sprite {
    //members:
    private Counter points;
    /** the constructor.
     * @param points the points we scored */
    public ScoreIndicator(Counter points) {
        this.points = points;
    }
    /** add the indicator to the sprite.
     * @param g the game.
     */
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
    /**draw the score to the screen.
     * @param d the draw surface*/
    public void drawOn(DrawSurface d) {
        d.drawText(100, 15, "Score:", 15);
        d.drawText(150, 15, Integer.toString(points.getValue()), 15);
    }
    /**the time passed method.
     * @param dt ...*/
    public void timePassed(double dt) {

    }

}
