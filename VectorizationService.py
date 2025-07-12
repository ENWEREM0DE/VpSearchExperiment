from openai import OpenAI

class VectorizationService:
    """Handles vectorization of text using OpenAI's API."""
    def __init__(self, api_key: str):
        """
        Initializes the OpenAI client.
        
        Args:
            api_key: Your OpenAI API key.
        """
        if api_key == "YOUR_OPENAI_API_KEY" or not api_key:
            raise ValueError("OpenAI API Key is not configured. Please set it in the script or as an environment variable.")
        self.client = OpenAI(api_key=api_key)

    def get_embedding(self, text: str, model="text-embedding-ada-002") -> list[float]:
        """
        Generates a vector embedding for a given text string.
        
        Args:
            text: The text to vectorize.
            model: The OpenAI embedding model to use.
            
        Returns:
            A list of floats representing the vector embedding.
        """
        try:
            text = text.replace("\n", " ")
            response = self.client.embeddings.create(input=[text], model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"An error occurred while getting embedding for '{text}': {e}")
            return None