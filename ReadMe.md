# OH Band Prototype

This repository contains the code base of a prototype OH Band. An OH band is a wristband wearable device which detects the hand motions of the users and determines if they are washing the hands correctly. These are especially used in hospitals and other organizations where the sanitary habits of the employees are important details. The demonstration of this project can be found in [my website](https://avishkaperera.vercel.app/projects/oh-band).

The prototype is implemented on an [Arduino Nano 33 BLE](https://store.arduino.cc/products/arduino-nano-33-ble) development board. This used components of this board were the acceleromoter, gyroscope, and the nRF52840 SoC. A neural network is constantly executing in this SoC which feeds on the six inputs from the above two sensors while producing predictions at 1 Hz rate. The neural network differentiates the user's gestures between 9 unique hand movements and 'other'.

The neural network was developed and trained with [TensorFlow](https://www.tensorflow.org) and [Keras](https://keras.io/) in python while it was deployed in the micro controller with [TensorFlow lite](https://www.tensorflow.org/lite). The model was implemented as a Dense neural network because TensorFlow lite dose not support multiple subgraphs, which are encountered in LSTM layers at the time of this project.

## Implementation

The implementation is based on three steps.

1. Data collection
2. Model development and training
3. Inferencing

A GUI application was developed to collect data and for inference.

The file structure of this repository is decribed below.

-   `data`: The section which generates data from the microcontroller and saves data in the computer
    -   `generate-data`: Generate the data from the microcontroler at the maximum sampling rate of the sensors and prints to the serial bus.
    -   `capture-data.ipynb`: Captures the data from the computer through the serial bus (COM3 port). This functionality is also implemented in the GUI application.
    -   `exports`: Exported raw datasets. contains two sets: 1) each class sampled throughout 30 seconds; 2) each class sampled throughout 60 seconds.
-   `ohband-model`: The model implemented in python and the converted model for the microcontroller in C++.
    -   `microcontroller`
    -   `python`
-   `ui-application`: The application which listens to the data from the microcontroller during both dataset creation stage and inferencing stage
    -   `src`: Self contained python application
    -   `ohband-app.ipynb`: The scripts used to develop the above self contained application.
