
/**
* @author Aviv Shisman 206558157
*/
public class Point {
    //members:
    private double x;
    private double y;
    /** calculating distance beetwen two points.
     * @param x the x
     * @param y the y*/
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }
    /** calculating distance beetwen two points.
     * @param other (the point)
     * @return the distance */
    public double distance(Point other) {
        return Math.sqrt((this.x - other.x) * (this.x - other.x) + (this.y - other.y) * (this.y - other.y));
    }
    /** calculating if two points equal.
     * @param other (the point being equald)
     * @return true/false */
    public boolean equals(Point other) {
        if (this.x == other.x && this.y == other.y) {
            return true;
        }
        return false;
    }
    /** retriving the x cordinate.
     * @return this.x
     */
    public double getX() {
        return this.x;
    }
    /** retriving the y cordinate.
     * @return this.y
     */
    public double getY() {
        return this.y;
    }

}
