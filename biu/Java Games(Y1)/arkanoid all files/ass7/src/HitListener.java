/**
* @author Aviv Shisman 206558157
*/
public interface HitListener {
    /** notify that a hit occurd.
     * @param beingHit the block
     * @param hitter the ball that hits*/
    void hitEvent(Block beingHit, Ball hitter);
}
