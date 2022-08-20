import java.awt.Color;
import java.util.List;

import biuoop.DrawSurface;
import biuoop.KeyboardSensor;
/**
* @author Aviv Shisman 206558157
*/
public class SubMenu implements Animation {
    //the members:
    private boolean stop;
    private KeyboardSensor key;
    private String result;
    private List<String> keys;
    private List<String> messages;

    /** the constructor.
     * @param k the KeyboardSensor
     * @param keys the keys for stopping
     * @param messeges the messages of each option
     * @param result which character the player chose */
    public SubMenu(KeyboardSensor k, List<String> keys, String result, List<String> messeges) {
        this.stop = false;
        this.key = k;
        this.result = result;
        this.keys = keys;
        this.messages = messeges;
    }
    /**running the end screen.
    * @param d the drawSurface
    * @param dt ...*/
    public void doOneFrame(DrawSurface d, double dt) {
        d.setColor(Color.CYAN);
        for (int i = 0; i < this.messages.size(); i++) {
            d.drawText(200, 100 + i * 100, this.messages.get(i), 30);
        }
        for (int i = 0; i < this.keys.size(); i++) {
            if (this.key.isPressed(keys.get(i))) {
                result = keys.get(i);
                this.stop = true;
                return;
            }
        }
    }
    /** if the animation should stop stops it.
     * @return the answer */
    public boolean shouldStop() {
        return this.stop;
    }
    /**returns the string.
     * @return the result what option the player chose
     */
    public String result() {
        return this.result;
    }

}
