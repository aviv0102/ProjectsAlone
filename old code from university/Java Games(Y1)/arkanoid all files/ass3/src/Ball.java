
import java.util.ArrayList;
import java.util.List;
import java.awt.Color;

import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class Ball implements Sprite {
    //the members:
    private Point center;
    private int r;
    private java.awt.Color color;
    private Velocity velocity;
    private GameEnvironment env;
    private int sign;

    /** the constructor.
     * @param center the center point of the ball.
     * @param color the color we chose for the ball
     * @param r the radious of ball */
    public Ball(Point center, int r, java.awt.Color color) {
        this.center = center;
        this.r = r;
        this.color = color;
        this.velocity = new Velocity(2 * 60, 2 * 60);
        this.sign = 0;
    }
     /** another constructor.
     * @param x the x of the center
     * @param y the y of the center
     * @param color the color we chose for the ball
     * @param r the radious of ball */
    public Ball(int x, int y, int r, java.awt.Color color) {
        this.center = new Point(x, y);
        this.r = r;
        this.color = color;
        this.velocity = new Velocity(2 * 60, 2 * 60);
        this.sign = 0;
    }
     /** getting the x of the center.
     * @return the x of center. */
    public int getX() {
        return (int) center.getX();
    }
    /** getting the y of the center.
     * @return the y of center. */
    public int getY() {
        return (int) center.getY();
    }
    /** getting the size of the ball.
     * @return the size of ball. */
    public int getSize() {
        return this.r;
    }
    /** getting the color of the ball.
     * @return the color of the ball. */
    public java.awt.Color getColor() {
        return this.color;
    }
    /** drawing the ball on the surface we chose.
     * giving the ball the default boarders.
     * @param surface the drawSurface. */
    public void drawOn(DrawSurface surface) {
        surface.setColor(this.color);
        surface.fillCircle((int) this.getX(), (int) this.getY(), this.r);
        surface.setColor(Color.BLACK);
        surface.drawCircle((int) this.getX(), (int) this.getY(), this.r);

    }
    /** setting velocity of the ball.
     * @param v the new velocity.. */
    public void setVelocity(Velocity v) {
        this.velocity = v;
    }
    /** setting velocity of the ball.
     * @param dx the vertical speed.
     * @param dy the horizontal speed */
    public void setVelocity(double dx, double dy) {
        this.velocity = new Velocity(dx, dy);
    }
    /** getting the speed.
     * @return the new velocity. */
    public Velocity getVelocity() {
        return this.velocity;
    }
    /** applying movement to the ball according to the speed.
     * if the ball reaches to one of the Collidable change his direction.
     * calculating which of the objects the ball will collide by traj and other methods
     * @param dt the speed by sec*/
    public void timePassed(double dt) {
        if (this.sign == 0) {
            Velocity v = new Velocity(this.velocity.getDX() * dt, this.velocity.getDY() * dt);
            this.setVelocity(v);
            this.sign++;
        }
        Point start = new Point(this.getX(), this.getY());
        Point end = new Point(this.getX() + this.velocity.getDX(), this.getY() + this.velocity.getDY());
        Line traj = new Line(start, end);
        CollisionInfo info = env.getClosestCollision(traj);
        if (env.getClosestCollision(traj) == null) {
            this.center = this.getVelocity().applyToPoint(this.center);
        } else {
            // getting the ball close to the block and than change his speed
            // direction
            Point p = info.collisionPoint();
            this.center = new Point(center.getX() + velocity.getDX() * (0.00001),
                    this.center.getY() + velocity.getDY() * (0.00001));
            this.setVelocity(env.getClosestCollision(traj).collisionObject().
                    hit(this, p, getVelocity()));
            List<Collidable> list = new ArrayList<Collidable>(env.getArr());
            int i = 0;
            while (i < list.size()) {
                if (this.isInRect(list.get(i).getCollisionRectangle()) > 0
                        && info.collisionObject() instanceof Paddle) {
                    Collidable obj = info.collisionObject();
                    int flag = this.isInRect(list.get(i).getCollisionRectangle());
                    if (flag == 1) {
                        this.velocity = new Velocity(obj.hit(this,
                                new Point(this.getX(), obj.getCollisionRectangle().
                                        getUpperLeft().getY()), velocity));
                        this.center = new Point(center.getX(), center.getY() - 10);
                    }
                    if (flag == 2) {
                        this.velocity = new Velocity(obj.hit(this,
                                new Point(this.getX(), obj.getCollisionRectangle().
                                        getUpperLeft().getY()), velocity));
                        this.center = new Point(center.getX(), center.getY() - 20);
                    }

                    return;

                }
                i++;
            }
            this.center = new Point(center.getX() + 0.5 * velocity.getDX()
            , center.getY() + 0.5 * velocity.getDY());


        }
    }
    /**checking if the ball is in the rect(paddle).
     * @param rect the rectangle
     * @return the result*/
    public int isInRect(Rectangle rect) {
        if (this.center.getX() < rect.getUpperLeft().getX() + rect.getWidth()
                && this.center.getX() > rect.getUpperLeft().getX()
                && this.center.getY() > rect.getUpperLeft().getY()) {
            return 1;
        }
        if (this.center.getX() < rect.getUpperLeft().getX() + rect.getWidth()
        && this.center.getX() > rect.getUpperLeft().getX()
                && this.center.getY() + this.r > rect.getUpperLeft().getY()) {
            return 2;
        }
        return 0;
    }
    /**adding the ball to the sprite collection.
     * giving the ball reference to the env
     * @param g the game */
    public void addToGame(GameLevel g) {
        this.env = g.getEnv();
        g.addSprite(this);
    }
    /**removing the ball from the sprite collection.
     * @param g the game */
    public void removeFromGame(GameLevel g) {
        g.removeSprite(this);
    }
}
