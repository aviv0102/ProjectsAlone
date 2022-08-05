import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class Green3 implements LevelInformation {
    //the members:
    private String name;
    private int numberOfBalls;
    private int paddleSpeed;
    private int paddleWidth;
    private List<Block> blocks;
    private List<Velocity> initialBallVelocities;

    /** the constructor.*/
    public Green3() {
        name = "Green 3";
        this.numberOfBalls = 4;
        this.paddleWidth = 100;
      this.paddleSpeed = 10 * 60;

    }
    /** get the background of the level.
     * @return the background*/
    public Sprite getBackground() {
        return new Green3Back();
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
         this.initialBallVelocities.add(new Velocity(60 * (1 + i), -60 * 5));
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
        int life = 2;
        for (int i = 0; i < 40; i++) {
            if (i == 10) {
                color = Color.red;
                h += 30;
                j = 0;
                life = 1;
            }
            if (i == 19) {
                color = Color.yellow;
                h += 30;
                j = 0;
            }
            if (i == 27) {
                color = Color.blue;
                h += 30;
                j = 0;
            }
            if (i == 34) {
                color = Color.white;
                h += 30;
                j = 0;
            }
            Rectangle rect = new Rectangle(new Point(740 - j, 100 + h), 40, 30);
            j += 40;
            Block b = new Block(rect, color, life);
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
