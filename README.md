# UPSC Essay Rating API

A Flask-based API for evaluating essays using Google's Gemini AI model. This API provides comprehensive feedback on language quality, analysis depth, and clarity of thought.

## Features

- **Language Quality Evaluation**: Assesses grammar, vocabulary, and writing style
- **Analysis Depth Evaluation**: Evaluates the depth and quality of analysis
- **Clarity of Thought Evaluation**: Assesses the clarity and coherence of ideas
- **Overall Feedback**: Provides comprehensive summary feedback
- **Scoring System**: Individual scores for each criterion and average score

## API Endpoints

### POST /evaluate

Evaluates an essay and returns detailed feedback.

**Request Body:**

```json
{
  "essay": "Your essay text here..."
}
```

**Response:**

```json
{
  "language_feedback": "Feedback on language quality...",
  "analysis_feedback": "Feedback on analysis depth...",
  "clarity_feedback": "Feedback on clarity of thought...",
  "overall_feedback": "Comprehensive summary feedback...",
  "individual_score": [8, 7, 9],
  "avg_score": 8.0
}
```

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "message": "UPSC Essay Rating API is running"
}
```

## Deployment on Vercel

### Prerequisites

1. A Google AI API key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))
2. A GitHub account
3. A Vercel account

### Steps

1. **Push to GitHub:**

   ```bash
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git push origin main
   ```

2. **Deploy on Vercel:**

   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect it as a Python project

3. **Set Environment Variables:**

   - In your Vercel project settings, go to "Environment Variables"
   - Add: `GOOGLE_API_KEY` with your Google AI API key
   - Redeploy the project

4. **Access Your API:**
   - Your API will be available at: `https://your-project-name.vercel.app`
   - Use this URL in your frontend application

### Frontend Integration

Use the following URL in your frontend to communicate with the API:

```
https://your-project-name.vercel.app/evaluate
```

**Example Frontend Code (JavaScript):**

```javascript
const evaluateEssay = async (essayText) => {
  try {
    const response = await fetch(
      "https://your-project-name.vercel.app/evaluate",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ essay: essayText }),
      }
    );

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error evaluating essay:", error);
    throw error;
  }
};
```

## Local Development

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   Create a `.env` file with:

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Project Structure

```
├── app.py              # Main Flask application
├── EssayRating.py      # Essay evaluation workflow
├── wsgi.py            # WSGI entry point for Vercel
├── vercel.json        # Vercel configuration
├── requirements.txt   # Python dependencies
├── env.example       # Environment variables template
└── README.md         # This file
```

## Dependencies

- Flask: Web framework
- LangGraph: Workflow orchestration
- LangChain: LLM framework
- Google Generative AI: AI model integration
- Flask-CORS: Cross-origin resource sharing
