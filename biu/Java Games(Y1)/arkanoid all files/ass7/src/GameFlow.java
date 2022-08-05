
import java.io.IOException;
import java.io.File;
import java.util.List;
import biuoop.DialogManager;
import biuoop.GUI;
import biuoop.KeyboardSensor;
/**
* @author Aviv Shisman 206558157
*/
public class GameFlow {
    //the members:
    private Counter points;
    private Counter lives;
    private GUI gui;
    private AnimationRunner ar;
    private KeyboardSensor ks;
    /** the constructor.
     * @param ar animation runner
     * @param ks keyboard sensor
     * @param gui the gui*/
    public GameFlow(AnimationRunner ar, KeyboardSensor ks, GUI gui) {
        this.points = new Counter();
        this.lives = new Counter();
        lives.increase(3);
        this.ar = ar;
        this.ks = ks;
        this.gui = gui;
    }
    /**running the game levels.
     * @param levels the list of levels we run */
    public void runLevels(List<LevelInformation> levels) {
        for (LevelInformation levelInfo : levels) {
            GameLevel level = new GameLevel(levelInfo, this.ar, this.ks, this.points
            , this.lives);
            level.initialize();
            while (this.lives.getValue() > 0 && level.getRemainBlocks().getValue() > 0) {
                level.playOneTurn();
            }
            if (this.lives.getValue() == 0) {
                break;
            }
        }
        if (this.lives.getValue() > 0) {
            this.ar.run(new KeyPressStoppableAnimation(this.ks, KeyboardSensor.SPACE_KEY,
                    new EndScreen(this.ks, this.points, 1)));
        }
        File highscore = new File("highscores");
        HighScoresTable table = new HighScoresTable(10);
        if (highscore.exists()) {
            try {
                table.load(highscore);
            } catch (IOException e) {
                System.out.println(" Something went wrong while loading!");
            }
        }
        DialogManager dialog = gui.getDialogManager();
        String name = dialog.showQuestionDialog("Name", "What is your name?", "");
        table.add(new ScoreInfo(name, this.points.getValue()));
        try {
            table.save(highscore);
        } catch (IOException e) {
            System.out.println(" Something went wrong while saving!");
        }
        this.ar.run(new KeyPressStoppableAnimation(this.ks, biuoop.KeyboardSensor.SPACE_KEY,
                new HighScoresAnimation(table)));
        return;
    }

}
