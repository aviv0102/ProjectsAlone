public interface Rule {
    boolean check(Cell[][] arr,int x,int y,char c);
    void apply(Cell[][] arr,int x,int y,char c);
}
