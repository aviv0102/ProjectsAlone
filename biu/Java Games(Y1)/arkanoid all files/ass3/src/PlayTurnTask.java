
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class PlayTurnTask implements Task<Void> {
    //memeber:
    private List<LevelInformation> levels;
    private GameFlow game;
    /**the constructor.
     * @param levels list of level...
     * @param g the game
     */
    public PlayTurnTask(List<LevelInformation> levels, GameFlow g) {
        this.levels = levels;
        this.game = g;
    }
    /** running the game.
     * @return void... */
    public Void run() {
        this.game.runLevels(levels);
        return null;
    }
    /**set the levels.
     * @param levelList the levels.
     */
    public void setLevel(List<LevelInformation> levelList) {
        this.levels = levelList;
    }
}
