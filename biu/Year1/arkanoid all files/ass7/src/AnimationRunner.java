
import biuoop.GUI;
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class AnimationRunner {
    //the members:
    private GUI gui;
    private int framesPerSecond;
    /** the constructor.
     * @param g the gui*/
    public AnimationRunner(GUI g) {
        this.gui = g;
        this.framesPerSecond = 60;
    }
    /** running the animation that it get.
    * @param animation the animation*/
    public void run(Animation animation) {
        double dt = (double) 1 / this.framesPerSecond;
        biuoop.Sleeper sleeper = new biuoop.Sleeper();
        int millisecondsPerFrame = 1000 / this.framesPerSecond;
        while (!animation.shouldStop()) {
            long startTime = System.currentTimeMillis(); // timing
            DrawSurface d = gui.getDrawSurface();

            animation.doOneFrame(d, dt);
            if (animation.shouldStop()) {
                return;
            }
            gui.show(d);
            long usedTime = System.currentTimeMillis() - startTime;
            long milliSecondLeftToSleep = millisecondsPerFrame - usedTime;
            if (milliSecondLeftToSleep > 0) {
                sleeper.sleepFor(milliSecondLeftToSleep);
            }
        }
    }
}
