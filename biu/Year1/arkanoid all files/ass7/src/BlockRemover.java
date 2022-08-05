
/**
* @author Aviv Shisman 206558157
*/
public class BlockRemover implements HitListener {
    //the members:
    private GameLevel gameLevel;
    private Counter remainingBlocks;
    /** the constructor.
     * @param gameLevel the game we use the counter for.
     * @param remianingBlock the number of blocks*/
    public BlockRemover(GameLevel gameLevel, Counter remianingBlock) {
        this.gameLevel = gameLevel;
        this.remainingBlocks = remianingBlock;
    }
    /** the constructor.
     * @param beingHit the block being hit.
     * @param hitter the ball that hits*/
    public void hitEvent(Block beingHit, Ball hitter) {
        if (beingHit.getLife() == 0) {
            beingHit.removeHitListener(this);
            beingHit.removeFromGame(this.gameLevel);
            this.remainingBlocks.decrease(1);
        }
    }

}
