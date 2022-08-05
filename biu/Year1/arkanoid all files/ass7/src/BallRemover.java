
/**
* @author Aviv Shisman 206558157
*/
public class BallRemover implements HitListener {
    //the members:
    private GameLevel gameLevel;
    /** the constructor.
     * @param gameLevel the game we use the counter for. */
    public BallRemover(GameLevel gameLevel) {
        this.gameLevel = gameLevel;
    }
    /** the constructor.
     * @param beingHit the block being hit.
     * @param hitter the ball that hits*/
    public void hitEvent(Block beingHit, Ball hitter) {
        hitter.removeFromGame(gameLevel);
       
    }

}
