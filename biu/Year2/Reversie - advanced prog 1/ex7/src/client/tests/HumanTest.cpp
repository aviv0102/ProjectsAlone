/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../HumanPlayer.h"


TEST(HumanPlayerTest,testSymbol){
    HumanPlayer p1('x');
    HumanPlayer p2('o');
    ASSERT_EQ('x',p1.getSymbol());
    ASSERT_EQ('o',p2.getSymbol());
    EXPECT_FALSE(p1.getSymbol()=='o');
    EXPECT_FALSE(p1.getSymbol()!='x');

}
