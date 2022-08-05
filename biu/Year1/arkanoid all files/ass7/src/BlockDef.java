
import java.io.BufferedReader;
import java.io.Reader;
import java.util.Map;
/**
* @author Aviv Shisman 206558157
*/
public class BlockDef {
    /** reading block definition file.
     * @param reader the file reader.
     * @return fitting Block factory.
     * @throws Exception ...
     */
    public static BlocksFromSymbolsFactory fromReader(Reader reader) throws Exception {
        BufferedReader bf = null;
        Map<Character, Integer> spacermap = new java.util.HashMap<Character, Integer>();
        Map<Character, Block> blockmap = new java.util.HashMap<Character, Block>();
        Map<String, String> defultMap = new java.util.HashMap<String, String>();
        String line;
        bf = new BufferedReader(reader);
        while ((line = bf.readLine()) != null) {
            line.trim();
            char symbol = '\0';
            char spacerSymbol = '\0';
            if (line.startsWith("#") || line.equals("")) {
                continue;
            }
            if (line.startsWith("default")) {

                String[] arrStr = line.split(" ");
                for (int i = 0; i < arrStr.length; i++) {
                    if (!arrStr[i].contains(":")) {
                        continue;
                    }
                    String[] parts = arrStr[i].split(":");
                    String key = parts[0];
                    String value = parts[1];
                    if (!arrStr[i].startsWith("default")) {
                        defultMap.put(key, value);
                    }

                }
            }
            java.util.HashMap<Integer, String> fillmap = new java.util.HashMap<Integer, String>();
            if (line.startsWith("bdef")) {
                Block b = new Block();
                for (Map.Entry<String, String> entry : defultMap.entrySet()) {
                    String key = entry.getKey();
                    String value = entry.getValue();
                    if (key.startsWith("width")) {
                        b.setWidth(Integer.parseInt(value));
                    }
                    if (key.startsWith("height")) {
                        b.setHeight(Integer.parseInt(value));
                    }
                    if (key.startsWith("stroke")) {
                        b.setStroke(value);
                    }
                    if (key.startsWith("hit_points")) {
                        b.setLives(Integer.parseInt(value));
                    }
                    if (key.startsWith("fill")) {
                        if (key.startsWith("fill-")) {
                            String[] fillArr = key.split("-");
                            fillmap.put(Integer.parseInt(fillArr[1]), value);
                        } else {
                            fillmap.put(1, value);
                        }
                    }
                    // finishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh here
                }
                String[] arrStr = line.split(" ");
                for (int i = 0; i < arrStr.length; i++) {
                    if (!arrStr[i].contains(":")) {
                        continue;
                    }
                    String[] parts = arrStr[i].split(":");
                    String key = parts[0];
                    String value = parts[1];
                    if (arrStr[i].startsWith("symbol")) {
                        symbol = value.charAt(0);
                    }
                    if (arrStr[i].startsWith("width")) {
                        b.setWidth(Integer.parseInt(value));
                    }
                    if (arrStr[i].startsWith("height")) {
                        b.setHeight(Integer.parseInt(value));
                    }
                    if (arrStr[i].startsWith("hit_points")) {
                        b.setLives(Integer.parseInt(value));
                    }
                    if (arrStr[i].startsWith("fill")) {
                        if (arrStr[i].startsWith("fill-")) {
                            String[] fillArr = key.split("-");
                            fillmap.put(Integer.parseInt(fillArr[1]), value);
                        } else {
                            fillmap.put(1, value);
                        }
                    }
                    if (arrStr[i].startsWith("stroke")) {
                        b.setStroke(value);
                    }
                }

                b.setFillMap(fillmap);
                blockmap.put(symbol, b);

            }
            if (line.startsWith("sdef")) {
                int width = 0;
                String[] arrStr = line.split(" ");
                for (int i = 0; i < arrStr.length; i++) {
                    if (!arrStr[i].contains(":")) {
                        continue;
                    }
                    String[] parts = arrStr[i].split(":");
                    String value = parts[1];
                    if (arrStr[i].startsWith("symbol")) {
                        spacerSymbol = value.charAt(0);
                    }
                    if (arrStr[i].startsWith("width")) {
                        width = Integer.parseInt(value);
                    }
                }
                if (width != 0) {
                    spacermap.put(spacerSymbol, width);
                }
            }

        }

        return new BlocksFromSymbolsFactory(spacermap, blockmap);
    }

}
