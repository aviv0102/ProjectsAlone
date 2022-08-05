
import java.awt.Color;
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class Paddle implements Sprite, Collidable {
    //members:
    private biuoop.KeyboardSensor keyboard;
    private Rectangle rect;
    private double speed;
    /**the constructor creates a paddle.
     * @param rect the rectangle
     * @param speed the speed*/
    public Paddle(Rectangle rect, int speed) {
        this.rect = rect;
        this.speed = speed;
    }
    /**get the keyboard from outside.
     * @param key the keyboard*/
    public void setKeyboard(biuoop.KeyboardSensor key) {
        this.keyboard = key;
    }
    /** move the paddle left.
     * @param dt the speed by time*/
    public void moveLeft(double dt) {
        Point p = null;
        if (rect.getUpperLeft().getX() > 21) {
            p = new Point(rect.getUpperLeft().getX() - dt * speed, rect.getUpperLeft().getY());
            this.rect = new Rectangle(p, rect.getWidth(), rect.getHeight());
        }
    }
    /** move the paddle right.
     * @param dt the speed by time*/
    public void moveRight(double dt) {
        Point p = null;
        if (rect.getUpperLeft().getX() + rect.getWidth() < 778) {
            p = new Point(rect.getUpperLeft().getX() + dt * speed, rect.getUpperLeft().getY());
            this.rect = new Rectangle(p, rect.getWidth(), rect.getHeight());
        }
    }
    /** the timepassed method.
     * what will happen in the next move
     * @param dt ...*/
    public void timePassed(double dt) {
        if (keyboard.isPressed(biuoop.KeyboardSensor.LEFT_KEY)) {
            this.moveLeft(dt);
        }
        if (keyboard.isPressed(biuoop.KeyboardSensor.RIGHT_KEY)) {
            this.moveRight(dt);
        }
    }
    /** draw the paddle to the screen.
     * @param surface the gui surface*/
    public void drawOn(DrawSurface surface) {
        surface.setColor(Color.yellow);
        surface.fillRectangle((int) rect.getUpperLeft().getX()
                , (int) rect.getUpperLeft().getY(), (int) rect.getWidth(), (int) rect.getHeight());
        surface.setColor(Color.black);
        surface.drawRectangle((int) rect.getUpperLeft().getX()
                , (int) rect.getUpperLeft().getY(), (int) rect.getWidth(), (int) rect.getHeight());
    }
    /** get the rectangle of this paddle.
     * @return the rect*/
    public Rectangle getCollisionRectangle() {
        return this.rect;
    }
    /**change the velocity of the ball.
     * depends on which part of the paddle it hits.
     * works by angles.
     * @param collisionP the impact point
     * @param currentV the velocity of the ball in the moment he entered
     * @param hitter the balls that hit the paddle
     * @return the new v */
    public Velocity hit(Ball hitter, Point collisionP, Velocity currentV) {
        double speedOfball = Math.sqrt(currentV.getDX() * currentV.getDX()
                + currentV.getDY() * currentV.getDY());
        double px = collisionP.getX();
        double piece = this.rect.getWidth() / 9;
        double x = this.rect.getUpperLeft().getX();

        if (collisionP.getY() == rect.getUpperLeft().getY()
                || collisionP.getY() == rect.getUpperLeft().getY() + rect.getHeight()) {
            if (px >= x && px <= x + piece) {
                return Velocity.fromAngleAndSpeed(300, speedOfball);
            } else if (px > x + piece && px <= x + 2 * piece) {
                return Velocity.fromAngleAndSpeed(315, speedOfball);
            } else if (px > x + 2 * piece && px <= x + 3 * piece) {
                return Velocity.fromAngleAndSpeed(330, speedOfball);
            } else if (px > x + 3 * piece && px <= x + 4 * piece) {
                return Velocity.fromAngleAndSpeed(345, speedOfball);
            } else if (px > x + 4 * piece && px <= x + 5 * piece) {
                return Velocity.fromAngleAndSpeed(360, speedOfball);
            } else if (px > x + 5 * piece && px <= x + 6 * piece) {
                return Velocity.fromAngleAndSpeed(15, speedOfball);
            } else if (px > x + 6 * piece && px <= x + 7 * piece) {
                return Velocity.fromAngleAndSpeed(30, speedOfball);
            } else if (px > x + 7 * piece && px <= x + 8 * piece) {
                return Velocity.fromAngleAndSpeed(45, speedOfball);
            } else if (px > x + 8 * piece) {
                return Velocity.fromAngleAndSpeed(60, speedOfball);
            }
        }
        return new Velocity(-currentV.getDX(), currentV.getDY());

    }
    /** add the paddle to the game.
     * @param g the game*/
    public void addToGame(GameLevel g) {
        g.addCollidable(this);
        g.addSprite(this);
    }
    /** remove the paddle from the game.
     * @param g the game*/
    public void removeFromGame(GameLevel g) {
        g.removeSprite(this);
        g.removeCollidable(this);
    }
}
