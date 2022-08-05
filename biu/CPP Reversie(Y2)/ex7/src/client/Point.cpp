/*aviv shisman 206558157
 * point gets x and y and creates a points
 */

#include "Point.h"
Point::Point(int a, int b): x(a),y(b){}

int Point::getX() const {
    return x;
}

int Point::getY() const {
    return y;
};