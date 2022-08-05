
/**
* @author Aviv Shisman 206558157
*/
public interface Collidable {
    /**
    * @return the collision retangle*/
    Rectangle getCollisionRectangle();
    /** giving the ball new velocity after he hit a collidable.
    * @param collisionPoint the point that will be the collison.
    * @param currentVelocity the velocity of the ball
    * @param hitter the ball that hits.
    * @return the new velocity*/
    Velocity hit(Ball hitter, Point collisionPoint, Velocity currentVelocity);
}
