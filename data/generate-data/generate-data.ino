#include <Arduino_LSM9DS1.h>

const double gThreshold = 2;     // Samples if the threshold of 2 G's is exceeded
const int samplingRate = 119;    // Default sampling rate of the IMU
const int guestureDuration = 60; // guesture duration in seconds
const int intervalDuration = 3;  // time between guestures
const int samplesPerGesture = samplingRate * guestureDuration;

int sampleRead = samplesPerGesture;

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  if (!IMU.begin())
  {
    Serial.println("Failed to initialize IMU");
    while (true)
      ;
  }
}

void loop()
{
  Serial.println("################################");
  for (int i = 0; i < intervalDuration; i++)
  {
    Serial.print("# ");
    Serial.println(i + 1);
    delay(1000);
  }
  Serial.println("################################");

  float aX,
      aY, aZ, gX, gY, gZ; // Variables to hold IMU data
  sampleRead = 0;
  while (sampleRead <= samplesPerGesture)
  {

    // check if both new acceleration and gyroscope data is
    // available
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable())
    {
      // read the acceleration and gyroscope data
      IMU.readAcceleration(aX, aY, aZ);
      IMU.readGyroscope(gX, gY, gZ);

      sampleRead++;

      // print the data in CSV format
      Serial.print(aX, 3);
      Serial.print(',');
      Serial.print(aY, 3);
      Serial.print(',');
      Serial.print(aZ, 3);
      Serial.print(',');
      Serial.print(gX, 3);
      Serial.print(',');
      Serial.print(gY, 3);
      Serial.print(',');
      Serial.print(gZ, 3);
      Serial.println();
    }
  }
}
