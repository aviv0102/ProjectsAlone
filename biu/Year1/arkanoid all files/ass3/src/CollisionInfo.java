
/**
* @author Aviv Shisman 206558157
*/
public class CollisionInfo {
    //members:
    private Point collisionP;
    private Collidable collisonObject;
    /** the constructor for points.
     * @param p the point of collision
     * @param o the object of collision */
    public CollisionInfo(Point p, Collidable o) {
        this.collisionP = p;
        this.collisonObject = o;
    }
    /** getting the point of collision.
     * @return the point */
    public Point collisionPoint() {
        return this.collisionP;
    }
    /** getting the object of collision.
     * @return the object */
    public Collidable collisionObject() {
        return this.collisonObject;
    }

}
