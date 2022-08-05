import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class LevelIndicator implements Sprite {
    //memebers:
    private GameLevel game;
    /** the constructor.
     * @param g the game*/
    public LevelIndicator(GameLevel g) {
        this.game = g;
    }
    /** add the indicator to the sprite.
     * @param g the game.
     */
    public void addToGame(GameLevel g) {
        g.addSprite(this);
    }
    /**draw the level to the screen.
     * @param d the draw surface*/
    public void drawOn(DrawSurface d) {
        d.drawText(600, 15, "Level:", 15);
        d.drawText(650, 15, this.game.getData().levelName(), 15);
    }
    /**the time passed method.
     * @param dt the speed by time*/
    public void timePassed(double dt) {

    }
}
