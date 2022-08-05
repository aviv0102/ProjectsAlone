
import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class FinalFour implements LevelInformation {
    // the members:
    private String name;
    private int numberOfBalls;
    private int paddleSpeed;
    private int paddleWidth;
    private List<Block> blocks;
    private List<Velocity> initialBallVelocities;
    /** the constructor.*/
    public FinalFour() {
        name = "Final Four";
        this.numberOfBalls = 4;
        this.paddleWidth = 100;
        this.paddleSpeed = 10*60;

    }
    /** get the background of the level.
     * @return the background*/
    public Sprite getBackground() {
        return new FinalFourBack();
    }
    /** get the paddle width.
     * @return the paddleWidth*/
    public int paddleWidth() {
        return this.paddleWidth;
    }
    /** get the paddle speed.
     * @return the paddleSpeed*/
    public int paddleSpeed() {
        return this.paddleSpeed;
    }
    /** Initialize the balls velocity.
     * @return the list of velocity's*/
    public List<Velocity> initialBallVelocities() {
        this.initialBallVelocities = new ArrayList<Velocity>();
        for (int i = 0; i < this.numberOfBalls; i++) {
            this.initialBallVelocities.add(new Velocity(60*(1 + i), -5*60));
        }
        return this.initialBallVelocities;
    }
    /** get the number of balls.
     * @return the number of balls*/
    public int numberOfBalls() {
        return this.numberOfBalls;
    }
    /** get level name.
     * @return the level name*/
    public String levelName() {
        return this.name;
    }
    /** Initialize this level blocks.
     * @return the list of blocks*/
    public List<Block> blocks() {
        this.blocks = new ArrayList<Block>();
        int j = 0;
        int h = 0;
        Color color = Color.gray;
        for (int i = 0; i < 105; i++) {
            if (i == 15) {
                color = Color.red;
                h += 30;
                j = 0;
            }
            if (i == 30) {
                color = Color.yellow;
                h += 30;
                j = 0;
            }
            if (i == 45) {
                color = Color.green;
                h += 30;
                j = 0;
            }
            if (i == 60) {
                color = Color.white;
                h += 30;
                j = 0;
            }
            if (i == 75) {
                color = Color.pink;
                h += 30;
                j = 0;
            }
            if (i == 90) {
                color = Color.blue;
                h += 30;
                j = 0;
            }
            Rectangle rect = new Rectangle(new Point(730 - j, 80 + h), 50, 30);
            j += 50;
            Block b = new Block(rect, color);
            this.blocks.add(b);
        }

        return this.blocks;
    }
    /** get the number of blocks need to remove.
     * @return the number of blocks need to remove*/
    public int numberOfBlocksToRemove() {
        return this.blocks.size();
    }

}
