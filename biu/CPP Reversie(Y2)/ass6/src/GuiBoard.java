import javafx.fxml.FXMLLoader;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import org.w3c.dom.css.Rect;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

public class GuiBoard extends GridPane implements GameShower {
    private GameFlow gameFlow;
    private Label label;
    private Color firstColor;
    private Color secondColor;
    private int size;

    /**
     * Gui board constructor
     * @param l turn label
     */
    GuiBoard(Label l) {
        label = l;
        getSettings(); //get settings from file
        //creating fxml file and set GuiBoard as root
        //FXMLLoader fxmlLoader = new FXMLLoader("file:GuiBoard.fxml");
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("GuiBoard.fxml"));
        fxmlLoader.setRoot(this);
        fxmlLoader.setController(this);
        try {
            fxmlLoader.load();
        } catch (IOException exception) {
            throw new RuntimeException(exception);
        }
    }


    /**
     * get the settings from the settings file.
     */
    public int getSettings() {
        BufferedReader bufferedReader = null;
        try {
            File settings = new File("settings.txt");
            bufferedReader = new BufferedReader(new FileReader(settings));
            String data;
            java.awt.Color awtColor;
            //reading first color
            data = bufferedReader.readLine();
            data = data.substring(0, data.length() - 2);
            awtColor = java.awt.Color.decode(data);
            this.firstColor = Color.rgb(awtColor.getRed(), awtColor.getGreen()
                    , awtColor.getBlue(), awtColor.getAlpha() / 255.0);

            //reading second color
            data = bufferedReader.readLine();
            data = data.substring(0, data.length() - 2);
            awtColor = java.awt.Color.decode(data);
            this.secondColor = Color.rgb(awtColor.getRed(), awtColor.getGreen()
                    , awtColor.getBlue(), awtColor.getAlpha() / 255.0);

            //reading size of board
            data = bufferedReader.readLine();
            this.size = Integer.parseInt(data);
        } catch (Exception e) {
            System.out.println("Error settings file not found :)!");
        }
        if (bufferedReader != null) {
            try {
                bufferedReader.close();
            } catch (IOException e) {
                System.out.println("Error closing settings file");
            }
        }
        return size;
    }

    /**
     * @return size of the board
     */
    public int getSize() {
        return gameFlow.getSize();
    }

    /**
     * add the appropriate symbols to our gui
     * (rectangles for the board, and buttons for the player move)
     */
    public void show() {
        this.getChildren().clear();
        int s = (int) this.getHeight();
        int cellSize = s / this.size;
        //int cellSize = s / 8;
        //int size = gameFlow.getSize();
        Cell[][] arr = gameFlow.getCellManger().getArr();

        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                //put blank rectangle
                Rectangle rect = new Rectangle(0, 0, cellSize - 2, cellSize - 2);
                rect.setFill(Color.WHITE);
                rect.setStroke(Color.BLACK);
                this.add(rect, j, i);
                //if it's 'o' cell put rectangle in his color
                if (arr[i][j].symbol == 'o') {
                    Circle circle = new Circle(0, 0, cellSize / 2 - 2);
                    circle.setStroke(Color.BLACK);
                    circle.setFill(this.firstColor);
                    this.add(circle, j, i);
                }
                //if it's 'x' cell put rectangle in his color
                if (arr[i][j].symbol == 'x') {
                    Circle circle = new Circle(0, 0, cellSize / 2 - 2);
                    circle.setStroke(Color.BLACK);
                    circle.setFill(this.secondColor);
                    this.add(circle, j, i);
                }
            }
        }
        //set players colors lables
        Label firstColorLable = new Label("first player color");
        firstColorLable.setFont(new Font("Arial", 16));
        firstColorLable.setMinHeight(40);
        firstColorLable.setMinWidth(160);
        Label secondColorLable = new Label("second player color");
        secondColorLable.setFont(new Font("Arial", 16));
        secondColorLable.setMinHeight(40);
        secondColorLable.setMinWidth(160);
        Rectangle firstRectangle = new Rectangle(10,10,this.firstColor);
        Rectangle secondRectangle = new Rectangle(10,10,this.secondColor);
        HBox hBox1 = new HBox();
        hBox1.getChildren().addAll(firstColorLable, secondRectangle);
        HBox hBox2 = new HBox();
        hBox2.getChildren().addAll(secondColorLable, firstRectangle);
        VBox vBox = new VBox();
        vBox.getChildren().addAll(hBox1, hBox2);
        vBox.setTranslateX(20);
        this.add(vBox, size + 1, size/2 + 1);
    }

    /**
     * set the turn label to the appropriate player
     * @param symbol symbol of the current player
     */
    public void YourTurn(char symbol) {
        label.setFont(new Font("Arial", 16));
        if (symbol == 'x') {
            label.setText("First Player Move!");
        } else {
            label.setText("Second Player Move!");
        }
    }

    /**
     * play the game
     */
    public void play() {
        show(); //add the symbols to the gui
        YourTurn(gameFlow.getCurrentPlayers().getSymbol()); // set turn label
        Cell[][] arr = gameFlow.getCellManger().getArr(); //get board
        List<Button> buttons = new LinkedList<>(); //to allocate all the optional buttons moves
        int s = (int) this.getHeight();

        boolean noMoves = gameFlow.setPossibleMoves(); //"initialize" the board with the correct symbols
        //in case of no moves notify the gameFlow and wait for player to accept
        if (noMoves) {
            gameFlow.next();
            gameFlow.noMoves(true);
            if(gameFlow.getNoMovesCounter()==2){
                this.gameFlow.gameOver(true);
            }
            else {
                Button b = new Button("Press to Continue");
                b.setMinHeight(50);
                b.setMinWidth(150);
                VBox vBox = new VBox();
                vBox.getChildren().add(b);
                this.add(vBox, size + 5, size / 2);
                b.setOnAction(event -> {
                    this.play();
                    this.getChildren().remove(b);
                });
            }
        } else {
            gameFlow.noMoves(false);
        }
        int cellSize = s / this.size;
        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                //optional move and need to put a button in this cell
                if (arr[i][j].symbol == 'z') {
                    //creating button
                    Button button = new Button();
                    button.setMaxHeight(cellSize);
                    button.setMaxWidth(cellSize);
                    buttons.add(button);
                    this.add(button, j, i);
                    button.setOnAction(event -> {
                        boolean continu = false;
                        int row = GridPane.getRowIndex(button);
                        int col = GridPane.getColumnIndex(button);
                        for (Button b : buttons) {
                            this.getChildren().remove(b);
                        }
                        continu = gameFlow.playOneTurn(new Point(row, col));
                        show();
                        clearBoard();
                        if (continu) {
                            this.play();
                        }
                    });

                }
            }
        }

    }

    /*clear board after each move
      so there won't be wrong possible moves
     */
    public void clearBoard() {
        int size = gameFlow.getSize();
        Cell[][] arr = gameFlow.getCellManger().getArr();
        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                if (arr[i][j].symbol == 'z') {
                    arr[i][j].symbol = 'a';

                }
            }
        }
    }

    /**
     * @param g gameFlow
     */
    public void setGameFlow(GameFlow g) {
        gameFlow = g;
    }
}

