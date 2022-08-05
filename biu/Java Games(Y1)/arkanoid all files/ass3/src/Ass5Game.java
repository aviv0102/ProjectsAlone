
import biuoop.KeyboardSensor;
import biuoop.GUI;
import java.util.List;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
*/
public class Ass5Game {
    /** the main.
     * running all the levels
     * @param args the arguments for the main*/
    public static void main(String[] args) {
        List<LevelInformation> list = new ArrayList<LevelInformation>();
        int[] myArr = new int[args.length];
        for (int i = 0; i < args.length; i++) {
            try {
                myArr[i] = Integer.parseInt(args[i]);
            } catch (Exception e) {
                System.out.println("NOT A NUMBER");
            }
        }
        for (int i = 0; i < args.length; i++) {
            if (myArr[i] == 1) {
                list.add(new DirectHit());
            }
            if (myArr[i] == 2) {
                list.add(new SunnyDay());
            }
            if (myArr[i] == 3) {
                list.add(new Green3());
            }
            if (myArr[i] == 4) {
                list.add(new FinalFour());
            }
        }
        if (list.size() <= 0) {
            list.add(new DirectHit());
            list.add(new SunnyDay());
            list.add(new Green3());
            list.add(new FinalFour());

        }
        GUI gui = new GUI("game", 800, 600);
        AnimationRunner ar = new AnimationRunner(gui);
        KeyboardSensor key = gui.getKeyboardSensor();
        
        

		while (true) {
			File highscore=new File("highscores");
	    	HighScoresTable table=new HighScoresTable(10);
	    	if(highscore.exists()){
	    		try{
					table.load(highscore);
				} catch (IOException e) {
					System.out.println(" Something went wrong while loading!");
				}
			}
			HighScoresAnimation highscoreAnimation = new HighScoresAnimation(table, "e", key);
	        GameFlow game = new GameFlow(ar, key, gui);
			Menu<Task<Void>> menu = new MenuAnimation<Task<Void>>("Welcome to Arkanoid", key);
			menu.addSelection("h", "Press H for ScoreTable", new ShowHiScoresTask(ar, highscoreAnimation, key));
			menu.addSelection("s", "Press S for Game", new PlayTurnTask(list, game));
			menu.addSelection("q", "Press Q for Quit", new QuitTask());
			ar.run(menu);
			Task<Void> task = menu.getStatus();
			task.run();
		}


	}
}
