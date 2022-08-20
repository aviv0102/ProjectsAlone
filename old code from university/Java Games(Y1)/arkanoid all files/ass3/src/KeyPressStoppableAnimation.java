
import biuoop.DrawSurface;
import biuoop.KeyboardSensor;
/**
* @author Aviv Shisman 206558157
*/
public class KeyPressStoppableAnimation implements Animation {
    //members:
    private Animation animation;
    private String key;
    private KeyboardSensor sensor;
    private boolean stop;
    /**the constructor.
     * @param sensor the keyboard
     * @param key the key for stopping
     * @param animation the animation we will stop
     */
    public KeyPressStoppableAnimation(KeyboardSensor sensor, String key, Animation animation) {
        this.animation = animation;
        this.key = key;
        this.sensor = sensor;
        this.stop = false;

    }
    /**when animation should stop we will stop it here.
     * @param d the surface.
     * @param dt the speed by time.
     */
    public void doOneFrame(DrawSurface d, double dt) {
        this.animation.doOneFrame(d, dt);
        if (this.sensor.isPressed(key)) {
            this.stop = true;
        }
    }
    /**telling the animation runner when to stop.
     * @return true or false
     */
    public boolean shouldStop() {
        if (this.stop) {
            return animation.shouldStop();
        }
        return false;
    }


}
