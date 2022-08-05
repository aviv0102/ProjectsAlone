
import java.util.List;
import java.util.ArrayList;
/**
* @author Aviv Shisman 206558157
*/
public class Rectangle {
    //members:
    private double height;
    private double width;
    private Point upperLeft;
    private Line topL;
    private Line bottomL;
    private Line rightL;
    private Line leftL;
    /**the constructor creates a rectangle.
     * @param r the rectangle*/
    public Rectangle(Rectangle r) {
        this.height = r.getHeight();
        this.width = r.getWidth();
        this.upperLeft = new Point(r.getUpperLeft().getX(), r.getUpperLeft().getY());
        Point downLeft = new Point(upperLeft.getX(), upperLeft.getY() + this.getHeight());
        Point upperRight = new Point(upperLeft.getX() + this.getWidth(), upperLeft.getY());
        Point downRight = new Point(upperRight.getX(), upperRight.getY() + this.getHeight());
        this.topL = new Line(upperLeft, upperRight);
        this.bottomL = new Line(downLeft, downRight);
        this.leftL = new Line(upperLeft, downLeft);
        this.rightL = new Line(upperRight, downRight);
    }
    /**the constructor creates a rectangle.
     * @param upperLeft the upper left point of the rect
     * @param width the width
     * @param height the height*/
    public Rectangle(Point upperLeft, double width, double height) {
        this.height = height;
        this.width = width;
        this.upperLeft = upperLeft;
        Point downLeft = new Point(upperLeft.getX(), upperLeft.getY() + this.getHeight());
        Point upperRight = new Point(upperLeft.getX() + this.getWidth(), upperLeft.getY());
        Point downRight = new Point(upperRight.getX(), upperRight.getY() + this.getHeight());
        this.topL = new Line(upperLeft, upperRight);
        this.bottomL = new Line(downLeft, downRight);
        this.leftL = new Line(upperLeft, downLeft);
        this.rightL = new Line(upperRight, downRight);
    }
    /**gets all the intersection points of rect with a line.
     * @param line the line
     * @return list of points*/
    public List<Point> intersectionPoints(Line line) {
        List<Point> points = new ArrayList<Point>();
        if (line.isIntersecting(topL)) {
            points.add(line.intersectionWith(topL));
        }
        if (line.isIntersecting(bottomL)) {
            points.add(line.intersectionWith(bottomL));
        }
        if (line.isIntersecting(rightL)) {
            points.add(line.intersectionWith(rightL));
        }
        if (line.isIntersecting(leftL)) {
            points.add(line.intersectionWith(leftL));
        }

        return points;
    }
    /**get the width.
     * @return the width*/
    public double getWidth() {
        return this.width;
    }
    /**get the height.
     * @return the height*/
    public double getHeight() {
        return this.height;
    }
    /**get the upper left point.
     * @return the point */
    public Point getUpperLeft() {
        return this.upperLeft;
    }

}
