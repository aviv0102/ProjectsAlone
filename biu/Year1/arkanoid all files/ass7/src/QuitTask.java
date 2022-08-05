/**
* @author Aviv Shisman 206558157
*/
public class QuitTask implements Task<Void> {
    /** quits the game.
     * @return void...
     */
    public Void run() {
        System.exit(0);
        return null;
    }
}
