
import java.util.List;
import java.io.File;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.PrintWriter;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
*/
public class HighScoresTable {
    //members:
    private int maxsize;
    private List<ScoreInfo> scores;
    /**the constructor.
     * @param size the wanted size of the table.
     */
    public HighScoresTable(int size) {
        this.scores = new ArrayList<ScoreInfo>();
        this.maxsize = size;
    }
    /**adding element to the table.
     * @param score the element.
     */
    public void add(ScoreInfo score) {
        this.scores.add(score);
    }
    /**get the size of table.
     * @return the size
     */
    public int size() {
        return this.scores.size();
    }
    /**get the size of table.
     * @return the size
     */
    public int sizeMax() {
        return this.maxsize;
    }
    /** get the highest scores.
     * @return list of them in size we got in constructor.
     */
    public List<ScoreInfo> getHighScores() {
        List<ScoreInfo> highest = new ArrayList<ScoreInfo>();
        for (int i = 0; i < scores.size(); i++) {
            for (int j = 0; j < scores.size() - 1; j++) {
                if (scores.get(j).getScore() < scores.get(j + 1).getScore()) {
                    ScoreInfo temp = scores.get(j);
                    scores.set(j, scores.get(j + 1));
                    scores.set(j + 1, temp);
                }
            }
        }
        for (int i = 0; i < scores.size(); i++) {
            highest.add(scores.get(i));
            if (i == this.maxsize) {
                break;
            }
        }

        return highest;
    }
    /**get the rank of a score.
     * @param score the score
     * @return the rank.
     */
    public int getRank(int score) {
        List<ScoreInfo> arr = new ArrayList<ScoreInfo>(this.getHighScores());
        for (int i = 0; i < arr.size(); i++) {
            if (arr.get(i).getScore() < score) {
                return i + 1;
            }
        }
        return 0;

    }
    /**clear the table. */
    public void clear() {
        this.scores.clear();
    }
    /**save to the file.
     * @param filename the file
     * @throws IOException ...
     */
    public void save(File filename) throws IOException {
        List<ScoreInfo> arr = new ArrayList<ScoreInfo>(this.getHighScores());
        PrintWriter os = null;
        try {
            // writing to a file in the consept of name-score
            // later we will split by the '-'
            os = new PrintWriter(new OutputStreamWriter(new FileOutputStream(filename)));
            for (int i = 0; i < maxsize; i++) {
                os.println(arr.get(i).getName() + "-" + Integer.toString(arr.get(i).getScore()));
            }
        } catch (Exception e) {
            System.out.println(" Something went wrong while save !");
        } finally {
            if (os != null) {
                os.close();
            }
        }

    }
    /**load from a file to our table.
     * @param filename the file.
     * @throws IOException ...
     */
    public void load(File filename) throws IOException {
        List<String> arr = new ArrayList<String>();
        BufferedReader is = null;
        try {
            is = new BufferedReader(new InputStreamReader(new FileInputStream(filename)));
            String line;
            while ((line = is.readLine()) != null) {
                arr.add(line);
            }
        } catch (Exception e) {
            System.out.println(" Something went wrong while load !");
        } finally {
            if (is != null) { // Exception might have happened at constructor
                try {
                    is.close(); // closes FileInputStream too
                } catch (IOException e) {
                    System.out.println(" Failed closing the file !");
                }
            }
        }
        List<ScoreInfo> newList = new ArrayList<ScoreInfo>();
        for (int i = 0; i < arr.size(); i++) {
            String[] tok = arr.get(i).split("-", 2);
            String name = tok[0];
            int score = 0;
            try {
                score = Integer.parseInt(tok[1]);
            } catch (Exception e) {
                System.out.println(" Something went wrong!");
            }
            ScoreInfo info = new ScoreInfo(name, score);
            newList.add(info);
        }
        this.scores = newList;
    }
}
