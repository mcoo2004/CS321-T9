/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.example.hotel;

import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.stage.Stage;



public class GuestController implements Initializable {
    
    private Stage stage;
    private Scene scene;
    private Parent root;
    private Parent homeRoot;
    public void setHomeRoot(Parent preRoot){this.homeRoot=preRoot;}
    
    private Parent resultRoot;
    public void setResultRoot(Parent resultRoot){this.resultRoot=resultRoot;}
    //first name
    @FXML
    private TextField firstname = new TextField();
    //last name
    @FXML
    private TextField lastname = new TextField();
    //email
    @FXML
    private TextField email = new TextField();
    //phone number
    @FXML
    private TextField phonenumber = new TextField();
    
    
    @FXML
    public String selected;
    public void setSelected(String s){selected =s;System.out.println(selected);}
    
    public String checkIn,checkOut;
    public int hotelNumber;
    public void recieveDatesAndHotel(String in, String out,int hotelNum){checkIn=in;checkOut=out;hotelNumber=hotelNum;System.out.println(in+"\n"+out+"\n"+hotelNumber);}
    
    
    public void AddResToDataBase(){
        int hotelNo,roomNo;
        long guestNo;
        //pass check in and check out as strings from filters
        guestNo = Long.parseLong(phonenumber.getText());
        hotelNo=hotelNumber;
        roomNo = Integer.parseInt(selected.substring(0 , selected.indexOf("\n")));
        App app = new App();
        app.addRes(guestNo, hotelNo, roomNo, checkIn, checkOut);
    }
    
    
    
    
    
    @FXML
    public void AddGuestToDataBase(){
        App app = new App();
        app.insert(firstname.getText(), lastname.getText(), email.getText(), phonenumber.getText());
        }
    
    @FXML
    private void switchToResults(ActionEvent event) throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("results.fxml"));
        resultRoot = loader.load();
        ResultsController resultController = new ResultsController();
        resultController.refreshList();
        resultController.refreshList();
        stage=(Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(resultRoot);
        stage.setScene(scene);
        stage.show();
    }
    public void switchToConfirmation(ActionEvent event) throws IOException{
        String s = firstname.getText()+" "+lastname.getText()+"\n "+email.getText()+"\n "+phonenumber.getText();
        AddGuestToDataBase();
        FXMLLoader loader = new FXMLLoader(getClass().getResource("confirmation.fxml"));
        root = loader.load();
        ConfirmationController confirmationController = loader.getController();
        confirmationController.setHomeRoot(homeRoot);
        confirmationController.setLabel("Your Information: "+s);
        AddResToDataBase();
        stage=(Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }
    @Override
    public void initialize(URL arg0, ResourceBundle arg1) {
        /*something goes here */
    }
} 
