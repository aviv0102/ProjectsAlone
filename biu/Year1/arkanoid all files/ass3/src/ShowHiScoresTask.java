import biuoop.KeyboardSensor;
/**
* @author Aviv Shisman 206558157
*/
public class ShowHiScoresTask implements Task<Void> {
    //members:
    private AnimationRunner ar;
    private Animation highScoresAnimation;
    private KeyboardSensor ks;

    /**the constructor.
     * @param runner the ar
     * @param highScoresAnimation the high score animation shows the scores.
     * @param k keyboard
     */
    public ShowHiScoresTask(AnimationRunner runner, Animation highScoresAnimation
            , KeyboardSensor k) {
        this.ar = runner;
        this.highScoresAnimation = highScoresAnimation;
        this.ks = k;
    }
    /** execute the run-running the highscore table animation.
     * @return void...
     */
    public Void run() {
        this.ar.run(new KeyPressStoppableAnimation(this.ks,
                KeyboardSensor.SPACE_KEY, this.highScoresAnimation));
        return null;
    }
}