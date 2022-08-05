/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../ClientPlayer.h"

TEST(ClientPlayerTest,constructor){
    ClientPlayer p1(NULL, 'x');
    ASSERT_EQ('x',p1.getSymbol());
    EXPECT_FALSE(p1.getSymbol() !='x');

}

