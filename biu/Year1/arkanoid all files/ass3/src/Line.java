
import java.util.List;
/**
* @author Aviv Shisman 206558157
*/
public class Line {
    //members:
    private Point start;
    private Point end;
    /** the constructor for points.
     * @param start the start of the line
     * @param end the end of the line */
    public Line(Point start, Point end) {
        this.start = start;
        this.end = end;
    }
    /** the constructor for variables.
    * @param x1 the start of the line1
    * @param y1 the end of the line1
    * @param x2 the start of the line2
    * @param y2 the end of the line2 */
    public Line(double x1, double y1, double x2, double y2) {
        this.start = new Point(x1, y1);
        this.end = new Point(x2, y2);
    }
    /** calculting the length.
     * @return length of line.*/
    public double length() {
        return this.start.distance(end);
    }
    /** gets the start of line.
     * @return start point.*/
    public Point start() {
        return this.start;
    }
    /** gets the end of line.
     * @return end point.*/
    public Point end() {
        return this.end;
    }
    /** gets the middle of line.
     * @return middle point.*/
    public Point middle() {
        double x1 = start.getX();
        double x2 = end.getX();
        double a = (x1 + x2) / 2;
        double y1 = start.getY();
        double y2 = end.getY();
        double b = (y1 + y2) / 2;
        Point middle = new Point(a, b);

        return middle;
    }
    /** gets if there intersection between two lines.
     * @param other - the other line
     * @return true/false.*/
    public boolean isIntersecting(Line other) {
        float x1 = (float) this.start.getX();
        float x2 = (float) this.end.getX();
        float y1 = (float) this.start.getY();
        float y2 = (float) this.end.getY();
        float x3 = (float) other.start.getX();
        float x4 = (float) other.end.getX();
        float y3 = (float) other.start.getY();
        float y4 = (float) other.end.getY();
        //calculating the intersection point by the lines continuation.
        Point a = this.intersectionWith(other);
        if (a == null) {
            return false;
        }
        int flag = 0;
        //if the point a is between the lines return true.
        if ((x1 <= (float) a.getX() && (float) a.getX() <= x2)
                || (x1 >= (float) a.getX() && (float) a.getX() >= x2)) {
            flag++;
        }
        if ((x3 <= (float) a.getX() && (float) a.getX() <= x4)
                || (x3 >= (float) a.getX() && (float) a.getX() >= x4)) {
            flag++;
        }
        if ((y1 <= (float) a.getY() && (float) a.getY() <= y2)
                || (y1 >= (float) a.getY() && (float) a.getY() >= y2)) {
            flag++;
        }
        if ((y3 <= (float) a.getY() && (float) a.getY() <= y4)
                || (y3 >= (float) a.getY() && (float) a.getY() >= y4)) {
            flag++;
        }
        if (flag == 4) {
            return true;
        }

        return false;
    }
    /** gets the intersection point by the lines continuation.
     * @param other the other line.
     * @return point of the intersections.*/
    public Point intersectionWith(Line other) {
        double x1 = this.start.getX();
        double x2 = this.end.getX();
        double y1 = this.start.getY();
        double y2 = this.end.getY();
        double x3 = other.start.getX();
        double x4 = other.end.getX();
        double y3 = other.start.getY();
        double y4 = other.end.getY();
        double d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
        if (d == 0) {
            return null;
        }
        double xi = ((x3 - x4) * (x1 * y2 - y1 * x2) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d;
        double yi = ((y3 - y4) * (x1 * y2 - y1 * x2) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d;

        return new Point(xi, yi);

    }
    /** check if lines equal.
     * @param other -other line.
     * @return true/false.*/
    public boolean equals(Line other) {
        int flag = 0;
        if (this.start.equals(other.start) && this.end.equals(other.end)) {
            flag++;
        }
        if (this.start.equals(other.end) && this.end.equals(other.start)) {
            flag++;
        }
        if (flag == 1) {
            return true;
        }
        return false;
    }
    /** get the closet intersection point to start of the line from the rectangle.
     * @param rect the rectangle.
     * @return point.*/
    public Point closestIntersectionToStartOfLine(Rectangle rect) {
        Point p = null;
        if (rect.intersectionPoints(this).size() > 0) {
            List<Point> points = rect.intersectionPoints(this);
            Point temp = points.get(0);
            for (int i = 0; i < points.size(); i++) {
                if (temp.distance(this.start) > points.get(i).distance(this.start)) {
                    temp = points.get(i);
                }
            }
            return temp;
        }

        return p;
    }

}
