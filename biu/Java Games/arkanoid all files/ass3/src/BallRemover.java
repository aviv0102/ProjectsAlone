
/**
* @author Aviv Shisman 206558157
*/
public class BallRemover implements HitListener {
    //the members:
    private GameLevel gameLevel;
    private Counter remainingBalls;
    /** the constructor.
     * @param gameLevel the game we use the counter for.
     * @param remianingBalls the number of balls*/
    public BallRemover(GameLevel gameLevel, Counter remianingBalls) {
        this.gameLevel = gameLevel;
        this.remainingBalls = remianingBalls;
    }
    /** the constructor.
     * @param beingHit the block being hit.
     * @param hitter the ball that hits*/
    public void hitEvent(Block beingHit, Ball hitter) {
        hitter.removeFromGame(gameLevel);
        this.remainingBalls.decrease(1);
    }

}
