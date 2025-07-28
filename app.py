import streamlit as st
import json
import requests # Ensure 'requests' library is installed: pip install requests

# --- Configuration for LLM API Call ---
# IMPORTANT: For actual LLM integration, you would replace this with your API key.
# For Canvas environment, __api_key__ is automatically provided if you use gemini-2.0-flash or imagen-3.0-generate-002
# For other models, you would need to provide an API key here.
API_KEY = "AIzaSyBfxd2tyrLeE0yHKyLWsh_hj6fUmL-h1Ds" # Paste your Google Gemini API Key here if running locally. Obtain it from Google AI Studio.

# --- LLM Call Function ---
def generate_text_with_llm(prompt_text, model_name="gemini-2.0-flash"):
    """
    Calls the Gemini API to generate text based on a prompt using the requests library.
    This function is designed to work within Streamlit's synchronous flow.
    """
    st.info("Generating content with AI... This might take a moment.")
    
    chat_history = []
    # Corrected syntax: "text": prompt_text (colon, not quote after text)
    chat_history.append({ "role": "user", "parts": [{ "text": prompt_text }] }) 
    payload = { "contents": chat_history }

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"

    try:
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        
        result = response.json() # Parse the JSON response directly

        # Check for candidates and content parts
        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            st.success("Content generated!")
            return generated_text
        else:
            st.error("Failed to generate content from LLM. Response structure unexpected.")
            st.json(result) # Show the full response for debugging
            return "Error: Could not generate content."
    except requests.exceptions.RequestException as e:
        st.error(f"Network or API request error: {e}")
        return f"Error: Network or API request failed: {e}"
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response from LLM: {e}")
        return f"Error: Invalid JSON response: {e}"
    except Exception as e:
        st.error(f"An unexpected error occurred during LLM call: {e}")
        return f"Error: {e}"


# --- Resume and Cover Letter Generation Functions (synchronous) ---
def generate_resume_section(section_name, user_data, job_description, model="gemini-2.0-flash"):
    """
    Generates a specific section of the resume using an LLM.
    The prompt is designed to guide the LLM to create relevant content.
    """
    if section_name == "Summary":
        prompt = f"""
        You are an expert resume writer. Write a concise and compelling professional summary (3-4 sentences) for a resume.
        Focus on the user's skills, experience, and career goals, making it highly relevant to the provided job description.

        User's Skills: {user_data.get('skills', 'N/A')}
        User's Experience: {user_data.get('experience', 'N/A')}
        User's Career Goals: {user_data.get('career_goals', 'N/A')}
        Job Role Applying For: {user_data.get('job_role', 'N/A')}
        Job Description: {job_description}

        Ensure the summary highlights key qualifications and aligns with the job's requirements.
        """
    elif section_name == "Experience":
        prompt = f"""
        You are an expert resume writer. For the following user experience, rewrite the bullet points to be achievement-oriented,
        quantifiable where possible, and highly relevant to the provided job description. Use strong action verbs.
        Each bullet point should be concise (1-2 lines).

        User's Experience: {user_data.get('experience', 'N/A')}
        Job Role Applying For: {user_data.get('job_role', 'N/A')}
        Job Description: {job_description}

        Format the output as a list of bullet points.
        """
    elif section_name == "Skills":
        prompt = f"""
        You are an expert resume writer. Based on the user's provided skills and the job description,
        generate a comprehensive list of relevant skills. Categorize them into Technical Skills, Soft Skills, and Tools/Technologies.
        Prioritize skills mentioned in both the user's input and the job description.

        User's Skills: {user_data.get('skills', 'N/A')}
        Job Description: {job_description}

        Format the output clearly with categories.
        """
    elif section_name == "Education":
        prompt = f"""
        You are an expert resume writer. Based on the user's education and the job description,
        format the education section for a resume. Include degree, university, and graduation date.
        If relevant, mention any academic achievements or coursework that aligns with the job.

        User's Education: {user_data.get('education', 'N/A')}
        Job Description: {job_description}

        Format the output professionally.
        """
    else:
        return "Unsupported resume section."

    return generate_text_with_llm(prompt, model) # Call synchronous version

def generate_cover_letter(user_data, job_description, model="gemini-2.0-flash"):
    """
    Generates a personalized cover letter using an LLM.
    The prompt guides the LLM to create a professional and tailored letter.
    """
    prompt = f"""
    You are an expert cover letter writer. Write a professional and personalized cover letter
    for the user applying to the specified job role.
    The letter should be 3-4 paragraphs long, highlighting key skills and experiences
    that directly align with the job description.

    User's Name: {user_data.get('name', 'N/A')}
    User's Email: {user_data.get('email', 'N/A')}
    User's Skills: {user_data.get('skills', 'N/A')}
    User's Experience: {user_data.get('experience', 'N/A')}
    User's Education: {user_data.get('education', 'N/A')}
    User's Career Goals: {user_data.get('career_goals', 'N/A')}

    Job Role Applying For: {user_data.get('job_role', 'N/A')}
    Job Description: {job_description}

    Structure:
    - Paragraph 1: Express enthusiasm, state the role, and briefly mention why they are a great fit.
    - Paragraph 2-3: Elaborate on 2-3 key experiences/skills from the user's profile that directly match the job description. Provide specific examples if the user data allows.
    - Concluding Paragraph: Reiterate interest, call to action (interview), and thank you.

    Maintain a professional and confident tone.
    """
    return generate_text_with_llm(prompt, model) # Call synchronous version

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="AI Resume & Cover Letter Generator")

st.title("📄 AI Resume & Cover Letter Generator")
st.markdown("---")

st.header("1. Your Information")

col1, col2 = st.columns(2)
with col1:
    # Removed default values for user information fields
    user_name = st.text_input("Full Name", "") 
    user_email = st.text_input("Email", "") 
    user_skills = st.text_area("Your Key Skills (comma-separated)", "")
    user_experience = st.text_area("Your Work Experience (brief summary or key achievements)", "")

with col2:
    # Removed default values for user education, career goals, job role, and job description
    user_education = st.text_area("Your Education (Degree, University, Year)", "")
    user_career_goals = st.text_area("Your Career Goals", "")
    job_role = st.text_input("Job Role You're Applying For", "")
    job_description = st.text_area("Full Job Description", "")

user_data = {
    "name": user_name,
    "email": user_email,
    "skills": user_skills,
    "experience": user_experience,
    "education": user_education,
    "career_goals": user_career_goals,
    "job_role": job_role
}

st.markdown("---")
st.header("2. Generate Documents")

def generate_documents_sync():
    if not job_description:
        st.warning("Please provide a Job Description to generate tailored documents.")
        return

    st.session_state['generating'] = True
    st.session_state['resume_content'] = ""
    st.session_state['cover_letter_content'] = ""
    st.session_state['resume_summary'] = ""
    st.session_state['resume_experience'] = ""
    st.session_state['resume_skills'] = ""
    st.session_state['resume_education'] = ""

    with st.spinner("Generating Resume Summary..."):
        st.session_state['resume_summary'] = generate_resume_section("Summary", user_data, job_description)
    
    with st.spinner("Generating Resume Experience..."):
        st.session_state['resume_experience'] = generate_resume_section("Experience", user_data, job_description)
        
    with st.spinner("Generating Resume Skills..."):
        st.session_state['resume_skills'] = generate_resume_section("Skills", user_data, job_description)

    with st.spinner("Generating Resume Education..."):
        st.session_state['resume_education'] = generate_resume_section("Education", user_data, job_description)

    st.session_state['resume_content'] = f"""
# {user_data['name']}
**Email:** {user_data['email']} | **Skills:** {user_data['skills'].split(',')[0]}...

---

## Summary
{st.session_state['resume_summary']}

---

## Experience
{st.session_state['resume_experience']}

---

## Skills
{st.session_state['resume_skills']}

---

## Education
{st.session_state['resume_education']}
"""
    
    with st.spinner("Generating Cover Letter..."):
        st.session_state['cover_letter_content'] = generate_cover_letter(user_data, job_description)

    st.session_state['generating'] = False
    st.rerun()

if st.button("Generate Resume & Cover Letter", type="primary"):
    generate_documents_sync()


st.markdown("---")
st.header("3. Generated Documents")

if 'generating' in st.session_state and st.session_state['generating']:
    st.info("Generation in progress...")
elif 'resume_content' in st.session_state and st.session_state['resume_content']:
    st.subheader("Generated Resume")
    st.markdown(st.session_state['resume_content'])
    
    st.subheader("Generated Cover Letter")
    st.markdown(st.session_state['cover_letter_content'])
else:
    st.info("Fill in your details and click 'Generate' to see your documents.")

st.markdown("---")
st.caption("Powered by Generative AI (LLMs)")