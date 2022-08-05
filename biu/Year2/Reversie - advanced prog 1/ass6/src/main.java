import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class main extends Application {

    /* the main function show the main manu.
     * and operate the game.
     * */
    public void start(Stage primaryStage) throws Exception {

        //set background
        Image img = new Image("file:reversiBG.jpg", false);
        ImageView iv = new ImageView();
        iv.setImage(img);
        primaryStage.setTitle("Reversi");         //set window

        //set menu buttons
        Button start = new Button("Start Game");
        Button settings = new Button("Settings");
        Button exit = new Button("Exit");
        start.setMaxWidth(150);
        settings.setMaxWidth(150);
        exit.setMaxWidth(150);

        /*when pressed start
          starting the game and restarting the gui board
         */
        start.setOnAction(event -> {
            startGame(primaryStage);
        });

        //user wishes to exit the game...
        exit.setOnAction(event -> {
            primaryStage.close();
        });

        /*when user pressing the settings button opens the settings menu
          and showing it to user.
         */
        settings.setOnAction(event -> {
            settingsPress(primaryStage,start,settings,exit);
        });

        //setting menu with vbox
        VBox vbox = new VBox();
        vbox.getChildren().addAll(start); // button will be left of text
        vbox.getChildren().addAll(settings); // button will be left of text
        vbox.getChildren().addAll(exit); // button will be left of text
        vbox.setSpacing(10);
        vbox.setPadding(new Insets(55, 0, 50, 150));

        //add elements to stackPane layout
        StackPane stackPane = new StackPane();
        stackPane.getChildren().addAll(iv, vbox);

        //show scene
        Scene mainScene = new Scene(stackPane, 460, 215);
        primaryStage.setScene(mainScene);
        primaryStage.show();


    }

    public void settingsPress(Stage primaryStage,Button start,Button settings,Button exit) {
        //the image
        Image img = new Image("file:reversiBG.jpg", false);
        ImageView iv = new ImageView();
        iv.setImage(img);

        //set lables
        Label colorFirstLabel = new Label("Enter first player color: ");
        colorFirstLabel.setFont(new Font("Arial", 20));
        colorFirstLabel.setTextFill(Color.WHITE);
        Label colorSecondLabel = new Label("Enter second player color: ");
        colorSecondLabel.setFont(new Font("Arial", 20));
        colorSecondLabel.setTextFill(Color.WHITE);
        Label boardSizeLable = new Label("Enter the size of the board: ");
        boardSizeLable.setFont(new Font("Arial", 20));
        boardSizeLable.setTextFill(Color.WHITE);

        //set color pickers
        HBox box1 = new HBox();
        box1.setSpacing(20);
        box1.setPadding(new Insets(5, 5, 5, 5));
        ColorPicker colorPicker1 = new ColorPicker();
        colorPicker1.setMaxWidth(50);
        colorPicker1.setMaxHeight(20);
        colorPicker1.setValue(Color.CORAL);
        box1.getChildren().addAll(colorSecondLabel, colorPicker1);
        HBox box2 = new HBox();
        box2.setPadding(new Insets(5, 5, 5, 5));
        ColorPicker colorPicker2 = new ColorPicker();
        colorPicker2.setMaxWidth(50);
        colorPicker2.setMaxHeight(20);
        colorPicker2.setValue(Color.BLUE);
        box2.getChildren().addAll(colorFirstLabel, colorPicker2);

        //set board size
        HBox box3 = new HBox();
        box3.setSpacing(10);
        box3.setPadding(new Insets(5, 5, 5, 5));
        TextField textField = new TextField("8");
        textField.setMaxHeight(20);
        textField.setMaxWidth(50);
        box3.getChildren().addAll(boardSizeLable, textField);
        //main button
        Button back = new Button("press to main menu");

        //set all colors choices and buttons
        VBox colors = new VBox();
        colors.getChildren().addAll(box1, box2, box3,back);
        colors.setSpacing(10);

        //saving the settings before return to menu
        back.setOnAction(event1 -> {
            //write to file
            OutputStreamWriter settingsWriter = null;
            try {
                File settingsFile = new File("settings.txt");
                settingsWriter = new OutputStreamWriter(new FileOutputStream(settingsFile));

                settingsWriter.write(colorPicker1.getValue() + "\n");
                settingsWriter.write(colorPicker2.getValue() + "\n");
                try {
                    if (Integer.parseInt(textField.getText()) > 20 || Integer.parseInt(textField.getText()) < 4) {
                        Alert alert = new Alert(Alert.AlertType.INFORMATION);
                        alert.setTitle("Settings");
                        alert.setHeaderText("Wrong Settings");
                        alert.setContentText("You enter wrong size of board(4-20 only)" +
                                "\nI put 8 as default");
                        alert.show();
                        settingsWriter.write(8 + "");
                    } else {
                        settingsWriter.write(textField.getText() + "");
                    }
                }catch (Exception exception) {
                    Alert alert = new Alert(Alert.AlertType.INFORMATION);
                    alert.setTitle("Settings");
                    alert.setHeaderText("Wrong Settings");
                    alert.setContentText("You enter wrong size of board(4-20 only)" +
                            "\nI put 8 as default");
                    alert.show();
                    settingsWriter.write(8 + "");
                }

            } catch (IOException e) {
                System.out.println("Error writing to file");
            }
            if (settingsWriter != null) {
                try {
                    settingsWriter.close();
                } catch (IOException e) {
                    System.out.println("Error closing the file");
                }
            }
            //setting the main menu scene for return
            VBox v = new VBox();
            //set menu buttons

            v.getChildren().addAll(start, settings, exit); // button will be left of text
            v.setSpacing(10);
            v.setPadding(new Insets(55, 0, 50, 150));
            StackPane p = new StackPane();
            p.getChildren().addAll(iv, v);
            primaryStage.setScene(new Scene(p, 460, 215));
        });

        StackPane sp = new StackPane();
        sp.getChildren().addAll(iv, colors); //add all to stack
        primaryStage.setScene(new Scene(sp, 460, 215));
    }

    /**
     * Called when pressing start button.
     * @param primaryStage main stage
     */
    public void startGame(Stage primaryStage) {

        //setting labels and button
        Label label = new Label();
        label.setTranslateY(-300);
        label.setTranslateX(650);
        Label gameStatus = new Label("In Game");
        gameStatus.setTranslateY(-270);
        gameStatus.setTranslateX(650);
        gameStatus.setFont(new Font("Arial", 16));
        Label firstScore = new Label();
        firstScore.setTranslateY(-250);
        firstScore.setTranslateX(650);
        firstScore.setFont(new Font("Arial", 16));
        Label secScore = new Label();
        secScore.setTranslateY(-230);
        secScore.setTranslateX(650);
        secScore.setFont(new Font("Arial", 16));

        //setting the game classes
        GuiBoard guiBoard = new GuiBoard(label);
        guiBoard.setPrefWidth(626);
        guiBoard.setPrefHeight(626);
        int size = guiBoard.getSettings();
        CellManger cellManger = new CellManger(size);
        cellManger.setWhite(size/2, size/2);
        cellManger.setWhite(size/2+1, size/2+1);
        cellManger.setBlack(size/2, size/2+1);
        cellManger.setBlack(size/2+1, size/2);
        Player p1 = new GuiPlayer('x');
        Player p2 = new GuiPlayer('o');
        Rule r = new ReverseRule();
        Player[] players = new Player[2];
        players[0] = p1;
        players[1] = p2;
        GameFlow gameFlow = new GameFlow(cellManger, r, players, size, gameStatus, firstScore, secScore);
        guiBoard.setGameFlow(gameFlow);

        //setting stage and scene
        GridPane g = new GridPane();
        g.getChildren().addAll(label, guiBoard, gameStatus, firstScore, secScore);
        primaryStage.setScene(new Scene(g, 626 + 250, 626));

        guiBoard.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
