# VP Role Semantic Search Application

This Streamlit application allows users to search for Vice President roles using semantic similarity matching.

## Features

- Search for VP roles by department
- AI-powered semantic matching using OpenAI embeddings
- Real-time similarity scores with color-coded results
- Clean, user-friendly interface

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run vp_search_app.py
   ```

3. Open your web browser and go to `http://localhost:8501`

## How to Use

1. **Role Field**: This is fixed as "Vice President" and cannot be changed
2. **Department Field**: Enter the department or area you want to search for (e.g., "Sales", "Marketing", "Operations", "Technology")
3. **Search Button**: Click to perform the semantic search
4. **Results**: View the matching VP roles with their similarity scores

## Understanding Similarity Scores

- 🟢 **0.8 - 1.0**: Excellent match (highly relevant)
- 🟡 **0.6 - 0.8**: Good match (moderately relevant)  
- 🔴 **0.0 - 0.6**: Fair match (somewhat relevant)

Higher scores indicate better semantic similarity between your search and the VP role.

## Configuration

The application uses the following services:
- OpenAI API for text embeddings
- MongoDB for storing and searching VP data
- Vector search capabilities for semantic matching

Make sure your MongoDB database is properly configured with the vector search index. 