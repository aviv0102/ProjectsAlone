
import java.awt.Color;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.Map;


import biuoop.DrawSurface;
import java.util.ArrayList;

/**
 * @author Aviv Shisman 206558157
 */
public class Block implements Collidable, Sprite, HitNotifier {
    // members:
    private Rectangle rect;
    private java.awt.Color color;
    private int life;
    private List<HitListener> hitListeners;
    private String stroke;
    private List<Object> fillers;
    /** @param b the block we want to duplicate.
     * the constructor*/
    public Block(Block b) {
        this.rect = new Rectangle(b.getCollisionRectangle());
        this.hitListeners = new ArrayList<HitListener>();
        this.life = b.getLife();
        this.fillers = new ArrayList<Object>(b.getfillerList());
        this.stroke = b.getStoke();
    }
    /** create a blank block we will later change.*/
    public Block() {
        this.fillers = new ArrayList<Object>();
        this.hitListeners = new ArrayList<HitListener>();
        this.rect = new Rectangle(new Point(1, 1), 1, 1);
        this.life = 1;
    }

    /**
     * the constructor creating a block.
     * @param rect
     *            the rectangle shape of block
     */
    public Block(Rectangle rect) {
        this.hitListeners = new ArrayList<HitListener>();
        this.rect = rect;
        this.color = Color.BLACK;
        this.life = 1;
    }

    /**
     * the constructor creating a block.
     * @param rect
     *            the rectangle shape of block
     * @param color
     *            the color of the block
     */
    public Block(Rectangle rect, Color color) {
        this.hitListeners = new ArrayList<HitListener>();
        this.rect = rect;
        this.color = color;
        this.life = 1;
    }

    /**
     * the constructor creating a block.
     * @param rect
     *       the rectangle shape of block
     * @param color
     *            the color of the block
     * @param life
     *            the life of the block
     */
    public Block(Rectangle rect, Color color, int life) {
        this.hitListeners = new ArrayList<HitListener>();
        this.rect = rect;
        this.color = color;
        this.life = life;
    }

    /**
     * get the shape of the block the rectangle.
     * @return the rectangle
     */
    public Rectangle getCollisionRectangle() {
        return this.rect;
    }

    /**
     * after the ball hits a block givinig him a new velocity.
     * @param collisionP the collision point
     * @param currentV the current velocity
     * @param hitter the ball that hits
     * @return the new velocity*/
    public Velocity hit(Ball hitter, Point collisionP, Velocity currentV) {
        if (life > 0) {
            this.life--;
        }
        this.notifyHit(hitter);
        double dx = currentV.getDX();
        double dy = currentV.getDY();
        int flag = 0;
        if (Math.abs(collisionP.getY() - rect.getUpperLeft().getY()) < 0.0001
                || Math.abs(collisionP.getY()
                        - (rect.getUpperLeft().getY() + rect.getHeight())) < 0.0001) {
            dy = -currentV.getDY();
            flag++;
        }
        if (Math.abs(collisionP.getX() - rect.getUpperLeft().getX()) < 0.0001
                || Math.abs(collisionP.getX()
                        - (rect.getUpperLeft().getX() + rect.getWidth())) < 0.0001) {
            dx = -currentV.getDX();
            flag++;
        }
        if (flag == 2) {
            return new Velocity(-currentV.getDX(), -currentV.getDY());
        }

        return new Velocity(dx, dy);
    }

    /**
     * the method for drawing a block.
     * @param surface the gui surface.
     */
    public void drawOn(DrawSurface surface) {
        // drawing the rectangle
        try {
            if (!this.fillers.isEmpty()) {
                if (this.fillers.get(this.life - 1) instanceof Image) {
                    surface.drawImage((int) this.rect.getUpperLeft().getX()
                            , (int) this.rect.getUpperLeft().getY(),
                            (BufferedImage) this.fillers.get(this.life - 1));
                }
            }
        } catch (Exception e) {
            System.out.println("");
        }
        try {
            if (!this.fillers.isEmpty()) {
                if (this.fillers.get(this.life - 1) instanceof Color) {
                    surface.setColor((Color) this.fillers.get(this.life - 1));
                    surface.fillRectangle((int) rect.getUpperLeft().getX()
                            , (int) rect.getUpperLeft().getY(),
                            (int) rect.getWidth(), (int) rect.getHeight());
                    surface.setColor(Color.black);
                    surface.drawRectangle((int) rect.getUpperLeft().getX()
                            , (int) rect.getUpperLeft().getY(),
                            (int) rect.getWidth(), (int) rect.getHeight());
                }
            }
        } catch (Exception e) {
            System.out.println("");
        }
        if (this.color != null) {
            surface.setColor(this.color);
            surface.fillRectangle((int) rect.getUpperLeft().getX(), (int) rect.getUpperLeft().getY(),
                    (int) rect.getWidth(), (int) rect.getHeight());
            surface.setColor(Color.black);
            surface.drawRectangle((int) rect.getUpperLeft().getX(), (int) rect.getUpperLeft().getY(),
                    (int) rect.getWidth(), (int) rect.getHeight());
        }
    }

    /** calling timepassed method that does nothing in this case.
     * @param dt the speed by time */
    public void timePassed(double dt) {

    }

    /**
     * adding the block to the game.
     * @param g the game
     */
    public void addToGame(GameLevel g) {
        g.addCollidable(this);
        g.addSprite(this);
    }

    /**
     * removing the block from the game.
     * @param gameLevel the game
     */
    public void removeFromGame(GameLevel gameLevel) {
        gameLevel.removeCollidable(this);
        gameLevel.removeSprite(this);
    }

    /**
     * adding hit listener.
     * @param hl the hit listener
     */
    public void addHitListener(HitListener hl) {
        this.hitListeners.add(hl);
    }

    /**
     * removing hit listener.
     * @param hl the hit listener
     */
    public void removeHitListener(HitListener hl) {
        this.hitListeners.remove(hl);
    }

    /**
     * getting the life of a block.
     * @return the life of the block
     */
    public int getLife() {
        return this.life;
    }

    /**
     * notify all the hit listeners on a hit.
     * @param hitter the ball
     */
    private void notifyHit(Ball hitter) {
        List<HitListener> listeners = new ArrayList<HitListener>(this.hitListeners);
        for (HitListener hl : listeners) {
            hl.hitEvent(this, hitter);
        }
    }
    /** setting the width.
     * @param w the width*/
    public void setWidth(int w) {
        this.rect = new Rectangle(this.rect.getUpperLeft(), w, this.rect.getHeight());
    }
    /** setting the height.
     * @param h the height*/
    public void setHeight(int h) {
        this.rect = new Rectangle(this.rect.getUpperLeft(), this.rect.getWidth(), h);
    }
    /** setting the point.
     * @param x the x
     * @param y the y*/
    public void setPoint(int x, int y) {
        this.rect = new Rectangle(new Point(x, y), this.rect.getWidth(), this.rect.getHeight());
    }
    /** setting the lives.
     * @param l the lives*/
    public void setLives(int l) {
        this.life = l;
    }
    /** setting the stroke.
     * @param s the stroke*/
    public void setStroke(String s) {
        this.stroke = s;
    }
    /**setting the fillers.
     * @param fill the fillMap we use*/
    public void setFillMap(java.util.HashMap<Integer, String> fill) {
        for (int i = 0; i < fill.size(); i++) {
            for (Map.Entry<Integer, String> entry : fill.entrySet()) {
                if (entry.getKey().intValue() == i + 1) {
                    String value = entry.getValue();
                    if ((value.startsWith("color(RGB(")) && (value.endsWith("))"))) {
                        String param = extractParam(value, "color(RGB(", "))");
                        String[] parts = param.split(",");
                        int r = Integer.parseInt(parts[0]);
                        int g = Integer.parseInt(parts[1]);
                        int b = Integer.parseInt(parts[2]);
                        String s = String.format("#%02x%02x%02x", r, g, b);
                        this.fillers.add(java.awt.Color.decode(s));

                    } else if ((value.startsWith("color(")) && (value.endsWith(")"))) {
                        String param = extractParam(value, "color(", ")");
                        try {
                            java.lang.reflect.Field field = Color.class.getField(param);
                            Color col = (Color) field.get(null);
                            this.fillers.add(col);
                        } catch (NoSuchFieldException e) {
                            throw new RuntimeException("Unsupported color name: " + param);
                        } catch (IllegalAccessException e) {
                            throw new RuntimeException("Unsupported color name: " + param);
                        }
                    } else if ((value.startsWith("image(")) && (value.endsWith(")"))) {
                        String param = extractParam(value, "image(", ")");
                        java.io.InputStream is = null;
                        try {
                            is = ClassLoader.getSystemClassLoader()
                                    .getResourceAsStream(param);
                            if (is == null) {
                                is = ClassLoader.getSystemClassLoader()
                                        .getResourceAsStream("/" + param);
                            }
                            java.awt.image.
                            BufferedImage image = javax.imageio.ImageIO.read(is);

                            //img = ImageIO.read(new File(param));
                            this.fillers.add(image);
                        } catch (Exception e) {
                            throw new RuntimeException("Failed loading image: " + param, e);

                        }

                    }
                }
            }
        }

    }
    /** get the fillers.
     * @return the list of them
     */
    private List<Object> getfillerList() {
        return this.fillers;
    }
    /** get the stroke.
     * @return the stroke.
     */
    public String getStoke() {
        return this.stroke;
    }
    /** a method to extract from the string.
     * @param value the wanted value
     * @param pre the preix
     * @param post the postfix
     * @return new String
     */
    private static String extractParam(String value, String pre, String post) {
        return value.substring(pre.length(), value.length() - post.length());
    }
    /** get the hitListeners.
     * @return the list of them
     */
    public List<HitListener> getListeners() {
        return this.hitListeners;
    }

}
