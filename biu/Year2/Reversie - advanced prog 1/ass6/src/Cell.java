public class Cell {
    char symbol;

    Cell(char s) { symbol = s;}

    Cell() { symbol = 'a';}

    /**
     * checking if the cell is empty
     */
    boolean isEmpty() {
        if(symbol=='x' || symbol=='o'){
            return false;
        }
        return true;
    }

    char opposite() {
        if(symbol=='x'){
            return 'o';
        }
        if(symbol=='o'){
            return 'x';
        }
        return 'a';
    }
}
