import java.awt.Color;

import biuoop.DrawSurface;
/**
* @author Aviv Shisman 206558157
*/
public class HighScoresAnimation implements Animation {
    //members:
    private HighScoresTable table;
    /** the constructor.
     * @param table the table
     */
    public HighScoresAnimation(HighScoresTable table) {
        this.table = table;
    }
    /**the do one frame method.
     * @param d the surface
     * @param dt the speed by time.
     */
    public void doOneFrame(DrawSurface d, double dt) {
        d.setColor(Color.GRAY);
        d.drawRectangle(0, 0, 800, 800);
        d.setColor(Color.RED);
        d.drawText(100, 50, "HighScore Table", 28);
        d.setColor(Color.green);
        d.drawText(150, 100, "Player Name        Score", 20);
        d.drawText(150, 105, "________________________", 20);
        d.drawText(150, 555, "Press Space to Continuo", 30);

        for (int i = 0; i < table.size(); i++) {
            if (i == table.sizeMax()) {
                break;
            }
            d.setColor(Color.blue);
            ScoreInfo info = table.getHighScores().get(i);
            d.drawText(150, 130 + 24 * (i), info.getName(), 20);
            d.drawText(300, 130 + 24 * (i), Integer.toString(info.getScore()), 20);
        }

    }

    /**
     * telling the animation runner to stop.
     * @return to stop or not
     */
    public boolean shouldStop() {
        return true;
    }

}
