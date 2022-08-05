public class GuiPlayer implements Player {
    private char symbol;

    /**
     * GuiPlayer constructor.
     * @param x symbol
     */
    public GuiPlayer(char x) {
        symbol = x;
    }

    /**
     * we don't need this function
     * @param pointsArr
     * @param a
     * @return
     */
    @Override
    public Point oneMove(Point[] pointsArr, int a) {
     return null;
    }

    /**
     * @return player symbol.
     */
    @Override
    public char getSymbol() {
        return symbol;
    }
}

