
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public interface LevelInformation {
    /** get the number of balls.
     * @return the number of balls*/
    int numberOfBalls();

    /** Initialize the balls velocity.
     * @return the list of velocity's*/
    List<Velocity> initialBallVelocities();
    /** get the paddle speed.
     * @return the paddleSpeed*/
    int paddleSpeed();
    /** get the paddle width.
     * @return the paddleWidth*/
    int paddleWidth();

    /** get level name.
     * @return the level name*/
    String levelName();

    /** get the background of the level.
     * @return the background*/
    Sprite getBackground();

    /** Initialize this level blocks.
     * @return the list of blocks*/
    List<Block> blocks();

    /** get the number of blocks need to remove.
     * @return the number of blocks need to remove*/
    int numberOfBlocksToRemove();
}