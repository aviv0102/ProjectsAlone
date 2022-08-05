/*aviv shisman 206558157
 * an interface for all rules
 * every rule will be checked
 * and after we check the rule we apply it
 *  */
#include "Cell.h"
#ifndef ASS1_RULE_H
#define ASS1_RULE_H


class Rule {
public:
    Rule(){

    }
    virtual int check(Cell**,int,int,char) const=0;
    virtual void apply(Cell**,int,int,char) const=0;

};


#endif //ASS1_RULE_H
