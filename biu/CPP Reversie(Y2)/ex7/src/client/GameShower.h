/*aviv shisman 206558157 01
 *rome sharon 209296235 01
 * interface,objects that will implement him
 * will be treated as a "screen"
 *explanation on the methods in the cpp file
 */

#ifndef ASS1_GAMESHOW_H
#define ASS1_GAMESHOW_H


class GameShower {
public:
    GameShower(){};
    virtual int getSize() const=0;
    virtual void show() const=0;
};


#endif //ASS1_GAMESHOW_H
