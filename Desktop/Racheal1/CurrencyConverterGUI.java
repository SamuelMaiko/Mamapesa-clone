import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.FileReader;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Locale;
import java.util.ResourceBundle;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

import javax.management.RuntimeErrorException;

public class CurrencyConverterGUI extends Application {
    private JsonObject ratesObject;
    private CustomComboBox sourceCurrencyComboBox;
    private CustomComboBox targetCurrencyComboBox;
    private String lastInputDate;
    private VBox historyVBox;
    private static final Logger logger = Logger.getLogger(CurrencyConverterGUI.class.getName());

    public static void main(String[] args) {
        logger.info("Starting the application.");
         // Determine the user's locale (you can do this dynamically)
         Locale userLocale = Locale.US;
         // Load the appropriate resource bundle
        ResourceBundle bundle = ResourceBundle.getBundle("Messages", Locale.getDefault());
        // Retrieve a message from the bundle
        String applicationName = bundle.getString("application.name");
        String sourcecurrency = bundle.getString("source.currency");

        // You can then use these messages in your application
        System.out.println("Application Name: " + applicationName);
        System.out.println("Source Currency: " + sourcecurrency);
        // Schedule the Python script to run periodically (e.g., every hour)
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(() -> runPythonScript(), 0, 1, TimeUnit.HOURS);
        
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            // Perform cleanup tasks here
            logger.info("Shutting down the application.");
        }));
        // Launch the JavaFX application
        launch(args);

    }

    // Add this method to run the Python script
    private static void runPythonScript() {
        try {
            String pythonScript = "python";  // Modify this if your Python interpreter has a different name
            String scriptPath = "fetch_currency_rates.py";  // Provide the correct path to your Python script

            ProcessBuilder processBuilder = new ProcessBuilder(pythonScript, scriptPath);
            Process process = processBuilder.start();

            // Wait for the Python script to complete
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println("Python script executed successfully.");
            } else {
                System.err.println("Error running Python script. Exit code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Currency Converter");


        try {
            loadExchangeRateData("currency_rates.json"); // Load data from a provided JSON file
        } catch (IOException e) {
            showAlert("Error", "Failed to read currency rates file: " + e.getMessage());
            return;
        }

        // GUI components
        BorderPane borderPane = new BorderPane();
        sourceCurrencyComboBox = new CustomComboBox();
        targetCurrencyComboBox = new CustomComboBox();
        TextField amountTextField = new TextField();
        Label resultLabel = new Label();

        // Creating a VBox to hold history
        VBox vbox1 = new VBox();

        // Fill sourceCurrencyComboBox and targetCurrencyComboBox from ratesObject
        Set<Map.Entry<String, JsonElement>> entries = ratesObject.entrySet();
        for (Map.Entry<String, JsonElement> entry : entries) {
            sourceCurrencyComboBox.getItems().add(entry.getKey());
            targetCurrencyComboBox.getItems().add(entry.getKey());
        }

        Button convertButton = new Button("Convert");
        convertButton.setOnAction(e -> {
            String sourceCurrency = sourceCurrencyComboBox.getValue();
            String targetCurrency = targetCurrencyComboBox.getValue();
            double amount;

            try {
                amount = Double.parseDouble(amountTextField.getText());
            } catch (NumberFormatException ex) {
                showAlert("Invalid Input", "Please enter a valid numeric amount.");
                return;
            }

            if (ratesObject.has(sourceCurrency) && ratesObject.has(targetCurrency)) {
                double sourceToUSD = ratesObject.get(sourceCurrency).getAsDouble();
                double targetToUSD = ratesObject.get(targetCurrency).getAsDouble();
                double conversionRate = targetToUSD / sourceToUSD;
                double convertedAmount = amount * conversionRate;
                resultLabel.setText(amount + " " + sourceCurrency + " is equal to " + convertedAmount + " " + targetCurrency);
                saveToHistory(resultLabel.getText(), historyVBox);
                // Add the result to history
            } else {
                showAlert("Invalid Currency Codes", "Selected currency codes or conversion rates not found.");
            }
            });

         // Create a history section with scroll functionality
         historyVBox = new VBox(10);
         historyVBox.setAlignment(Pos.TOP_LEFT);
         historyVBox.setPrefHeight(200);  // Set the preferred height of the history VBox
         historyVBox.setStyle("-fx-background-color: #F5F5F5; -fx-padding: 10;");
         ScrollPane historyScrollPane = new ScrollPane(historyVBox);
         historyScrollPane.setFitToWidth(true);  // Enable horizontal scrolling
         historyScrollPane.setFitToHeight(true); // Enable vertical scrolling

        Button clearButton = new Button("Clear");
        clearButton.setOnAction(event -> {
            sourceCurrencyComboBox.setValue(null);
            targetCurrencyComboBox.setValue(null);
            amountTextField.setText("");
            resultLabel.setText("");
        });

        // Create and add a button for clearing the history
        Button clearHistoryButton = new Button("Clear History");
        clearHistoryButton.setOnAction(event -> {
            historyVBox.getChildren().clear();
        });

        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(
            new Label("Source Currency:"),
            sourceCurrencyComboBox,
            new Label("Target Currency:"),
            targetCurrencyComboBox,
            new Label("Amount:"),
            amountTextField,
            convertButton,
            clearButton,
            new Label("Result:"),
            resultLabel,
            new Label("Input History:"),
            historyScrollPane,// Add history VBox to the main VBox
            clearHistoryButton // Add the clear history button
        );
        borderPane.setCenter(vbox);

        Scene scene = new Scene(borderPane, 700, 400);
        primaryStage.setScene(scene);
        // Show the primary stage
        primaryStage.show();
    }

    private void loadExchangeRateData(String jsonFilePath) throws IOException {
        try (FileReader reader = new FileReader(jsonFilePath)) {
            JsonElement jsonElement = JsonParser.parseReader(reader);
            JsonObject jsonObject = jsonElement.getAsJsonObject();

            if (jsonObject.has("rates")) {
                ratesObject = jsonObject.getAsJsonObject("rates");
            } else {
                throw new IOException("'rates' field not found in JSON.");
            }
        } catch (IOException e) {
                showAlert("Error", "Failed to read currency rates file: " + e.getMessage());
                throw new IOException("Failed to read currency rates file: " + e.getMessage());
            }
    }

    private void saveToHistory(String result, VBox historyVBox) {
        if (historyVBox.getChildren().size() >= 5) {
            historyVBox.getChildren().remove(0);
        }
    
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy - hh:mm a", Locale.ENGLISH);
        String formattedDateTime = now.format(formatter);
        lastInputDate = formattedDateTime; // Assign the value to lastInputDate
        Label historyEntry = new Label(result);
        Label dateLabel = new Label("As of: " + lastInputDate);
        VBox historyEntryBox = new VBox(historyEntry, dateLabel);
        historyVBox.getChildren().add(historyEntryBox);
    }


    private void showAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private class CustomComboBox extends ComboBox<String> {
        private final TextField editor;
        private ObservableList<String> originalItems;
        private ObservableList<String> filteredItems;

        public CustomComboBox() {
            editor = getEditor();
            setEditable(true);

            editor.textProperty().addListener((observable, oldValue, newValue) -> {
                if (originalItems == null) {
                    originalItems = FXCollections.observableArrayList(getItems());
                }

                if (newValue.isEmpty()) {
                    filteredItems = originalItems;
                } else {
                    filteredItems = originalItems.filtered(item ->
                            item.toLowerCase().contains(newValue.toLowerCase()));
                }
                setItems(filteredItems);

                if (!filteredItems.isEmpty()) {
                    show();
                } else {
                    hide();
                }
            });

            setOnHidden(e -> {
                setItems(originalItems);
                filteredItems = null;
            });

            // Add this part to set the text of the editor when an item is selected
            setOnAction(e -> {
                if (getSelectionModel().getSelectedItem() != null) {
                    editor.setText(getSelectionModel().getSelectedItem());
                }
                hide();
            });
        }
    }
}
