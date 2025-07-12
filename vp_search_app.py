import streamlit as st
import sys
import os
import dotenv

from VectorizationService import VectorizationService
from VPExperimentPersonService import VPExperimentPersonService

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize services
@st.cache_resource
def init_services():
    """Initialize the vectorization and database services."""
    try:
        vectorizer = VectorizationService(api_key=OPENAI_API_KEY)
        db_service = VPExperimentPersonService()
        return vectorizer, db_service
    except Exception as e:
        st.error(f"Error initializing services: {e}")
        return None, None

def perform_search(department, vectorizer, db_service):
    """Perform the semantic search synchronously."""
    try:
        # Create the search query
        search_query = f"Vice President {department}"
        
        # Vectorize the search query
        with st.spinner("Vectorizing search query..."):
            query_vector = vectorizer.get_embedding(search_query)
        
        if not query_vector:
            st.error("Failed to create vector embedding for the search query.")
            return []
        
        # Perform semantic search
        with st.spinner("Searching for matching VP roles..."):
            results = db_service.semantic_vp_search(
                normalized_role="VP",
                summary_vector=query_vector,
                batch_size=100
            )
        
        return results
    
    except Exception as e:
        st.error(f"Error during search: {e}")
        return []

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="VP Role Search",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 VP Role Semantic Search")
    st.markdown("Search for Vice President roles by department using AI-powered semantic matching.")
    
    # Initialize services
    vectorizer, db_service = init_services()
    
    if vectorizer is None or db_service is None:
        st.error("Failed to initialize services. Please check your configuration.")
        return
    
    # Create the input form
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.text_input(
                "Role",
                value="Vice President",
                disabled=True,
                help="This field is fixed and cannot be changed"
            )
        
        with col2:
            department = st.text_input(
                "Department",
                placeholder="e.g., Sales, Marketing, Operations, Technology...",
                help="Enter the department or area you want to search for"
            )
        
        search_button = st.form_submit_button("🔍 Search", type="primary")
    
    # Perform search when button is clicked
    if search_button:
        if not department.strip():
            st.warning("Please enter a department to search for.")
            return
        
        # Run the synchronous search
        results = perform_search(department, vectorizer, db_service)
        
        if not results:
            st.info("No matching VP roles found for your search.")
            return
        
        # Display results
        st.success(f"Found {len(results)} matching VP roles:")
        
        # Create a nice display of results
        for i, person in enumerate(results, 1):
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.markdown(f"**{person['personName']}**")
                
                with col2:
                    st.markdown(f"*{person['personRole']}*")
                
                with col3:
                    # Create a color-coded similarity score
                    score = person['cosineScore']
                    if score >= 0.8:
                        st.markdown(f"🟢 **{score:.3f}**")
                    elif score >= 0.6:
                        st.markdown(f"🟡 **{score:.3f}**")
                    else:
                        st.markdown(f"🔴 **{score:.3f}**")
                
                # Add a subtle separator
                if i < len(results):
                    st.markdown("<hr style='margin: 10px 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        # Add a summary
        st.markdown("---")
        avg_score = sum(person['cosineScore'] for person in results) / len(results)
        st.markdown(f"**Search Summary:** {len(results)} results found with average similarity score of {avg_score:.3f}")
        
        # Add score legend
        with st.expander("📊 Understanding Similarity Scores"):
            st.markdown("""
            **Similarity Score Legend:**
            - 🟢 **0.8 - 1.0**: Excellent match (highly relevant)
            - 🟡 **0.6 - 0.8**: Good match (moderately relevant)
            - 🔴 **0.0 - 0.6**: Fair match (somewhat relevant)
            
            Higher scores indicate better semantic similarity between your search and the VP role.
            """)

if __name__ == "__main__":
    main() 