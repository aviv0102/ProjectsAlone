
import biuoop.KeyboardSensor;

import biuoop.GUI;
import java.util.List;
import java.util.Map;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/**
 * @author Aviv Shisman 206558157
 */
public class Ass6Game {
    /**
     * the main. running all the levels
     * @param args the arguments for the main
     */
    public static void main(String[] args) {
        GUI gui = new GUI("game", 800, 600);
        AnimationRunner ar = new AnimationRunner(gui);
        KeyboardSensor keyboard = gui.getKeyboardSensor();
        AnimationRunner ar2 = new AnimationRunner(gui);
        List<String> messages = new ArrayList<String>();
        List<String> keys = new ArrayList<String>();
        Map<String, String> map = new java.util.HashMap<String, String>();
        BufferedReader bf = null;

        String filename = null;
        if (args.length > 0) {
            filename = args[0];
            filename = filename.trim();
        }
        java.io.Reader reader = null;
        try {
            if (filename == null) {
                reader = new java.io.InputStreamReader(
                        ClassLoader.getSystemClassLoader().
                        getResourceAsStream("level_sets.txt"));
            } else {
                reader = new java.io.InputStreamReader(
                        ClassLoader.getSystemClassLoader().
                        getResourceAsStream(filename));
            }
        } catch (Exception e) {
            System.out.println("could not find level sets");
        }
        try {
            bf = new BufferedReader(reader);
            String line;
            String path;
            String key = null;
            while ((line = bf.readLine()) != null) {
                line.trim();
                if (line.contains(":")) {
                    String[] parts = line.split(":");
                    key = parts[0];
                    String value = parts[1];
                    keys.add(key);
                    messages.add(value);
                } else {
                    path = line;
                    map.put(key, path);
                }
            }

        } catch (Exception e) {
            System.out.println(" Something went wrong while loading level sets!");
        } finally {
            try {
                if (bf != null) {
                    bf.close();
                }
            } catch (Exception e) {
                System.out.println(" Something went wrong closing bf!");
            }
        }
        String result = null;

        while (true) {
            SubMenu sub = new SubMenu(keyboard, keys, result, messages);
            List<LevelInformation> list = new ArrayList<LevelInformation>();
            File highscore = new File("highscores");
            HighScoresTable table = new HighScoresTable(10);
            if (highscore.exists()) {
                try {
                    table.load(highscore);
                } catch (IOException e) {
                    System.out.println(" Something went wrong while loading!");
                }
            }
            HighScoresAnimation highscoreAnimation = new HighScoresAnimation(table);
            GameFlow game = new GameFlow(ar, keyboard, gui);
            MenuAnimation<Task<Void>> menu = new MenuAnimation<Task<Void>>("Welcome to Arkanoid", keyboard);
            PlayTurnTask t = new PlayTurnTask(list, game);
            menu.addSelection("h", "Press H for ScoreTable"
                    , new ShowHiScoresTask(ar, highscoreAnimation, keyboard));
            menu.addSelection("s", "Press S for Game", t);
            menu.addSelection("q", "Press Q for Quit", new QuitTask());
            menu.addSubMenu(sub, ar2);
            ar.run(menu);
            try {
                result = sub.result();
                String classPath = map.get(result);
                list = LevelSpecificationReader.fromReader(new java.io.InputStreamReader(
                        ClassLoader.getSystemClassLoader().getResourceAsStream(classPath)));
            } catch (Exception e) {
                System.out.println(" Something went wrong while loading in main!");
            }
            t.setLevel(list);
            Task<Void> task = menu.getStatus();
            task.run();
        }

    }
}
