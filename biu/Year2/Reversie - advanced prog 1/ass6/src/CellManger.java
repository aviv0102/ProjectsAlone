public class CellManger {
    int size;
    Cell[][] arr;

    CellManger(int s) {
        size = s;
        arr = new Cell[size + 3][size + 3];
        for (int i = 0; i < size + 3; i++) {
            for (int j = 0; j < size + 3; j++) {
                arr[i][j] = new Cell('a');
            }
        }

    }

    int getSize() {
        return size;
    }

    void setBlack(int x, int y) {
        arr[x][y].symbol = 'x';
    }

    void setWhite(int x, int y) {
        arr[x][y].symbol = 'o';
    }

    Cell[][] getArr() {
        return arr;
    }

    void setArr(Cell[][] a) {
        for (int i = 0; i < size + 3; i++) {
            for (int j = 0; j < size + 3; j++) {
                arr[i][j].symbol = a[i][j].symbol;
            }
        }
    }

    void setCell(int i, int j, char s) {
        arr[i][j].symbol = s;
    }

    int getCount(char symbol) {
        int counter = 0;
        for (int i = 0; i < size + 3; ++i) {
            for (int j = 0; j < size + 3; ++j) {
                if (arr[i][j].symbol == symbol) {
                    counter++;
                }
            }
        }
        return counter;
    }

    Cell getCell(int i, int j) {
        return arr[i][j];
    }
}
