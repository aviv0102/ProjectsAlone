
import java.util.ArrayList;
import java.util.List;
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class SpriteCollection {
    // members:
    private List<Sprite> arr;
    /** the constructor build an array of sprite's.*/
    public SpriteCollection() {
        this.arr = new ArrayList<Sprite>();
    }
    /** an method to add sprite's.
     * @param s the sprite we add*/
    public void addSprite(Sprite s) {
        arr.add(s);
    }
    /** an method to remove sprite's.
     * @param s the sprite we remove*/
    public void removeSprite(Sprite s) {
        arr.remove(s);
    }
    /** a method to activate time passed on all.
     * the sprite's
     * @param dt the speed by time*/
    public void notifyAllTimePassed(double dt) {
        for (int i = 0; i < arr.size(); i++) {
            arr.get(i).timePassed(dt);
        }
    }
    /** a method to draw all sprite's.
     * @param d the surface*/
    public void drawAllOn(DrawSurface d) {
        for (int i = 0; i < arr.size(); i++) {
            arr.get(i).drawOn(d);
        }
    }
}