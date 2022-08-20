
import java.util.List;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
*/
public class GameEnvironment {
    // members:
    private List<Collidable> arr;
    /** the constructor builds a array of collidables.*/
    public GameEnvironment() {
        this.arr = new ArrayList<Collidable>();
    }
    /** get the collidable arr.
     * @return the arr*/
    public List<Collidable> getArr() {
        return this.arr;
    }
    /** add collidable to the array.
     * @param c the object we add*/
    public void addCollidable(Collidable c) {
        this.arr.add(c);
    }
    /** remove collidable from the array.
     * @param c the object we remove*/
    public void removeCollidalbe(Collidable c) {
        arr.remove(c);
    }
    /** get the closest collision from all the objects.
     * @param trajectory the line of the ball movment
     * @return the collisioninfo(point and object) */
    public CollisionInfo getClosestCollision(Line trajectory) {
        List<Point> points = new ArrayList<Point>();
        List<Collidable> objects = new ArrayList<Collidable>();
        for (int i = 0; i < arr.size(); i++) {
            Rectangle rect = arr.get(i).getCollisionRectangle();
            if (trajectory.closestIntersectionToStartOfLine(rect) != null) {
                points.add(trajectory.closestIntersectionToStartOfLine(rect));
                objects.add(arr.get(i));
            }
        }
        if (points.isEmpty()) {
            return null;
        } else {
            Point closestP = points.get(0);
            Collidable newObject = objects.get(0);
            for (int i = 0; i < points.size(); i++) {
                if (trajectory.start().distance(closestP)
                        > trajectory.start().distance(points.get(i))) {
                    closestP = points.get(i);
                    newObject = objects.get(i);
                }
            }
            return new CollisionInfo(closestP, newObject);
        }
    }

}