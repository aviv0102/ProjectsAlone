
/**
* @author Aviv Shisman 206558157
*/
public class Velocity {
    //members:
    private double dx;
    private double dy;
     /** the constructor.
     * @param dx the horizontal speed.
     * @param dy the vertical speed. */
    public Velocity(double dx, double dy) {
        this.dx = dx;
        this.dy = dy;
    }
    /** the constructor.
    * @param v the velocity. */
    public Velocity(Velocity v) {
        this.dx = v.getDX();
        this.dy = v.getDY();
    }
    /** applying the speed to the point and there for moving the ball.
     * @param p the center of the ball which we move.
     * @return the new point after moving it.*/
    public Point applyToPoint(Point p) {
        Point newP = new Point(p.getX() + this.dx, p.getY() + this.dy);
        return newP;
    }
    /** Retrieve the dx.
     * @return the horizontal speed.*/
    public double getDX() {
        return this.dx;
    }
    /** Retrieve the dy.
     * @return the vertical speed.*/
    public double getDY() {
        return this.dy;
    }
    /** if the user prefer to use angle and speed this is the method.
     * constructing a vector by applying to speed and angle to the furmula.
     * @param angle the angle.
     * @param speed the speed.
     * @return the new velocity.*/
    public static Velocity fromAngleAndSpeed(double angle, double speed) {
        double dx = Math.cos(Math.toRadians(angle - 90)) * speed;
        double dy = Math.sin(Math.toRadians(angle - 90)) * speed;

        return new Velocity(dx, dy);
    }

}