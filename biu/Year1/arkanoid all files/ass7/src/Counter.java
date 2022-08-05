
/**
* @author Aviv Shisman 206558157
*/
public class Counter {
    //the members:
    private int counter;
    /**the counter constructor.*/
    public Counter() {
        this.counter = 0;
    }
    /** add a number to the counter.
     * @param number the number*/
    public void increase(int number) {
        this.counter = counter + number;
    }
    /** remove a number from the counter.
     * @param number the number*/
    void decrease(int number) {
        this.counter = counter - number;
    }
    /** get counter value.
     * @return the value*/
    int getValue() {
        return this.counter;
    }

}
