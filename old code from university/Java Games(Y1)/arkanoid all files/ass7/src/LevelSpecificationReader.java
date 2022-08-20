
import java.util.List;


import java.io.BufferedReader;
import java.util.ArrayList;
import java.awt.Color;
/**
* @author Aviv Shisman 206558157
*/
public class LevelSpecificationReader {

    /**reading a level defenition file and returning a list of levels.
     * @param reader the reader.
     * @return list of levels.
     * @throws Exception ...
     */
    public static List<LevelInformation> fromReader(java.io.Reader reader) throws Exception {

        List<LevelInformation> levels = new ArrayList<LevelInformation>();
        BufferedReader bf = null;
        String line;
        GenericLevel currentLV = null;
        java.util.Map<String, BlocksFromSymbolsFactory> map = new java.util.HashMap
                <String, BlocksFromSymbolsFactory>();
        //the block factory will be used to create blocks
        BlocksFromSymbolsFactory blockFac = null;
        int rowHeight = -1;
        int rowIndex = -1;
        int blockStartx = -1;
        int blockStarty = -1;

        try {

            bf = new BufferedReader(reader);
            boolean readingBlock = false;
            while ((line = bf.readLine()) != null) {
                line = line.trim();
                if ((!"".equals(line)) && (!line.startsWith("#"))) {
                    if (!readingBlock) {
                        if ("START_LEVEL".equals(line)) {
                            // creating new level
                            currentLV = new GenericLevel();
                        } else if ("END_LEVEL".equals(line)) {
                            // adding the created level and intiallizing all the
                            // variables
                            levels.add(currentLV);
                            currentLV = null;
                            blockFac = null;
                            rowHeight = -1;
                            rowIndex = -1;
                            blockStartx = -1;
                            blockStarty = -1;
                        } else if ("START_BLOCKS".equals(line)) {
                            readingBlock = true;
                            rowIndex = 0;
                        } else {
                            String[] parts = line.split(":");
                            String key = parts[0];
                            String value = parts[1];

                            if ("block_definitions".equals(key)) {
                                if (map.containsKey(value)) {
                                    blockFac = map.get(value);
                                } else {
                                    try {
                                        //java.io.Reader fr = new FileReader(
                                          //      value);
                                        //blockFac = BlockDef.fromReader(fr);
                                        blockFac = BlockDef.fromReader(new
                                         java.io.InputStreamReader(
                                         ClassLoader.getSystemClassLoader()
                                        .getResourceAsStream(value)));
                                    } catch (Exception e) {
                                        System.out.println(" Something w"
                                                + "ent wronsg");
                                    }
                                    map.put(value, blockFac);
                                }
                            } else if ("row_height".equals(key)) {
                                rowHeight = Integer.parseInt(value);
                            } else if ("blocks_start_x".equals(key)) {
                                blockStartx = Integer.parseInt(value);
                            } else if ("blocks_start_y".equals(key)) {
                                blockStarty = Integer.parseInt(value);
                            } else {
                                setLevel(currentLV, key, value);
                            }
                        }
                    } else if ("END_BLOCKS".equals(line)) {
                        readingBlock = false;
                    } else {
                        int currentX = blockStartx;
                        for (int i = 0; i < line.length(); i++) {
                            char symbol = line.charAt(i);
                            int currentY = rowIndex * rowHeight + blockStarty;
                            if (blockFac.isSpaceSymbol(symbol)) {
                                currentX += blockFac.getSpaceWidth(symbol);
                            } else {
                                Block b = null;
                                b = blockFac.getBlock(symbol, currentX, currentY);
                                if (b == null) {
                                    System.out.println(" Something wrong ");
                                }
                                currentX = (int) (currentX
                                        + b.getCollisionRectangle()
                                        .getWidth());
                                currentLV.addBlock(b);
                            }
                        }
                        rowIndex = rowIndex + 1;
                    }
                }
            }
        } finally {
            if (bf != null) {
                bf.close();
            }
        }

        return levels;
    }
    /**setting all the other properties in a level.
     * @param currentLevel the generic level.
     * @param key the key of string
     * @param value the value
     */
    private static void setLevel(GenericLevel currentLevel, String key, String value) {
        if ("level_name".equals(key)) {
            currentLevel.setName(value);
        } else {
            if ("background".equals(key)) {
                if ((value.startsWith("color(RGB(")) && (value.endsWith("))"))) {
                    String param = getValue(value, "color(RGB(", "))");
                    String[] parts = param.split(",");
                    int r = Integer.parseInt(parts[0].trim());
                    int g = Integer.parseInt(parts[1].trim());
                    int b = Integer.parseInt(parts[2].trim());
                    Color color = new Color(r, g, b);
                    currentLevel.setBack(new OneColorBack(color));
                } else if ((value.startsWith("color(")) && (value.endsWith(")"))) {
                    String param = getValue(value, "color(", ")");
                    try {
                        java.lang.reflect.Field field = Color.class.getField(param);
                        Color color = (Color) field.get(null);
                        currentLevel.setBack(new OneColorBack(color));
                    } catch (NoSuchFieldException e) {
                        throw new RuntimeException("Unsupported color name: " + param);
                    } catch (IllegalAccessException e) {
                        throw new RuntimeException("Unsupported color name: " + param);
                    }
                } else if ((value.startsWith("image(")) && (value.endsWith(")"))) {
                    String param = getValue(value, "image(", ")");
                    java.io.InputStream is = null;
                    try {
                         is =
                        ClassLoader.getSystemClassLoader().getResourceAsStream(param);
                        java.awt.image.BufferedImage image = javax
                                .imageio.ImageIO.read(is);
                        currentLevel.setBack(new ImgBack(image));
                    } catch (Exception e) {
                        throw new RuntimeException("Failed loading image: " + param, e);
                    } finally {
                        if (is != null) {
                            try {
                                is.close();
                            } catch (Exception e) {
                                throw new RuntimeException("Failed");
                            }
                        }
                    }
                }
            }
            if ("ball_velocities".equals(key)) {
                String[] velocitiesDef = value.split(" ");
                for (String velDef : velocitiesDef) {
                    String[] v = velDef.split(",");

                    currentLevel.addVelocity(
                            Velocity.fromAngleAndSpeed(
                                    Double.parseDouble(v[0]),
                                    Double.parseDouble(v[1])));

                }

            } else if ("paddle_speed".equals(key)) {
                currentLevel.setSpeed(Integer.parseInt(value));
            } else if ("paddle_width".equals(key)) {
                currentLevel.setWidth(Integer.parseInt(value));
            } else if ("num_blocks".equals(key)) {
                currentLevel.setBlocksToClear(Integer.parseInt(value));
            }
        }
    }
    /** extracting from a string the value we want.
     * @param value the value
     * @param pref the prefix
     * @param post the postfix
     * @return the wanted val
     */
    private static String getValue(String value, String pref, String post) {
        return value.substring(pref.length(), value.length() - post.length());
    }
}
