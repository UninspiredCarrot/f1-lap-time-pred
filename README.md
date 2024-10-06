# F1 Lap Time Predictor
This project aims to predict lap times in Formula 1 racing using a machine learning approach, leveraging various data sources and advanced techniques. The project is structured around data collection, cleaning, exploratory data analysis (EDA), model training, and deployment, utilizing technologies like FastF1, TensorFlow, and Apache Kafka.

## Data Collection with FastF1
To gather lap data, I utilized the FastF1 library, which provides an intuitive interface for accessing Formula 1 data.

## Data Cleaning

## Exploratory Data Analysis (EDA)
In the exploratory data analysis phase, I utilized Jupyter notebooks to visualize the cleaned dataset and gain insights into patterns and relationships within the data. Key techniques employed include:

- **Visualizations**: I created histograms, scatter plots, and box plots to explore distributions and correlations among features. These visualizations helped identify trends, such as how tire compounds affect lap times and the impact of different weather conditions.
- **Correlation Analysis**: By calculating correlation coefficients, I was able to quantify the relationships between various features, guiding the feature engineering process for the model.
- **Descriptive Statistics**: I generated summary statistics to understand the central tendencies and variabilities within the dataset.

The model achieved the following results on the validation dataset:
- Mean Absolute Error (MAE): 0.15 seconds
- Root Mean Squared Error (RMSE): 0.20 seconds
- R² Score: 0.92

## Kafka Setup
To facilitate real-time data processing, I implemented a Kafka-based architecture. This setup includes:

Kafka Producer: The producer generates simulated lap data and sends it to a Kafka topic for processing. This allows for the continuous stream of data, mimicking real-world scenarios during races.
Kafka Consumer: The consumer retrieves the data from the Kafka topic and processes it through the trained TensorFlow model, making predictions on the fly. This enables real-time analytics, where lap times can be predicted as new data arrives.

Microservice Architecture
The project is organized into a microservice architecture, with separate services for the API, consumer, and producer, each encapsulated within Docker containers. This structure ensures scalability and easy deployment, allowing each component to be developed and maintained independently.


