

import java.awt.Color;
import biuoop.KeyboardSensor;
import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class GameLevel implements Animation {
    //the members:
    private SpriteCollection sprites;
    private GameEnvironment env;
    private Paddle paddle;
    private Counter blockRemaine;
    private Counter points;
    private Counter livesInd;
    private AnimationRunner runner;
    private boolean stop;
    private biuoop.KeyboardSensor keyboard;
    private LevelInformation data;
    private boolean sign;
    private boolean start;
    /** the constructor.
     * @param data the game levels
     * @param ar the animation runner
     * @param key the keyboard sensor
     * @param p the points counter
     * @param l the live counter*/
    public GameLevel(LevelInformation data, AnimationRunner ar, biuoop.KeyboardSensor key
            , Counter p, Counter l) {
        this.data = data;
        this.env = new GameEnvironment();
        this.sprites = new SpriteCollection();
        this.blockRemaine = new Counter();
        this.points = p;
        this.livesInd = l;
        this.runner = ar;
        this.keyboard = key;
        this.stop = false;
        this.sign = false;
        this.start = true;
    }
    /**add a collidable to the collection.
     *@param c the collidable.*/
    public void addCollidable(Collidable c) {
        env.addCollidable(c);
    }
    /**add a sprite to the collection.
     *@param s the sprite.*/
    public void addSprite(Sprite s) {
        sprites.addSprite(s);
    }
    /**remove the collidable from the collection.
     *@param c the collidable.*/
    public void removeCollidable(Collidable c) {
        env.removeCollidalbe(c);
    }
    /**remove the Sprite from the collection.
     *@param s the Sprite.*/
    public void removeSprite(Sprite s) {
        sprites.removeSprite(s);
    }
    /** a method to get the environment of the game.
     * @return the env*/
    public GameEnvironment getEnv() {
        return this.env;
    }
    /** stopping the animation runner.
     * @return the boolean to stop*/
    public boolean shouldStop() {
        return this.stop;
    }
    /** getting the data.
     * @return the data*/
    public LevelInformation getData() {
        return this.data;
    }
    /**Initializing the game.
     * creating the blocks the ball and the paddle
     *adding all of them to the game
     *creating the listeners and each to the blocks*/
    public void initialize() {
        //creating background and boarders
        Sprite s = data.getBackground();
        s.addToGame(this);
        Rectangle rect1 = new Rectangle(new Point(0, 0), 800, 30);
        Rectangle rect2 = new Rectangle(new Point(0, 30), 20, 680);
        Rectangle rect3 = new Rectangle(new Point(780, 30), 20, 680);
        Block block1 = new Block(rect1, Color.gray);
        Block block2 = new Block(rect2, Color.gray);
        Block block3 = new Block(rect3, Color.gray);
        block1.addToGame(this);
        block2.addToGame(this);
        block3.addToGame(this);
        Rectangle rect4 = new Rectangle(new Point(0, 590), 800, 20);
        Block block4 = new Block(rect4, Color.GRAY);
        block4.addToGame(this);

        // creating the indicators
        LevelIndicator level = new LevelIndicator(this);
        level.addToGame(this);
        ScoreIndicator scoreind = new ScoreIndicator(this.points);
        scoreind.addToGame(this);
        LivesIndicator lives = new LivesIndicator(this.livesInd);
        lives.addToGame(this);
        ScoreTrackingListener scorelistener = new ScoreTrackingListener(this.points);
        BlockRemover listener1 = new BlockRemover(this, this.blockRemaine);
        BallRemover listner2 = new BallRemover(this);
        block4.addHitListener(listner2);
        block1.addHitListener(listner2);
        block2.addHitListener(listner2);
        block3.addHitListener(listner2);


        // adding to each block a listeners.
        // increasing the blocks counter.
        for (int i = 0; i < data.blocks().size(); i++) {
            this.blockRemaine.increase(1);
            Block block = data.blocks().get(i);
            block.addToGame(this);
            block.addHitListener(listener1);
            block.addHitListener(scorelistener);
            block.addHitListener(listner2);
        }

    }
    /** doing one frame.
     * @param d the drawSurface
     * @param dt the speed by time*/
    public void doOneFrame(DrawSurface d, double dt) {
        //if you lose
        if (this.livesInd.getValue() == 0 && !sign) {
            this.sign = true;
            this.runner.run(new KeyPressStoppableAnimation(this.keyboard, KeyboardSensor.SPACE_KEY,
                    new EndScreen(this.keyboard, this.points, 0)));
            this.stop = true;
        }
        // if the level ended
        if (this.blockRemaine.getValue() == 0) {
            this.points.increase(100);
            this.stop = true;
        }
     
        // stoping the game with p
        if (this.keyboard.isPressed("p")) {
            this.runner.run(
                    new KeyPressStoppableAnimation(this.keyboard
                            , biuoop.KeyboardSensor.SPACE_KEY, new PauseScreen()));
        }
        if (!this.sign) {
            this.sprites.drawAllOn(d);
            this.sprites.notifyAllTimePassed(dt);
        }

     }
    /**running one turn of the game.
     *creating the paddle and the balls.*/
    public void playOneTurn() {
        Rectangle pad = new Rectangle(new Point((800 - data.paddleWidth()) / 2, 570), data.paddleWidth(), 20);
        this.paddle = new Paddle(pad, data.paddleSpeed());
        this.paddle.addToGame(this);
        this.paddle.setKeyboard(keyboard);
      
        // countdown before turn starts.
        if (this.livesInd.getValue() > 0) {
            this.runner.run(new CountdownAnimation((double) 3, this.sprites));
        }
        if (this.start) {
            this.start = false;
            this.runner.run(this);
        }
    }
    /** get the number of blocks remain.
     * @return the number of blocks*/
    public Counter getRemainBlocks() {
        return this.blockRemaine;
    }
   
}
