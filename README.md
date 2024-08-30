# RedBricks - FastAPI Tweet Sentiment Analysis

This project is a FastAPI application for predicting tweet sentiment using a pre-trained LSTM model. It provides an API endpoint where you can input a tweet and get its predicted sentiment.

## Features

- **API Endpoint**: Accepts a tweet text and returns the predicted sentiment.
- **LSTM Model**: Uses a TensorFlow LSTM model to classify sentiments.
- **Deployment**: The application is deployed on Koyeb, allowing easy access and testing.
- **CI/CD Pipeline**: Automated deployment with GitHub Actions when changes are pushed to the repository.

## Deployed Application

The application is deployed and accessible at: [Koyeb Deployment Link](http://thirsty-estrella-redbricks-47ee49d8.koyeb.app/).

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```
### 2. Install Dependencies

Ensure you have Python 3.7+ installed. Then, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

To run the application locally, use:

```bash
uvicorn main:app --reload
```

Replace `main:app` with the appropriate module and app name if different.

### 4. Access the API Documentation

Once the application is running, navigate to http://127.0.0.1:8000/docs to access the interactive API documentation powered by Swagger UI.

## API Endpoint

- POST /predict-sentiment: Predicts the sentiment of a given tweet.

Request Example:

```bash
{
  "tweet": "It's a great day!"
}
```

Response Example:
```bash
{
  "sentiment": "Happy"
}
```

## Deployment on Koyeb
1. Create a Koyeb Account: If you haven't already, create an account on [Koyeb](https://app.koyeb.com/).
2. Deploy from GitHub: Connect your GitHub repository and select the FastAPI application repository.
3. Setup Build and Deployment: Koyeb will automatically detect your FastAPI application and create a build. Configure environment variables and any required secrets.
4. Access the Deployed Application: Once deployed, you can access your FastAPI app using the provided Koyeb URL.

## CI/CD Pipeline

This project is integrated with a CI/CD pipeline using GitHub Actions. The pipeline includes:

- Linting and Formatting: Ensures code quality and consistency.
- Testing: Runs sample tests to ensure functionality.
- Deployment: Automatically deploys to Koyeb upon successful testing.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [Koyeb](https://app.koyeb.com/) for the hosting platform.




