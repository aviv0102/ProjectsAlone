import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class SunnyDay implements LevelInformation {
    //members:
    private String name;
    private int numberOfBalls;
    private int paddleSpeed;
    private int paddleWidth;
    private List<Block> blocks;
    private List<Velocity> initialBallVelocities;
    /** the constructor. */
    public SunnyDay() {
        name = "SunnyDay";
        this.numberOfBalls = 10;
        this.paddleWidth = 400;
        this.paddleSpeed = 4*60;

    }
    /** get the background of the level.
     * @return the background*/
    public Sprite getBackground() {
        return new SunnyDayBack();
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
		for (int i = 1; i <= this.numberOfBalls * 5; i += 5) {
			Velocity v = new Velocity(Velocity.fromAngleAndSpeed(i, 5));
			this.initialBallVelocities.add(new Velocity(v.getDX() * 60, v.getDY() * 60));
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
        Color color = Color.red;
        for (int i = 0; i < 19; i++) {
            if (i == 3) {
                color = Color.red;
            }
            if (i == 6) {
                color = Color.yellow;
            }
            if (i == 9) {
                color = Color.green;
            }
            if (i == 12) {
                color = Color.BLUE;
            }
            if (i == 15) {
                color = Color.pink;
            }
            if (i == 17) {
                color = Color.blue;
            }
            Rectangle rect = new Rectangle(new Point(20 + j, 250), 40, 20);
            j += 40;
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
