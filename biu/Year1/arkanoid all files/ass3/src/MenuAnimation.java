
import java.awt.Color;

import biuoop.DrawSurface;
import biuoop.KeyboardSensor;
import java.util.List;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
* @param <T> the task currently "unknown" type
*/
public class MenuAnimation<T> implements Menu<T> {
    //members:
    private boolean stop;
    private KeyboardSensor keyboard;
    private String name;
    private List<T> tasks;
    private List<String> nameOfTask;
    private List<String> keys;
    private T status;
    private SubMenu sub;
    private AnimationRunner ar;
    /**the constructor.
     * @param name the name of the menu
     * @param ks the keyboard
     */
    public MenuAnimation(String name, KeyboardSensor ks) {
        this.keyboard = ks;
        this.name = name;
        this.stop = false;
        this.tasks = new ArrayList<T>();
        this.nameOfTask = new ArrayList<String>();
        this.keys = new ArrayList<String>();
    }
    /** drawing frame of menu to screen.
     * @param dt the speed by time
     * @param d the surface
     */
    public void doOneFrame(DrawSurface d, double dt) {
        d.setColor(Color.GRAY);
        d.drawRectangle(0, 0, 800, 800);
        d.setColor(Color.RED);
        d.drawText(100, 50, this.name, 28);
        d.setColor(Color.green);
        for (int i = 0; i < this.keys.size(); i++) {
            d.drawText(100, 100 + 32 * (i), this.nameOfTask.get(i), 25);
            if (this.keyboard.isPressed(this.keys.get(i))) {
                this.status = this.tasks.get(i);
                // if the key is s run sub menu
                if (this.keys.get(i) == "s") {
                    this.ar.run(sub);
                    this.stop = true;
                    return;
                }
                this.stop = true;
                return;
            }

        }
    }
       /**adding a selection to the menu.
        * @param key the key for selecting
        * @param name1 the message we get in the screen
        * @param task the task to execute
        */
    public void addSelection(String key, String name1, T task) {
        this.keys.add(key);
        this.nameOfTask.add(name1);
        this.tasks.add(task);
    }
       /** get the current task.
        * @return returns the task
        */
    public T getStatus() {
        return this.status;
    }
    /**setting the sub menu.
     * @param s the sub menu
     * @param runner animation runner for running the sub menu
     */
    public void addSubMenu(SubMenu s, AnimationRunner runner) {
        this.sub = s;
        this.ar = runner;
    }


    /**
     * telling the animation runner to stop.
     * @return to stop or not
     */
    public boolean shouldStop() {
        return this.stop;
    }

}
