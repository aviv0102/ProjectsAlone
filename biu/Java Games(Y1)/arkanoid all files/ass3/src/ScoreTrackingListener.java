
/**
* @author Aviv Shisman 206558157
*/
public class ScoreTrackingListener implements HitListener {
    //members:
    private Counter points;
    /**the constructor.
     * @param points the points counter*/
    public ScoreTrackingListener(Counter points) {
        this.points = points;
    }
    /** each time a hit occourd increase the score accordingly.
     * @param hitter the ball that hits
     * @param beingHit the block that we hit*/
    public void hitEvent(Block beingHit, Ball hitter) {
        if (beingHit.getLife() == 0) {
            points.increase(10);
        }
        points.increase(5);
    }

}
