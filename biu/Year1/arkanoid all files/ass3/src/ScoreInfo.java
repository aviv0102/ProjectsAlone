
/**
* @author Aviv Shisman 206558157
*/
public class ScoreInfo {
    //members:
    private String name;
    private int score;
    /** the constructor.
     * @param name the name of the player
     * @param score what the score he got
     */
    public ScoreInfo(String name, int score) {
        this.score = score;
        this.name = name;
    }
    /** get the player name.
     * @return the name
     */
    public String getName() {
        return this.name;
    }
    /** return the score.
     * @return ...
     */
    public int getScore() {
        return this.score;
    }




}
