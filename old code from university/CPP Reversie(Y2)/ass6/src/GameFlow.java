import javafx.scene.control.Alert;
import javafx.scene.control.Label;

public class GameFlow {
    private CellManger manger;
    private Rule rule;
    private Player[] players;
    private int current;
    private int numOfPieces;
    private int size;
    private Label status;
    private Label firstScore;
    private Label secondScore;
    private int noMovesCounter;

    /**
     * GameFlow constructor
     *
     * @param c    cellManger
     * @param r    Rule
     * @param p    players array
     * @param s    size of board
     * @param stat status of the game
     * @param fir  Label score of first player
     * @param sec  Label score of second player
     */
    GameFlow(CellManger c, Rule r, Player[] p, int s, Label stat, Label fir, Label sec) {
        manger = c;
        rule = r;
        players = p;
        size = s;
        current = 0;
        numOfPieces = 4;
        status = stat;
        firstScore = fir;
        secondScore = sec;
        noMovesCounter = 0;
    }

    public CellManger getCellManger() {
        return manger;
    }

    public int getSize() {
        return size;
    }

    /**
     * pass the move to the other player
     */
    public void next() {
        current++;
        if (current == 2) {
            current = 0;
        }
    }

    /**
     * @return current player
     */
    public Player getCurrentPlayers() {
        return players[current];
    }

    /**
     * change status label to no moves or inGame
     *
     * @param answer true:no moves, false:InGame
     */
    public void noMoves(boolean answer) {
        if (answer) {
            this.status.setText("no Moves" +
                    " Press to Continue");
            this.noMovesCounter++;
        } else {
            this.status.setText("In Game");
            this.noMovesCounter = 0;
        }
    }

    public int getNoMovesCounter() {
        return this.noMovesCounter;
    }

    /**
     * Apply the status of the board in the player choose.
     *
     * @param a Point the player choose to play
     * @return true if game is still played, false if game over.
     */
    boolean playOneTurn(Point a) {
        //set the point on the board
        if (players[current].getSymbol() == 'x') {
            manger.setBlack(a.getX(), a.getY());
        } else {
            manger.setWhite(a.getX(), a.getY());
        }
        numOfPieces++;
        //applying the rule: flipping the appropriate pieces
        rule.apply(manger.getArr(), a.getX(), a.getY(), players[current].getSymbol());
        current++;

        if (current == 2) {
            current = 0;
        }
        //set score label
        firstScore.setText("First Score: " + manger.getCount(players[0].getSymbol()));
        secondScore.setText("Second Score: " + manger.getCount(players[1].getSymbol()));

        //game is over
        if (numOfPieces >= size * size) {
            gameOver(false);
            return false;
        }
        return true;
    }

    public void gameOver(boolean noTurns) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        String s;
        if (noTurns) {
            alert.setHeaderText("There are no moves for both players");
        } else {
            alert.setHeaderText(null);
        }
        if (this.manger.getCount('x') > this.manger.getCount('o')) {
            s = "First won Game Over";
            status.setText("First won Game Over");
        } else if (this.manger.getCount('x') < this.manger.getCount('o')) {
            s = "Second won Game Over";
            status.setText("Second won Game Over");
        } else {
            s = "It's a Tie Game Over";
            status.setText("It's a Tie Game Over");
        }
        alert.setTitle("Winner");
        alert.setContentText(s);

        alert.showAndWait();
    }


    /**
     * apply the board with 'z' means optional moves for the current player.
     *
     * @return true:there are moves, false:no optional moves for the current player.
     */
    public boolean setPossibleMoves() {
        //going trough all the cells in the array and checking who is valid place to set piece
        int i = 0, j = 0, k = 0;
        //check if there are optional moves
        for (i = 1; i <= size; i++) {
            for (j = 1; j <= size; j++) {
                if (rule.check(manger.getArr(), i, j, players[current].getSymbol())) {
                    manger.getArr()[i][j].symbol = 'z';
                    k++;
                }
            }
        }
        if (k == 0) {
            return true;
        }
        return false;
    }
}
