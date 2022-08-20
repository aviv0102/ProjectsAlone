
import java.util.List;
import java.awt.Color;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
*/
public class DirectHit implements LevelInformation {
    // the members:
    private String name;
    private int numberOfBalls;
    private int paddleSpeed;
    private int paddleWidth;
    private List<Block> blocks;
    private List<Velocity> initialBallVelocities;
    /** the constructor.*/
    public DirectHit() {
        name = "Direct Hit";
        this.numberOfBalls = 1;
        this.paddleWidth = 100;
        this.paddleSpeed = 6*60;

    }
    /** get the background of the level.
     * @return the background*/
    public Sprite getBackground() {
        return new DirectHitBack();
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
            this.initialBallVelocities.add(new Velocity(0, -6*60));
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
        Rectangle rect = new Rectangle(new Point(380, 80), 40, 40);

        Block b = new Block(rect, Color.red);
        this.blocks.add(b);
        return this.blocks;
    }
    /** get the number of blocks need to remove.
     * @return the number of blocks need to remove*/
    public int numberOfBlocksToRemove() {
        return this.blocks.size();
    }
}
