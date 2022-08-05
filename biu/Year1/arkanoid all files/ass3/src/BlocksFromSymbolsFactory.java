import java.util.Map;
/**
* @author Aviv Shisman 206558157
*/
public class BlocksFromSymbolsFactory {
    //members:
    private Map<Character, Integer> spacersMap;
    private Map<Character, Block> blockMap;
    /** the constructor.
     * @param spacers the spaces map
     * @param blockMap ...
     */
    public BlocksFromSymbolsFactory(Map<Character, Integer> spacers, Map<Character, Block> blockMap) {
        this.spacersMap = spacers;
        this.blockMap = blockMap;

    }
    /** return true if is spacer.
     * @param s a char
     * @return true or false
     */
    public boolean isSpaceSymbol(char s) {
        if (this.spacersMap.containsKey(s)) {
            return true;
        }
        return false;
    }

    /** return true if is blockSymbol.
     * @param s a char
     * @return true or false
     */
    public boolean isBlockSymbol(char s) {
        if (this.blockMap.containsKey(s)) {
            return true;
        }
        return false;
    }
     /** creating blocks by the block map and symbol c.
      * @param c a char
      * @param xpos the x position.
      * @param ypos the y position
      * @return new block
      */
    public Block getBlock(char c, int xpos, int ypos) {
        if (this.blockMap.containsKey(c)) {
            Block b = this.blockMap.get(c);
            Block a = new Block(b);
            a.setPoint(xpos, ypos);
            return a;
        }
        return null;
    }
    /** getting the spacers value.
     * @param s the spacer symbol
     * @return the value of it
     */
    public int getSpaceWidth(char s) {
        if (this.spacersMap.containsKey(s)) {
            return this.spacersMap.get(s);
        }
        return 0;
    }
}
