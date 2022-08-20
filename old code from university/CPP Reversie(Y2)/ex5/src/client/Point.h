/*aviv shisman 206558157
 * regular point class.
 */

#ifndef ASS1_POINT_H
#define ASS1_POINT_H


class Point {
public:
    Point(int,int);
    int getX() const;
    int getY() const;

private:
    int y;
    int x;
};


#endif //ASS1_POINT_H
