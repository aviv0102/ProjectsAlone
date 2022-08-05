import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class GenericLevel implements LevelInformation {
    //the members:
    private String name;
    private int numberOfBalls;
    private int paddleSpeed;
    private int paddleWidth;
    private List<Block> blocks;
    private List<Velocity> initialBallVelocities;
    private Sprite back;
    private int blockToClear;
    /** the constructor.*/
    public GenericLevel() {
        this.initialBallVelocities = new java.util.ArrayList<Velocity>();
        this.blocks = new java.util.ArrayList<Block>();
        this.numberOfBalls = 0;
    }
    /**set the number of blocks. /
     * @param n the number */
    public void setBlocksToClear(int n) {
        this.blockToClear = n;
    }
    /**set the speed of paddle. /
     * @param s the number */
    public void setSpeed(int s) {
        this.paddleSpeed = s;
    }
    /**set the width of paddle.
     * @param w the width*/
    public void setWidth(int w) {
        this.paddleWidth = w;
    }
    /**add a velocity.
     * @param v the new v.*/
    public void addVelocity(Velocity v) {
        this.initialBallVelocities.add(v);
        this.numberOfBalls++;
    }
    /**set the back.
     * @param s the background.
     */
    public void setBack(Sprite s) {
        this.back = s;
    }
    /** get the background.
     * @return the back.
     */
    public Sprite getBackground() {
        return this.back;
    }
    /**add a block.
     * @param b the block.
     */
    public void addBlock(Block b) {
        blocks.add(b);
    }
    /** set the level name.
     * @param s the string.
     */
    public void setName(String s) {
        this.name = s;
    }
    /** get the paddle width.
     * @return the width*/
    public int paddleWidth() {
        return this.paddleWidth;
    }
    /**get the paddle speed.
     * @return the paddle speed.
     */
    public int paddleSpeed() {
        return this.paddleSpeed;
    }
    /** get the velocity's.
     * @return the list of them.*/
    public List<Velocity> initialBallVelocities() {
        return this.initialBallVelocities;
    }
    /** get the name of the level.
     * @return the name.
     */
    public String levelName() {
        return this.name;
    }
    /** get the number of balls.
     * @return the number of them.
     */
    public int numberOfBalls() {
        return this.numberOfBalls;
    }
    /**get all the blocks.
     * @return the number of blocks.
     */
    public List<Block> blocks() {
        return this.blocks;
    }
    /**the number of blocks to remove.
     * @return the number of them.
     */
    public int numberOfBlocksToRemove() {
        return this.blockToClear;
    }
}
