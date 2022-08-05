public class ReverseRule implements Rule {

    @Override
    public boolean check(Cell[][] arr, int x, int y, char c) {
        if(!arr[x][y].isEmpty()){
            return false;
        }
        if(x==0 || y==0){
            return false;
        }
        if(up(arr,x, y,c) ||right(arr,x, y,c) ||down(arr,x, y,c) ||left(arr,x, y,c) ||
                upRight(arr,x, y,c) ||upLeft(arr,x, y,c) ||downLeft(arr,x, y,c)
                ||downRight(arr,x, y,c)){
            return true;
        }



        return false;    }

    @Override
    public void apply(Cell[][] arr, int x, int y, char c) {
        if (right(arr, x, y, c)) {
            applyRight(arr, x, y, c);
        }
        if (down(arr, x, y, c)) {
            applyDown(arr, x, y, c);
        }
        if (up(arr, x, y, c)) {
            applyUp(arr, x, y, c);
        }
        if (left(arr, x, y, c)) {
            applyLeft(arr, x, y, c);
        }
        if (upRight(arr, x, y, c)) {
            applyUpRight(arr, x, y, c);
        }
        if (upLeft(arr, x, y, c)) {
            applyUpLeft(arr, x, y, c);
        }
        if (downLeft(arr, x, y, c)) {
            applyDownLeft(arr, x, y, c);
        }
        if (downRight(arr, x, y, c)) {
            applyDownRight(arr, x, y, c);
        }
    }

    void applyDown(Cell[][] arr, int x, int y, char c) {
        int i = 1;
        if (c == 'x') {
            if (arr[x][y + 1].symbol == 'o') {
                do {
                    arr[x][y + i].symbol = arr[x][y + i].opposite();
                    i++;
                    if (arr[x][y + i].symbol == 'x') {
                        return;
                    }

                } while (arr[x][y + i].symbol == 'o');
            }
        }
        if (c == 'o') {
            if (arr[x][y + 1].symbol == 'x') {
                do {
                    arr[x][y + i].symbol = arr[x][y + i].opposite();

                    i++;
                    if (arr[x][y + i].symbol == 'o') {
                        return;
                    }
                } while (arr[x][y + i].symbol == 'x');
            }
        }
        return;
    }

    void applyUp(Cell[][] arr, int x, int y, char c) {
        int i=1;
        if(y<=1){
            return;
        }
        if(c=='x') {
            if (arr[x][y - 1].symbol == 'o') {
                do {
                    arr[x][y-i].symbol=arr[x][y-i].opposite();
                    i++;
                    if (arr[x][y - i].symbol == 'x') {
                        return;
                    }

                }while(arr[x][y - i].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x][y - 1].symbol == 'x') {
                do {
                    arr[x][y-i].symbol=arr[x][y-i].opposite();

                    i++;
                    if (arr[x][y - i].symbol == 'o') {
                        return;
                    }
                }while(arr[x][y - i].symbol == 'x');
            }
        }
        return;



    }

    void applyRight(Cell[][] arr, int x, int y, char c) {
        int i=1;
        if(c=='x') {
            if (arr[x+ 1][y].symbol == 'o') {
                do {
                    arr[x+i][y].symbol=arr[x+i][y].opposite();
                    i++;
                    if (arr[x + i][y].symbol == 'x') {
                        return;
                    }

                }while(arr[x+ i][y].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+ 1][y ].symbol == 'x') {
                do {
                    arr[x+i][y].symbol=arr[x+i][y].opposite();
                    i++;
                    if (arr[x+ i][y ].symbol == 'o') {
                        return;
                    }
                }while(arr[x+ i][y ].symbol == 'x');
            }
        }
        return;

    }

    void applyLeft(Cell[][] arr, int x, int y, char c) {
        int i=1;
        if(x<=1){
            return ;
        }
        if(c=='x') {
            if (arr[x-1][y].symbol == 'o') {
                do {
                    arr[x-i][y].symbol=arr[x-i][y].opposite();
                    i++;
                    if (arr[x - i][y].symbol == 'x') {
                        return;
                    }
                }while(arr[x- i][y].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y].symbol == 'x') {
                do {
                    arr[x-i][y].symbol=arr[x-i][y].opposite();
                    i++;
                    if (arr[x-i][y].symbol == 'o') {
                        return ;
                    }
                }while(arr[x- i][y].symbol == 'x');
            }
        }
        return ;
    }

    void applyUpRight(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(y<=1){
            return;
        }
        if(c=='x') {
            if (arr[x+1][y-1 ].symbol == 'o') {
                do {
                    arr[x+i][y-j].symbol=arr[x+i][y-j].opposite();
                    i++;
                    j++;
                    if (arr[x + i][y-j].symbol == 'x') {
                        return ;
                    }
                }while(arr[x+ i][y-j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+1][y-1 ].symbol == 'x') {
                do {
                    arr[x+i][y-j].symbol=arr[x+i][y-j].opposite();
                    i++;
                    j++;
                    if (arr[x + i][y-j].symbol == 'o') {
                        return ;
                    }
                }while(arr[x + i][y-j].symbol == 'x');
            }
        }
        return ;
    }

    void applyUpLeft(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(y<=1 || x<=1){
            return ;
        }
        if(c=='x') {
            if (arr[x-1][y-1 ].symbol == 'o') {
                do {
                    arr[x-i][y-j].symbol=arr[x-i][y-j].opposite();
                    i++;
                    j++;
                    if (arr[x - i][y-j].symbol == 'x') {
                        return ;
                    }
                }while(arr[x- i][y-j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y-1 ].symbol == 'x') {
                do {
                    arr[x-i][y-j].symbol=arr[x-i][y-j].opposite();
                    i++;
                    j++;
                    if (arr[x - i][y-j].symbol == 'o') {
                        return ;
                    }
                }while(arr[x - i][y-j].symbol == 'x');
            }
        }
        return ;
    }

    void applyDownRight(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(c=='x') {
            if (arr[x+1][y+1 ].symbol == 'o') {
                do {
                    arr[x+i][y+j].symbol=arr[x+i][y+j].opposite();
                    i++;
                    j++;
                    if (arr[x + i][y+j].symbol == 'x') {
                        return;
                    }
                }while(arr[x+ i][y+j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+1][y+1 ].symbol == 'x') {
                do {
                    arr[x+i][y+j].symbol=arr[x+i][y+j].opposite();
                    i++;
                    j++;
                    if (arr[x + i][y+j].symbol == 'o') {
                        return;
                    }
                }while(arr[x + i][y+j].symbol == 'x');
            }
        }
        return;
    }

    void applyDownLeft(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(x<=1){
            return ;
        }
        if(c=='x') {
            if (arr[x-1][y+1 ].symbol == 'o') {
                do {
                    arr[x-i][y+j].symbol=arr[x-i][y+j].opposite();
                    i++;
                    j++;
                    if (arr[x - i][y+j].symbol == 'x') {
                        return ;
                    }
                }while(arr[x- i][y+j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y+1 ].symbol == 'x') {
                do {
                    arr[x-i][y+j].symbol=arr[x-i][y+j].opposite();
                    i++;
                    j++;
                    if (arr[x - i][y+j].symbol == 'o') {
                        return ;
                    }
                }while(arr[x - i][y+j].symbol == 'x');
            }
        }
        return ;
    }

    boolean down(Cell[][]arr, int x, int y, char c) {
        int i=1;
        if(c=='x') {
            if (arr[x][y + 1].symbol == 'o') {
                do {
                    i++;
                    if (arr[x][y + i].symbol == 'x') {
                        return true;
                    }
                }while(arr[x][y + i].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x][y + 1].symbol == 'x') {
                do {
                    i++;
                    if (arr[x][y + i].symbol == 'o') {
                        return true;
                    }
                }while(arr[x][y + i].symbol == 'x');
            }
        }
        return false;
    }

    boolean up(Cell[][]arr, int x, int y, char c) {
        int i=1;
        if(y<=1){
            return false;
        }
        if(c=='x') {
            if (arr[x][y - 1].symbol == 'o') {
                do {
                    i++;
                    if (arr[x][y - i].symbol == 'x') {
                        return true;
                    }
                }while(arr[x][y - i].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x][y - 1].symbol == 'x') {
                do {
                    i++;
                    if (arr[x][y - i].symbol == 'o') {
                        return true;
                    }
                }while(arr[x][y - i].symbol == 'x');
            }
        }
        return false;
    }
    boolean right(Cell[][]arr, int x, int y, char c) {
        int i=1;
        if(c=='x') {
            if (arr[x+ 1][y].symbol == 'o') {
                do {
                    i++;
                    if (arr[x + i][y].symbol == 'x') {
                        return true;
                    }
                }while(arr[x+ i][y].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+1][y].symbol == 'x') {
                do {
                    i++;
                    if (arr[x+ i][y].symbol == 'o') {
                        return true;
                    }
                }while(arr[x+ i][y].symbol == 'x');
            }
        }
        return false;
    }
    boolean left(Cell[][]arr, int x, int y, char c) {
        int i=1;
        if(x<=1){
            return false;
        }
        if(c=='x') {
            if (arr[x-1][y].symbol == 'o') {
                do {
                    i++;
                    if (arr[x - i][y].symbol == 'x') {
                        return true;
                    }
                }while(arr[x- i][y].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y].symbol == 'x') {
                do {
                    i++;
                    if (arr[x-i][y].symbol == 'o') {
                        return true;
                    }
                }while(arr[x- i][y].symbol == 'x');
            }
        }
        return false;
    }
    boolean downRight(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(c=='x') {
            if (arr[x+1][y+1 ].symbol == 'o') {
                do {
                    i++;
                    j++;
                    if (arr[x + i][y+j].symbol == 'x') {
                        return true;
                    }
                }while(arr[x+ i][y+j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+1][y+1 ].symbol == 'x') {
                do {
                    i++;
                    j++;
                    if (arr[x + i][y+j].symbol == 'o') {
                        return true;
                    }
                }while(arr[x + i][y+j].symbol == 'x');
            }
        }
        return false;
    }

    boolean downLeft(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(x<=1){
            return false;
        }
        if(c=='x') {
            if (arr[x-1][y+1 ].symbol == 'o') {
                do {
                    i++;
                    j++;
                    if (arr[x - i][y+j].symbol == 'x') {
                        return true;
                    }
                }while(arr[x- i][y+j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y+1 ].symbol == 'x') {
                do {
                    i++;
                    j++;
                    if (arr[x - i][y+j].symbol == 'o') {
                        return true;
                    }
                }while(arr[x - i][y+j].symbol == 'x');
            }
        }
        return false;
    }

    boolean upRight(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(y<=1){
            return false;
        }
        if(c=='x') {
            if (arr[x+1][y-1 ].symbol == 'o') {
                do {
                    i++;
                    j++;
                    if (arr[x + i][y-j].symbol == 'x') {
                        return true;
                    }
                }while(arr[x+ i][y-j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x+1][y-1 ].symbol == 'x') {
                do {
                    i++;
                    j++;
                    if (arr[x + i][y-j].symbol == 'o') {
                        return true;
                    }
                }while(arr[x + i][y-j].symbol == 'x');
            }
        }
        return false;
    }

    boolean upLeft(Cell[][] arr, int x, int y, char c) {
        int i=1;
        int j=1;
        if(y<=1 || x<=1){
            return false;
        }
        if(c=='x') {
            if (arr[x-1][y-1 ].symbol == 'o') {
                do {
                    i++;
                    j++;
                    if (arr[x - i][y-j].symbol == 'x') {
                        return true;
                    }
                }while(arr[x- i][y-j].symbol == 'o');
            }
        }
        if(c=='o') {
            if (arr[x-1][y-1 ].symbol == 'x') {
                do {
                    i++;
                    j++;
                    if (arr[x - i][y-j].symbol == 'o') {
                        return true;
                    }
                }while(arr[x - i][y-j].symbol == 'x');
            }
        }
        return false;
    }
}

