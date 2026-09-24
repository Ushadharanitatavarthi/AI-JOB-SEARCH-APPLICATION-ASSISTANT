# import streamlit as st
# from pypdf import PdfReader
# import requests



# # -----------------------------
# # CLOUD AI (Gemini)
# # -----------------------------

# def generate_ai(prompt):
#     """Generate text with Gemini through the REST API."""
#     api_key = st.secrets.get("GEMINI_API_KEY")
#     if not api_key:
#         raise RuntimeError(
#             "GEMINI_API_KEY is missing. Add it in Streamlit Cloud Secrets."
#         )

#     url = (
#         "https://generativelanguage.googleapis.com/v1beta/"
#         "models/gemini-3.5-flash-lite:generateContent"
#     )

#     response = requests.post(
#         url,
#         headers={
#             "x-goog-api-key": api_key,
#             "Content-Type": "application/json",
#         },
#         json={
#             "contents": [
#                 {
#                     "parts": [
#                         {"text": prompt}
#                     ]
#                 }
#             ]
#         },
#         timeout=60,
#     )

#     if response.status_code != 200:
#         try:
#             error_detail = response.json().get("error", {}).get("message", response.text)
#         except Exception:
#             error_detail = response.text
#         raise RuntimeError(
#             f"Gemini API error ({response.status_code}): {error_detail}"
#         )

#     data = response.json()
#     try:
#         return data["candidates"][0]["content"]["parts"][0]["text"]
#     except (KeyError, IndexError, TypeError):
#         raise RuntimeError("Gemini returned an unexpected response.")

# st.set_page_config(
#     page_title="AI Job Search Assistant",
#     page_icon="💼",
#     layout="wide"
# )

# st.title("💼 AI Job Search & Application Assistant")
# st.write("Upload your resume to find private and government job opportunities.")

# if "job_data" not in st.session_state:
#     st.session_state.job_data = []

# if "job_categories" not in st.session_state:
#     st.session_state.job_categories = {}

# if "resume_analysis" not in st.session_state:
#     st.session_state.resume_analysis = ""

# if "resume_text" not in st.session_state:
#     st.session_state.resume_text = ""

# if "application_result" not in st.session_state:
#     st.session_state.application_result = ""

# if "selected_job" not in st.session_state:
#     st.session_state.selected_job = None

# st.subheader("📄 Upload Your Resume")

# resume = st.file_uploader(
#     "Choose your resume PDF",
#     type=["pdf"],
#     key="resume_uploader"
# )

# if resume is not None:
#     st.success("Resume uploaded successfully! ✅")

#     try:
#         reader = PdfReader(resume)
#         resume_text = ""

#         for page in reader.pages:
#             text = page.extract_text()
#             if text:
#                 resume_text += text + "\n"

#         resume_text = resume_text.strip()
#         st.session_state.resume_text = resume_text

#     except Exception as e:
#         st.error(f"Could not read the resume: {e}")
#         st.stop()

#     if resume_text:
#         st.subheader("📃 Resume Content")

#         st.text_area(
#             "Extracted Resume Text",
#             resume_text,
#             height=250
#         )

#         st.subheader("🧠 AI Resume Analysis")

#         if st.button("Analyze Resume", key="analyze_resume"):
#             with st.spinner("Gemini is analyzing your resume..."):
#                 prompt = f"""
# You are an AI Resume Analysis Assistant.

# Analyze the following resume.

# Extract:

# 1. Name
# 2. Education
# 3. Technical Skills
# 4. Soft Skills
# 5. Projects
# 6. Internships / Experience
# 7. Certifications
# 8. Suggested Job Roles

# Also mention important skills that appear to be missing
# for the suggested job roles.

# Do not invent information that is not present in the resume.

# Give the answer in a clear and professional format.

# RESUME:
# {resume_text}
# """

#                 try:
#                     response = generate_ai(prompt)

#                     analysis = response["message"]["content"]
#                     st.session_state.resume_analysis = analysis

#                     st.success("Resume analysis completed! ✅")

#                 except Exception as e:
#                     st.error(f"Ollama error: {e}")

#         if st.session_state.resume_analysis:
#             st.text_area(
#                 "AI Analysis",
#                 st.session_state.resume_analysis,
#                 height=450
#             )

# st.divider()

# st.subheader("🚀 Explore Opportunities")

# tab_private, tab_government, tab_freelance, tab_application = st.tabs(
#     [
#         "🔎 Private Jobs",
#         "🏛️ Government Jobs",
#         "🌐 Freelancing",
#         "✉️ AI Application"
#     ]
# )

# # =========================================================
# # TAB 1: PRIVATE JOBS
# # =========================================================

# with tab_private:

#     st.subheader("🔎 Find Jobs Based on Your Resume")

#     st.write(
#         "We'll use your resume skills, education, projects, "
#         "and experience to find different private job opportunities."
#     )

#     if not st.session_state.resume_text:
#         st.warning("⚠️ Please upload your resume first.")

#     else:

#         if st.button(
#             "🔎 Find Jobs For Me",
#             key="find_private_jobs"
#         ):

#             with st.spinner(
#                 "Analyzing your resume and searching for suitable jobs..."
#             ):

#                 try:
#                     APP_ID = st.secrets["ADZUNA_APP_ID"]
#                     APP_KEY = st.secrets["ADZUNA_APP_KEY"]

#                     resume_for_search = (
#                         st.session_state.resume_text[:12000]
#                     )

#                     prompt = f"""
# You are a job-search assistant.

# Read the following resume and identify broad job-search
# keywords that are suitable for this candidate.

# Resume:
# {resume_for_search}

# Return ONLY 6 short job-search queries.

# Rules:
# - Do not return full sentences.
# - Do not return explanations.
# - Include different suitable job areas.
# - Consider technical skills, projects, education and fresher eligibility.
# - Do not focus on only one programming language.
# - Do not invent skills that are not present in the resume.

# Example format:

# Python developer
# Software developer
# Web developer
# QA tester
# Technical support
# Graduate software jobs
# """

#                     ai_response = generate_ai(prompt)

#                     search_text = ai_response["message"]["content"]

#                     search_queries = []

#                     for line in search_text.splitlines():
#                         line = line.strip()

#                         if not line:
#                             continue

#                         line = line.lstrip("-•*0123456789. ")

#                         if line:
#                             search_queries.append(line)

#                     search_queries = list(
#                         dict.fromkeys(search_queries)
#                     )

#                     search_queries = search_queries[:6]

#                     if not search_queries:
#                         st.error(
#                             "Could not generate job searches from the resume."
#                         )

#                     else:

#                         st.info(
#                             "Searching across multiple job areas: "
#                             + ", ".join(search_queries)
#                         )

#                         all_jobs = []

#                         url = (
#                             "https://api.adzuna.com/"
#                             "v1/api/jobs/in/search/1"
#                         )

#                         for query in search_queries:

#                             params = {
#                                 "app_id": APP_ID,
#                                 "app_key": APP_KEY,
#                                 "results_per_page": 10,
#                                 "what": query,
#                                 "where": "India",
#                                 "content-type": "application/json"
#                             }

#                             response = requests.get(
#                                 url,
#                                 params=params,
#                                 timeout=30
#                             )

#                             if response.status_code == 200:

#                                 data = response.json()

#                                 jobs = data.get(
#                                     "results",
#                                     []
#                                 )

#                                 all_jobs.extend(jobs)

#                             elif response.status_code == 429:

#                                 st.warning(
#                                     "⚠️ Adzuna API rate limit "
#                                     "was reached while searching. "
#                                     "Some searches may be missing."
#                                 )

#                                 break

#                             else:

#                                 st.warning(
#                                     f"Adzuna search failed "
#                                     f"for '{query}' "
#                                     f"(HTTP {response.status_code})"
#                                 )

#                         unique_jobs = []
#                         seen_jobs = set()

#                         for job in all_jobs:

#                             job_id = str(
#                                 job.get("id", "")
#                             )

#                             if (
#                                 job_id
#                                 and job_id not in seen_jobs
#                             ):

#                                 seen_jobs.add(job_id)
#                                 unique_jobs.append(job)

#                         unique_jobs = unique_jobs[:30]

#                         st.session_state.job_data = unique_jobs
#                         st.session_state.job_categories = {}

#                         if unique_jobs:

#                             st.success(
#                                 f"{len(unique_jobs)} "
#                                 "different private jobs found! ✅"
#                             )

#                         else:

#                             st.warning(
#                                 "No jobs were found. "
#                                 "Try again later or check your Adzuna API credentials."
#                             )

#                 except Exception as e:

#                     st.error(
#                         f"Could not search for jobs: {e}"
#                     )

#     job_data = st.session_state.job_data

#     if job_data:

#         st.divider()

#         st.subheader(
#             f"💼 Available Private Jobs ({len(job_data)})"
#         )

#         for i, job in enumerate(
#             job_data,
#             start=1
#         ):

#             title = job.get(
#                 "title",
#                 "Job Title Not Available"
#             )

#             company_data = job.get(
#                 "company",
#                 {}
#             )

#             if isinstance(
#                 company_data,
#                 dict
#             ):

#                 company = company_data.get(
#                     "display_name",
#                     "Company Not Available"
#                 )

#             else:

#                 company = str(company_data)

#             location_data = job.get(
#                 "location",
#                 {}
#             )

#             if isinstance(
#                 location_data,
#                 dict
#             ):

#                 location = location_data.get(
#                     "display_name",
#                     "Location Not Available"
#                 )

#             else:

#                 location = str(location_data)

#             description = job.get(
#                 "description",
#                 "Description Not Available"
#             )

#             if len(description) > 600:
#                 description = description[:600] + "..."

#             apply_link = job.get(
#                 "redirect_url",
#                 ""
#             )

#             with st.container(border=True):

#                 st.markdown(
#                     f"### {i}. {title}"
#                 )

#                 st.write(
#                     f"🏢 **Company:** {company}"
#                 )

#                 st.write(
#                     f"📍 **Location:** {location}"
#                 )

#                 st.write(
#                     f"📝 **Description:** {description}"
#                 )

#                 if apply_link:
#                     st.link_button(
#                         "🚀 Apply / View Job",
#                         apply_link
#                     )

#     if job_data:

#         st.divider()

#         st.subheader(
#             "🎯 AI Job Matching"
#         )

#         st.write(
#             "Llama 3.2 will compare the jobs with your resume "
#             "and classify them."
#         )

#         if st.button(
#             "🤖 Analyze Jobs With AI",
#             key="analyze_jobs"
#         ):

#             with st.spinner(
#                 "🤖 Llama 3.2 is analyzing jobs..."
#             ):

#                 try:

#                     resume_for_ai = (
#                         st.session_state.resume_text[:7000]
#                     )

#                     jobs_to_analyze = job_data[:15]

#                     categories = {}

#                     progress = st.progress(0)

#                     total_jobs = len(
#                         jobs_to_analyze
#                     )

#                     for index, job in enumerate(
#                         jobs_to_analyze,
#                         start=1
#                     ):

#                         title = job.get(
#                             "title",
#                             "Not specified"
#                         )

#                         company_data = job.get(
#                             "company",
#                             {}
#                         )

#                         if isinstance(
#                             company_data,
#                             dict
#                         ):

#                             company = company_data.get(
#                                 "display_name",
#                                 "Not specified"
#                             )

#                         else:

#                             company = str(company_data)

#                         location_data = job.get(
#                             "location",
#                             {}
#                         )

#                         if isinstance(
#                             location_data,
#                             dict
#                         ):

#                             location = location_data.get(
#                                 "display_name",
#                                 "Not specified"
#                             )

#                         else:

#                             location = str(location_data)

#                         description = job.get(
#                             "description",
#                             "Not specified"
#                         )

#                         description = description[:800]

#                         prompt = f"""
# You are an AI Job Matching Assistant.

# CANDIDATE RESUME:
# {resume_for_ai}

# JOB:
# Title: {title}
# Company: {company}
# Location: {location}
# Description: {description}

# Choose exactly ONE category:

# SKILL MATCH
# EDUCATION / ELIGIBILITY MATCH
# OTHER JOB

# Rules:

# SKILL MATCH:
# The job strongly matches the candidate's actual
# skills, technologies, projects or experience.

# EDUCATION / ELIGIBILITY MATCH:
# The candidate appears eligible because of their
# degree, branch, education or fresher status,
# but the skill match is not strong.

# OTHER JOB:
# There is no strong skill match and no clear
# education/eligibility match.

# Do not invent skills or qualifications.

# Return ONLY one of these:

# SKILL MATCH

# or

# EDUCATION / ELIGIBILITY MATCH

# or

# OTHER JOB
# """

#                         response = generate_ai(prompt)

#                         result = response[
#                             "message"
#                         ][
#                             "content"
#                         ].strip().upper()

#                         if "SKILL MATCH" in result:

#                             categories[index] = (
#                                 "SKILL MATCH"
#                             )

#                         elif (
#                             "EDUCATION" in result
#                             or
#                             "ELIGIBILITY" in result
#                         ):

#                             categories[index] = (
#                                 "EDUCATION / ELIGIBILITY MATCH"
#                             )

#                         else:

#                             categories[index] = (
#                                 "OTHER JOB"
#                             )

#                         progress.progress(
#                             index / total_jobs
#                         )

#                     st.session_state.job_categories = (
#                         categories
#                     )

#                     st.success(
#                         f"AI analyzed {total_jobs} jobs successfully! ✅"
#                     )

#                     st.info(
#                         "Currently analyzing the first 15 jobs "
#                         "to keep the local AI fast."
#                     )

#                 except Exception as e:

#                     st.error(
#                         f"Ollama error: {e}"
#                     )

#         categories = (
#             st.session_state.job_categories
#         )

#         if categories:

#             st.subheader(
#                 "🎯 Jobs Matched With Your Resume"
#             )

#             def display_matched_job(
#                 job,
#                 number
#             ):

#                 title = job.get(
#                     "title",
#                     "Job Title Not Available"
#                 )

#                 company_data = job.get(
#                     "company",
#                     {}
#                 )

#                 if isinstance(
#                     company_data,
#                     dict
#                 ):

#                     company = company_data.get(
#                         "display_name",
#                         "Company Not Available"
#                     )

#                 else:

#                     company = str(company_data)

#                 location_data = job.get(
#                     "location",
#                     {}
#                 )

#                 if isinstance(
#                     location_data,
#                     dict
#                 ):

#                     location = location_data.get(
#                         "display_name",
#                         "Location Not Available"
#                     )

#                 else:

#                     location = str(location_data)

#                 description = job.get(
#                     "description",
#                     "Description Not Available"
#                 )

#                 if len(description) > 500:

#                     description = (
#                         description[:500]
#                         + "..."
#                     )

#                 apply_link = job.get(
#                     "redirect_url",
#                     ""
#                 )

#                 with st.container(
#                     border=True
#                 ):

#                     st.markdown(
#                         f"### {number}. {title}"
#                     )

#                     st.write(
#                         f"🏢 **Company:** {company}"
#                     )

#                     st.write(
#                         f"📍 **Location:** {location}"
#                     )

#                     st.write(
#                         f"📝 **Description:** {description}"
#                     )

#                     if apply_link:

#                         st.link_button(
#                             "🚀 Apply / View Job",
#                             apply_link
#                         )

#             st.markdown(
#                 "## 🟢 Skill Match"
#             )

#             found = False

#             for i, job in enumerate(
#                 job_data[:15],
#                 start=1
#             ):

#                 if categories.get(i) == "SKILL MATCH":

#                     found = True

#                     display_matched_job(
#                         job,
#                         i
#                     )

#             if not found:

#                 st.info(
#                     "No strong skill matches found."
#                 )

#             st.markdown(
#                 "## 🎓 Education / Eligibility Match"
#             )

#             found = False

#             for i, job in enumerate(
#                 job_data[:15],
#                 start=1
#             ):

#                 if (
#                     categories.get(i)
#                     == "EDUCATION / ELIGIBILITY MATCH"
#                 ):

#                     found = True

#                     display_matched_job(
#                         job,
#                         i
#                     )

#             if not found:

#                 st.info(
#                     "No education/eligibility matches found."
#                 )

#             st.markdown(
#                 "## 🔵 Related / Other Jobs"
#             )

#             found = False

#             for i, job in enumerate(
#                 job_data[:15],
#                 start=1
#             ):

#                 if categories.get(i) == "OTHER JOB":

#                     found = True

#                     display_matched_job(
#                         job,
#                         i
#                     )

#             if not found:

#                 st.info(
#                     "No other jobs found."
#                 )


# # =========================================================
# # TAB 2: GOVERNMENT JOBS
# # =========================================================

# with tab_government:

#     st.subheader(
#         "🏛️ Government Jobs"
#     )

#     st.write(
#         "Find current government vacancies through official "
#         "Government of India employment portals."
#     )

#     with st.container(border=True):

#         st.markdown(
#             "### 🏛️ Employment News — Government Vacancies"
#         )

#         st.write(
#             "Official Government of India employment portal "
#             "listing vacancies from government organizations, "
#             "PSUs, universities and other public bodies."
#         )

#         st.link_button(
#             "🔎 View Government Jobs",
#             "https://employmentnews.gov.in/newemp/AllJobs.aspx?k=All"
#         )

#     with st.container(border=True):

#         st.markdown(
#             "### 🇮🇳 National Career Service — Government Jobs"
#         )

#         st.write(
#             "Government of India's National Career Service portal "
#             "with a dedicated government-sector job search."
#         )

#         st.link_button(
#             "🔎 Search Government Jobs",
#             "https://www.ncs.gov.in/"
#         )

#     with st.container(border=True):

#         st.markdown(
#             "### 📮 India Post — Recruitment"
#         )

#         st.write(
#             "Official India Post recruitment and vacancy page."
#         )

#         st.link_button(
#             "📮 View India Post Vacancies",
#             "https://www.indiapost.gov.in/vacancies"
#         )


# # =========================================================
# # TAB 3: FREELANCING
# # =========================================================

# with tab_freelance:

#     st.subheader(
#         "🌐 Freelancing Opportunities"
#     )

#     st.write(
#         "Explore freelance opportunities from popular "
#         "freelancing platforms."
#     )

#     with st.container(border=True):

#         st.markdown(
#             "### 💻 Freelancer.com"
#         )

#         st.write(
#             "Find freelance projects in software development, "
#             "web development, design, writing and many other fields."
#         )

#         st.link_button(
#             "🔎 View Freelance Jobs",
#             "https://www.freelancer.com/jobs/"
#         )

#     with st.container(border=True):

#         st.markdown(
#             "### 🌐 Upwork"
#         )

#         st.write(
#             "Explore freelance and remote work opportunities "
#             "across technology and other professional fields."
#         )

#         st.link_button(
#             "🔎 View Freelance Jobs",
#             "https://www.upwork.com/freelance-jobs/"
#         )


# # =========================================================
# # TAB 4: AI APPLICATION ASSISTANT
# # =========================================================

# with tab_application:

#     st.subheader(
#         "✉️ AI Application Assistant"
#     )

#     st.write(
#         "Generate a customized application email, "
#         "cover letter, or recruiter message for a job."
#     )

#     job_data = st.session_state.job_data

#     if job_data:

#         job_options = []

#         for i, job in enumerate(
#             job_data,
#             start=1
#         ):

#             title = job.get(
#                 "title",
#                 "Unknown Job"
#             )

#             company_data = job.get(
#                 "company",
#                 {}
#             )

#             if isinstance(
#                 company_data,
#                 dict
#             ):

#                 company = company_data.get(
#                     "display_name",
#                     "Unknown Company"
#                 )

#             else:

#                 company = str(
#                     company_data
#                 )

#             job_options.append(
#                 f"JOB {i} — {title} — {company}"
#             )

#         selected_job_text = st.selectbox(
#             "Choose a job",
#             job_options
#         )

#         selected_index = (
#             job_options.index(
#                 selected_job_text
#             )
#         )

#         selected_job = job_data[
#             selected_index
#         ]

#         application_type = st.selectbox(
#             "Choose what you want to generate",
#             [
#                 "Job Application Email",
#                 "Cover Letter",
#                 "Recruiter Message"
#             ]
#         )

#         if st.button(
#             "✨ Generate Application",
#             key="generate_application"
#         ):

#             with st.spinner(
#                 "🤖 Llama 3.2 is preparing your application..."
#             ):

#                 try:

#                     selected_title = selected_job.get(
#                         "title",
#                         "Unknown Job"
#                     )

#                     company_data = selected_job.get(
#                         "company",
#                         {}
#                     )

#                     if isinstance(
#                         company_data,
#                         dict
#                     ):

#                         selected_company = (
#                             company_data.get(
#                                 "display_name",
#                                 "Unknown Company"
#                             )
#                         )

#                     else:

#                         selected_company = str(
#                             company_data
#                         )

#                     selected_description = (
#                         selected_job.get(
#                             "description",
#                             "Not specified"
#                         )
#                     )

#                     selected_description = (
#                         selected_description[:2500]
#                     )

#                     resume_for_application = (
#                         st.session_state.resume_text[:9000]
#                     )

#                     application_prompt = f"""
# You are an AI Job Application Assistant.

# CANDIDATE RESUME:

# {resume_for_application}

# JOB DETAILS:

# Job Title:
# {selected_title}

# Company:
# {selected_company}

# Job Description:
# {selected_description}

# TASK:

# Generate a professional {application_type} for
# the candidate applying to this job.

# IMPORTANT RULES:

# - Use ONLY information available in the resume.
# - Do NOT invent skills.
# - Do NOT invent experience.
# - Do NOT invent qualifications.
# - Do NOT invent achievements.
# - Do NOT invent projects.
# - If the candidate is a fresher, write the application
#   appropriately for a fresher.
# - Mention relevant skills, projects and education only
#   when they actually appear in the resume.
# - Keep the content concise and professional.
# - Make it suitable for the selected job.
# - Do not mention that AI generated the content.

# Return ONLY the {application_type}.
# """

#                     response = generate_ai(application_prompt)

#                     application_result = (
#                         response[
#                             "message"
#                         ]["content"]
#                     )

#                     st.session_state.application_result = (
#                         application_result
#                     )

#                 except Exception as e:

#                     st.error(
#                         f"Ollama error: {e}"
#                     )

#     else:

#         st.info(
#             "🔎 Find private jobs first. "
#             "Then you can select a job here and generate an application."
#         )

#     if st.session_state.application_result:

#         st.markdown(
#             "### 📝 Generated Application"
#         )

#         st.text_area(
#             "You can copy and edit this before sending.",
#             st.session_state.application_result,
#             height=400
#         )

#     elif job_data:

#         st.info(
#             "Select a job and application type, then click "
#             "✨ Generate Application."
#         )


# # =========================================================
# # FOOTER
# # =========================================================

# st.divider()

# st.caption(
#     "💡 AI runs locally using Ollama and Llama 3.2. "
#     "Always verify job details and eligibility on the "
#     "official recruitment website before applying."
# )
    

import streamlit as st
from pypdf import PdfReader
from docx import document
import requests


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="AI Job Search Assistant",
    page_icon="💼",
    layout="wide"
)


# =========================================================
# CLOUD AI - GEMINI
# =========================================================

def generate_ai(prompt):
    """Generate text using Google Gemini REST API."""

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it in Streamlit Cloud Secrets."
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.5-flash-lite:generateContent"
    )

    response = requests.post(
        url,
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        timeout=60
    )

    if response.status_code != 200:
        try:
            error_detail = (
                response.json()
                .get("error", {})
                .get("message", response.text)
            )
        except Exception:
            error_detail = response.text

        raise RuntimeError(
            f"Gemini API error ({response.status_code}): "
            f"{error_detail}"
        )

    data = response.json()

    try:
        return (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "Gemini returned an unexpected response."
        )


# =========================================================
# APP TITLE
# =========================================================

st.title("💼 AI Job Search & Application Assistant")

st.write(
    "Upload your resume to find private and "
    "government job opportunities."
)


# =========================================================
# SESSION STATE
# =========================================================

if "job_data" not in st.session_state:
    st.session_state.job_data = []

if "job_categories" not in st.session_state:
    st.session_state.job_categories = {}

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "application_result" not in st.session_state:
    st.session_state.application_result = ""

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None


# =========================================================
# RESUME UPLOAD
# =========================================================

st.subheader("📄 Upload Your Resume")

resume = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    key="resume_uploader"
)


if resume is not None:

    st.success("Resume uploaded successfully! ✅")

    try:

        resume_text = ""

        # =================================================
        # PDF RESUME
        # =================================================

        if resume.name.lower().endswith(".pdf"):

            reader = PdfReader(resume)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    resume_text += page_text + "\n"


        # =================================================
        # DOCX RESUME
        # =================================================

        elif resume.name.lower().endswith(".docx"):

            from docx import Document

            document = Document(resume)

            for paragraph in document.paragraphs:

                if paragraph.text.strip():
                    resume_text += paragraph.text + "\n"


        resume_text = resume_text.strip()

        st.session_state.resume_text = resume_text


    except Exception as e:

        st.error(
            f"Could not read the resume: {e}"
        )

        st.stop()


    # =====================================================
    # RESUME CONTENT
    # =====================================================

    if resume_text:

        st.subheader("📃 Resume Content")

        st.text_area(
            "Extracted Resume Text",
            resume_text,
            height=250
        )


        # =================================================
        # AI RESUME ANALYSIS
        # =================================================

        st.subheader("🧠 AI Resume Analysis")

        if st.button(
            "Analyze Resume",
            key="analyze_resume"
        ):

            with st.spinner(
                "Gemini is analyzing your resume..."
            ):

                prompt = f"""
You are an AI Resume Analysis Assistant.

Analyze the following resume.

Extract:

1. Name
2. Education
3. Technical Skills
4. Soft Skills
5. Projects
6. Internships / Experience
7. Certifications
8. Suggested Job Roles

Also mention important skills that appear to be missing
for the suggested job roles.

Do not invent information that is not present in the resume.

Give the answer in a clear and professional format.

RESUME:

{resume_text}
"""

                try:

                    response = generate_ai(prompt)

                    # Gemini function already returns text
                    analysis = response

                    st.session_state.resume_analysis = analysis

                    st.success(
                        "Resume analysis completed! ✅"
                    )

                except Exception as e:

                    st.error(
                        f"Gemini error: {e}"
                    )


        if st.session_state.resume_analysis:

            st.text_area(
                "AI Analysis",
                st.session_state.resume_analysis,
                height=450
            )


# =========================================================
# OPPORTUNITY TABS
# =========================================================

st.divider()

st.subheader("🚀 Explore Opportunities")

(
    tab_private,
    tab_government,
    tab_freelance,
    tab_application
) = st.tabs(
    [
        "🔎 Private Jobs",
        "🏛️ Government Jobs",
        "🌐 Freelancing",
        "✉️ AI Application"
    ]
)


# =========================================================
# TAB 1 - PRIVATE JOBS
# =========================================================

with tab_private:

    st.subheader(
        "🔎 Find Jobs Based on Your Resume"
    )

    st.write(
        "We'll use your resume skills, education, "
        "projects and experience to find different "
        "private job opportunities."
    )


    if not st.session_state.resume_text:

        st.warning(
            "⚠️ Please upload your resume first."
        )

    else:

        if st.button(
            "🔎 Find Jobs For Me",
            key="find_private_jobs"
        ):

            with st.spinner(
                "Analyzing your resume and searching "
                "for suitable jobs..."
            ):

                try:

                    # -------------------------------------
                    # ADZUNA SECRETS
                    # -------------------------------------

                    APP_ID = st.secrets["ADZUNA_APP_ID"]

                    APP_KEY = st.secrets["ADZUNA_APP_KEY"]


                    # -------------------------------------
                    # RESUME
                    # -------------------------------------

                    resume_for_search = (
                        st.session_state.resume_text[:12000]
                    )


                    # -------------------------------------
                    # GENERATE SEARCH QUERIES
                    # -------------------------------------

                    prompt = f"""
You are a job-search assistant.

Read the following resume and identify broad
job-search keywords that are suitable for this candidate.

Resume:

{resume_for_search}

Return ONLY 6 short job-search queries.

Rules:

- Do not return full sentences.
- Do not return explanations.
- Include different suitable job areas.
- Consider technical skills, projects, education
  and fresher eligibility.
- Do not focus on only one programming language.
- Do not invent skills that are not present in the resume.

Example format:

Python developer
Software developer
Web developer
QA tester
Technical support
Graduate software jobs
"""

                    ai_response = generate_ai(prompt)

                    # Gemini returns plain text
                    search_text = ai_response


                    # -------------------------------------
                    # EXTRACT SEARCH QUERIES
                    # -------------------------------------

                    search_queries = []

                    for line in search_text.splitlines():

                        line = line.strip()

                        if not line:
                            continue

                        line = line.lstrip(
                            "-•*0123456789. "
                        )

                        if line:
                            search_queries.append(line)


                    # Remove duplicates
                    search_queries = list(
                        dict.fromkeys(
                            search_queries
                        )
                    )

                    search_queries = search_queries[:6]


                    if not search_queries:

                        st.error(
                            "Could not generate job searches "
                            "from the resume."
                        )

                    else:

                        st.info(
                            "Searching across multiple job areas: "
                            + ", ".join(search_queries)
                        )


                        # ---------------------------------
                        # ADZUNA SEARCH
                        # ---------------------------------

                        all_jobs = []

                        url = (
                            "https://api.adzuna.com/"
                            "v1/api/jobs/in/search/1"
                        )


                        for query in search_queries:

                            params = {
                                "app_id": APP_ID,
                                "app_key": APP_KEY,
                                "results_per_page": 10,
                                "what": query,
                                "where": "India",
                                "content-type": "application/json"
                            }


                            response = requests.get(
                                url,
                                params=params,
                                timeout=30
                            )


                            if response.status_code == 200:

                                data = response.json()

                                jobs = data.get(
                                    "results",
                                    []
                                )

                                all_jobs.extend(jobs)


                            elif response.status_code == 429:

                                st.warning(
                                    "⚠️ Adzuna API rate limit "
                                    "was reached. Some searches "
                                    "may be missing."
                                )

                                break


                            else:

                                st.warning(
                                    f"Adzuna search failed for "
                                    f"'{query}' "
                                    f"(HTTP {response.status_code})"
                                )


                        # ---------------------------------
                        # REMOVE DUPLICATES
                        # ---------------------------------

                        unique_jobs = []

                        seen_jobs = set()


                        for job in all_jobs:

                            job_id = str(
                                job.get(
                                    "id",
                                    ""
                                )
                            )


                            if (
                                job_id
                                and job_id not in seen_jobs
                            ):

                                seen_jobs.add(job_id)

                                unique_jobs.append(job)


                        unique_jobs = unique_jobs[:30]


                        # Save to session state

                        st.session_state.job_data = (
                            unique_jobs
                        )

                        st.session_state.job_categories = {}


                        if unique_jobs:

                            st.success(
                                f"{len(unique_jobs)} "
                                "different private jobs found! ✅"
                            )

                        else:

                            st.warning(
                                "No jobs were found. "
                                "Try again later or check "
                                "your Adzuna API credentials."
                            )


                except Exception as e:

                    st.error(
                        f"Could not search for jobs: {e}"
                    )


    # =====================================================
    # DISPLAY PRIVATE JOBS
    # =====================================================

    job_data = st.session_state.job_data


    if job_data:

        st.divider()

        st.subheader(
            f"💼 Available Private Jobs "
            f"({len(job_data)})"
        )


        for i, job in enumerate(
            job_data,
            start=1
        ):

            title = job.get(
                "title",
                "Job Title Not Available"
            )


            company_data = job.get(
                "company",
                {}
            )


            if isinstance(
                company_data,
                dict
            ):

                company = company_data.get(
                    "display_name",
                    "Company Not Available"
                )

            else:

                company = str(
                    company_data
                )


            location_data = job.get(
                "location",
                {}
            )


            if isinstance(
                location_data,
                dict
            ):

                location = location_data.get(
                    "display_name",
                    "Location Not Available"
                )

            else:

                location = str(
                    location_data
                )


            description = job.get(
                "description",
                "Description Not Available"
            )


            if len(description) > 600:

                description = (
                    description[:600]
                    + "..."
                )


            apply_link = job.get(
                "redirect_url",
                ""
            )


            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {i}. {title}"
                )

                st.write(
                    f"🏢 **Company:** {company}"
                )

                st.write(
                    f"📍 **Location:** {location}"
                )

                st.write(
                    f"📝 **Description:** {description}"
                )


                if apply_link:

                    st.link_button(
                        "🚀 Apply / View Job",
                        apply_link
                    )


    # =====================================================
    # AI JOB MATCHING
    # =====================================================

    if job_data:

        st.divider()

        st.subheader(
            "🎯 AI Job Matching"
        )

        st.write(
            "Gemini will compare the jobs with your "
            "resume and classify them."
        )


        if st.button(
            "🤖 Analyze Jobs With AI",
            key="analyze_jobs"
        ):

            with st.spinner(
                "🤖 Gemini is analyzing jobs..."
            ):

                try:

                    resume_for_ai = (
                        st.session_state.resume_text[:7000]
                    )


                    jobs_to_analyze = job_data[:15]


                    categories = {}


                    progress = st.progress(0)


                    total_jobs = len(
                        jobs_to_analyze
                    )


                    for index, job in enumerate(
                        jobs_to_analyze,
                        start=1
                    ):

                        title = job.get(
                            "title",
                            "Not specified"
                        )


                        company_data = job.get(
                            "company",
                            {}
                        )


                        if isinstance(
                            company_data,
                            dict
                        ):

                            company = company_data.get(
                                "display_name",
                                "Not specified"
                            )

                        else:

                            company = str(
                                company_data
                            )


                        location_data = job.get(
                            "location",
                            {}
                        )


                        if isinstance(
                            location_data,
                            dict
                        ):

                            location = location_data.get(
                                "display_name",
                                "Not specified"
                            )

                        else:

                            location = str(
                                location_data
                            )


                        description = job.get(
                            "description",
                            "Not specified"
                        )


                        description = description[:800]


                        prompt = f"""
You are an AI Job Matching Assistant.

CANDIDATE RESUME:

{resume_for_ai}

JOB:

Title: {title}
Company: {company}
Location: {location}
Description: {description}

Choose exactly ONE category:

SKILL MATCH
EDUCATION / ELIGIBILITY MATCH
OTHER JOB

Rules:

SKILL MATCH:
The job strongly matches the candidate's actual
skills, technologies, projects or experience.

EDUCATION / ELIGIBILITY MATCH:
The candidate appears eligible because of their
degree, branch, education or fresher status,
but the skill match is not strong.

OTHER JOB:
There is no strong skill match and no clear
education/eligibility match.

Do not invent skills or qualifications.

Return ONLY one of these:

SKILL MATCH

or

EDUCATION / ELIGIBILITY MATCH

or

OTHER JOB
"""


                        response = generate_ai(
                            prompt
                        )


                        # Gemini returns plain text
                        result = response.strip().upper()


                        if "SKILL MATCH" in result:

                            categories[index] = (
                                "SKILL MATCH"
                            )


                        elif (
                            "EDUCATION" in result
                            or
                            "ELIGIBILITY" in result
                        ):

                            categories[index] = (
                                "EDUCATION / ELIGIBILITY MATCH"
                            )


                        else:

                            categories[index] = (
                                "OTHER JOB"
                            )


                        progress.progress(
                            index / total_jobs
                        )


                    st.session_state.job_categories = (
                        categories
                    )


                    st.success(
                        f"AI analyzed {total_jobs} "
                        "jobs successfully! ✅"
                    )


                    st.info(
                        "Currently analyzing the first "
                        "15 jobs to keep the AI processing fast."
                    )


                except Exception as e:

                    st.error(
                        f"Gemini error: {e}"
                    )


        # =================================================
        # DISPLAY MATCHED JOBS
        # =================================================

        categories = (
            st.session_state.job_categories
        )


        if categories:

            st.subheader(
                "🎯 Jobs Matched With Your Resume"
            )


            def display_matched_job(
                job,
                number
            ):

                title = job.get(
                    "title",
                    "Job Title Not Available"
                )


                company_data = job.get(
                    "company",
                    {}
                )


                if isinstance(
                    company_data,
                    dict
                ):

                    company = company_data.get(
                        "display_name",
                        "Company Not Available"
                    )

                else:

                    company = str(
                        company_data
                    )


                location_data = job.get(
                    "location",
                    {}
                )


                if isinstance(
                    location_data,
                    dict
                ):

                    location = location_data.get(
                        "display_name",
                        "Location Not Available"
                    )

                else:

                    location = str(
                        location_data
                    )


                description = job.get(
                    "description",
                    "Description Not Available"
                )


                if len(description) > 500:

                    description = (
                        description[:500]
                        + "..."
                    )


                apply_link = job.get(
                    "redirect_url",
                    ""
                )


                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {number}. {title}"
                    )

                    st.write(
                        f"🏢 **Company:** {company}"
                    )

                    st.write(
                        f"📍 **Location:** {location}"
                    )

                    st.write(
                        f"📝 **Description:** {description}"
                    )


                    if apply_link:

                        st.link_button(
                            "🚀 Apply / View Job",
                            apply_link
                        )


            # ---------------------------------------------
            # SKILL MATCH
            # ---------------------------------------------
            st.markdown(
                "## 🟢 Skill Match"
            )


            found = False


            for i, job in enumerate(
                job_data[:15],
                start=1
            ):

                if categories.get(i) == "SKILL MATCH":

                    display_matched_job(
                        job,
                        i
                    )

                    found = True


            if not found:

                st.info(
                    "No strong skill matches found "
                    "among the analyzed jobs."
                )


            # ---------------------------------------------
            # EDUCATION / ELIGIBILITY MATCH
            # ---------------------------------------------

            st.markdown(
                "## 🔵 Education / Eligibility Match"
            )


            found = False


            for i, job in enumerate(
                job_data[:15],
                start=1
            ):

                if categories.get(i) == (
                    "EDUCATION / ELIGIBILITY MATCH"
                ):

                    display_matched_job(
                        job,
                        i
                    )

                    found = True


            if not found:

                st.info(
                    "No education/eligibility matches "
                    "found among the analyzed jobs."
                )


            # ---------------------------------------------
            # OTHER JOBS
            # ---------------------------------------------

            st.markdown(
                "## ⚪ Other Jobs"
            )


            found = False


            for i, job in enumerate(
                job_data[:15],
                start=1
            ):

                if categories.get(i) == "OTHER JOB":

                    display_matched_job(
                        job,
                        i
                    )

                    found = True


            if not found:

                st.info(
                    "No other jobs in the analyzed set."
                )


# =========================================================
# TAB 2: GOVERNMENT JOBS
# =========================================================

with tab_government:

    st.subheader("🏛️ Government Jobs")

    st.write(
        "Find government job opportunities based on "
        "your educational qualification."
    )

    # -----------------------------------------------------
    # CHECK RESUME
    # -----------------------------------------------------

    if not st.session_state.get("resume_text"):

        st.warning(
            "📄 Please upload your resume first "
            "to find suitable government jobs."
        )

    else:

        resume_text = st.session_state.resume_text

        # -------------------------------------------------
        # FIND GOVERNMENT JOBS BUTTON
        # -------------------------------------------------

        if st.button(
            "🔎 Find Government Jobs For Me",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Analyzing your educational qualification..."
            ):

                try:

                    # =============================================
                    # GOVERNMENT JOB DATABASE
                    # =============================================

                    government_jobs = [

                        # -----------------------------------------
                        # 10TH LEVEL
                        # -----------------------------------------

                        {
                            "education": "10th Pass",
                            "category": "SSC",
                            "organization": "Staff Selection Commission",
                            "role": "Multi Tasking Staff (MTS)",
                            "work": (
                                "Office support, records, files, "
                                "basic departmental and general "
                                "government duties."
                            ),
                            "location": "Various locations across India",
                            "qualification": "10th Pass",
                            "url": "https://ssc.gov.in/"
                        },

                        {
                            "education": "10th Pass",
                            "category": "RRB",
                            "organization": "Railway Recruitment Board",
                            "role": "Level-1 Railway Posts",
                            "work": (
                                "Railway maintenance, station support, "
                                "track-related and other Level-1 duties."
                            ),
                            "location": "Various Railway Zones across India",
                            "qualification": "10th Pass / as specified in notification",
                            "url": "https://www.rrbapply.gov.in/"
                        },

                        {
                            "education": "10th Pass",
                            "category": "India Post",
                            "organization": "Department of Posts",
                            "role": "Gramin Dak Sevak (GDS)",
                            "work": (
                                "Postal delivery, customer service, "
                                "branch post office and related duties."
                            ),
                            "location": "Various locations across India",
                            "qualification": "10th Pass",
                            "url": "https://indiapostgdsonline.gov.in/"
                        },

                        # -----------------------------------------
                        # 12TH LEVEL
                        # -----------------------------------------

                        {
                            "education": "12th Pass",
                            "category": "SSC",
                            "organization": "Staff Selection Commission",
                            "role": "CHSL - LDC / JSA / DEO",
                            "work": (
                                "Clerical work, data entry, documentation, "
                                "office records and government administration."
                            ),
                            "location": "Various Central Government offices",
                            "qualification": "12th Pass",
                            "url": "https://ssc.gov.in/"
                        },

                        {
                            "education": "12th Pass",
                            "category": "RRB",
                            "organization": "Railway Recruitment Board",
                            "role": "NTPC Undergraduate Posts",
                            "work": (
                                "Railway commercial, clerical, "
                                "ticketing and office-related activities."
                            ),
                            "location": "Various Railway Zones across India",
                            "qualification": "12th Pass / as specified in notification",
                            "url": "https://www.rrbapply.gov.in/"
                        },

                        {
                            "education": "12th Pass",
                            "category": "Defence",
                            "organization": "Indian Army / Defence",
                            "role": "Various 12th-level Defence Entries",
                            "work": (
                                "Defence, technical and support duties "
                                "depending on the recruitment."
                            ),
                            "location": "Various locations across India",
                            "qualification": "12th Pass / stream-specific",
                            "url": "https://joinindianarmy.nic.in/"
                        },

                        # -----------------------------------------
                        # DIPLOMA LEVEL
                        # -----------------------------------------

                        {
                            "education": "Diploma",
                            "category": "RRB",
                            "organization": "Railway Recruitment Board",
                            "role": "Junior Engineer (JE)",
                            "work": (
                                "Technical and engineering-related "
                                "work in railway departments."
                            ),
                            "location": "Various Railway Zones across India",
                            "qualification": "Diploma / Degree depending on discipline",
                            "url": "https://www.rrbapply.gov.in/"
                        },

                        {
                            "education": "Diploma",
                            "category": "PSU",
                            "organization": "Public Sector Undertakings",
                            "role": "Technician / Technical Assistant",
                            "work": (
                                "Technical maintenance, equipment handling, "
                                "operations and engineering support."
                            ),
                            "location": "Depends on organization",
                            "qualification": "Relevant Diploma / technical qualification",
                            "url": "https://employmentnews.gov.in/"
                        },

                        {
                            "education": "Diploma",
                            "category": "State Government",
                            "organization": "State Government Departments",
                            "role": "Junior Technical / Engineering Posts",
                            "work": (
                                "Technical support, engineering operations, "
                                "maintenance and departmental work."
                            ),
                            "location": "Various locations within the state",
                            "qualification": "Relevant Diploma",
                            "url": "https://employmentnews.gov.in/"
                        },

                        # -----------------------------------------
                        # DEGREE LEVEL
                        # -----------------------------------------

                        {
                            "education": "Degree",
                            "category": "SSC",
                            "organization": "Staff Selection Commission",
                            "role": "SSC CGL Posts",
                            "work": (
                                "Government administration, taxation, "
                                "accounts, auditing and departmental work."
                            ),
                            "location": "Various Central Government offices",
                            "qualification": "Bachelor's Degree",
                            "url": "https://ssc.gov.in/"
                        },

                        {
                            "education": "Degree",
                            "category": "RRB",
                            "organization": "Railway Recruitment Board",
                            "role": "NTPC Graduate Posts",
                            "work": (
                                "Railway operations, administration, "
                                "commercial and office-related activities."
                            ),
                            "location": "Various Railway Zones across India",
                            "qualification": "Bachelor's Degree / post-specific requirements",
                            "url": "https://www.rrbapply.gov.in/"
                        },

                        {
                            "education": "Degree",
                            "category": "Banking",
                            "organization": "IBPS / Public Sector Banks",
                            "role": "Probationary Officer / Clerk",
                            "work": (
                                "Banking operations, customer service, "
                                "financial services and administration."
                            ),
                            "location": "Various locations across India",
                            "qualification": "Bachelor's Degree",
                            "url": "https://www.ibps.in/"
                        },

                        {
                            "education": "Degree",
                            "category": "UPSC",
                            "organization": "Union Public Service Commission",
                            "role": "Civil Services / Other Graduate Posts",
                            "work": (
                                "Administrative, government and specialist "
                                "services depending on examination."
                            ),
                            "location": "Various locations across India",
                            "qualification": "Bachelor's Degree / post-specific",
                            "url": "https://www.upsc.gov.in/"
                        },

                        # -----------------------------------------
                        # B.TECH / ENGINEERING
                        # -----------------------------------------

                        {
                            "education": "B.Tech / Engineering",
                            "category": "RRB",
                            "organization": "Railway Recruitment Board",
                            "role": "Junior Engineer / Technical Posts",
                            "work": (
                                "Engineering, railway infrastructure, "
                                "technical operations and maintenance."
                            ),
                            "location": "Various Railway Zones across India",
                            "qualification": "Diploma / B.Tech depending on discipline",
                            "url": "https://www.rrbapply.gov.in/"
                        },

                        {
                            "education": "B.Tech / Engineering",
                            "category": "PSU",
                            "organization": "Public Sector Undertakings",
                            "role": "Engineer / Graduate Engineer Trainee",
                            "work": (
                                "Engineering, technology, operations, "
                                "projects and technical development."
                            ),
                            "location": "Depends on organization",
                            "qualification": "B.E. / B.Tech in relevant discipline",
                            "url": "https://employmentnews.gov.in/"
                        },

                        {
                            "education": "B.Tech / Engineering",
                            "category": "DRDO",
                            "organization": "Defence Research and Development Organisation",
                            "role": "Scientist / Technical Posts",
                            "work": (
                                "Defence research, engineering, software, "
                                "technology and technical development."
                            ),
                            "location": "Various DRDO laboratories across India",
                            "qualification": "B.Tech / relevant engineering qualification",
                            "url": "https://www.drdo.gov.in/"
                        },

                        {
                            "education": "B.Tech / Engineering",
                            "category": "ISRO",
                            "organization": "Indian Space Research Organisation",
                            "role": "Scientist / Engineer",
                            "work": (
                                "Space technology, software, engineering, "
                                "data processing and research."
                            ),
                            "location": "Various ISRO centres across India",
                            "qualification": "B.Tech / relevant engineering degree",
                            "url": "https://www.isro.gov.in/"
                        },

                        {
                            "education": "B.Tech / Engineering",
                            "category": "NIC",
                            "organization": "National Informatics Centre",
                            "role": "Scientist / Technical Officer",
                            "work": (
                                "Government software, e-governance, "
                                "IT infrastructure and digital services."
                            ),
                            "location": "Various locations across India",
                            "qualification": "Relevant engineering / technical degree",
                            "url": "https://www.nic.gov.in/"
                        },

                        {
                            "education": "B.Tech / Engineering",
                            "category": "UPSC",
                            "organization": "Union Public Service Commission",
                            "role": "Engineering / Technical Services",
                            "work": (
                                "Engineering and technical services "
                                "within Central Government departments."
                            ),
                            "location": "Various locations across India",
                            "qualification": "Engineering degree / post-specific",
                            "url": "https://www.upsc.gov.in/"
                        }

                    ]

                    # =============================================
                    # IDENTIFY CANDIDATE EDUCATION LEVEL
                    # =============================================

                    education_prompt = f"""
Analyze this candidate's resume.

RESUME:
{resume_text[:12000]}

Identify the HIGHEST COMPLETED EDUCATIONAL
QUALIFICATION.

Choose ONLY ONE:

10th Pass
12th Pass
Diploma
Degree
B.Tech / Engineering

IMPORTANT:
- If the candidate is currently studying B.Tech but
  has not completed it, still identify them as
  "B.Tech / Engineering" for job discovery,
  but actual eligibility must be verified from the
  recruitment notification.
- Do not consider certificates as a degree.
- Return ONLY ONE option.
"""

                    education_response = generate_ai(
                        education_prompt
                    )

                    education_level = (
                        education_response
                        .strip()
                        .upper()
                    )

                    # =============================================
                    # NORMALIZE GEMINI RESPONSE
                    # =============================================

                    if "B.TECH" in education_level:

                        candidate_level = "B.Tech / Engineering"

                    elif "ENGINEERING" in education_level:

                        candidate_level = "B.Tech / Engineering"

                    elif "DIPLOMA" in education_level:

                        candidate_level = "Diploma"

                    elif "12TH" in education_level:

                        candidate_level = "12th Pass"

                    elif "DEGREE" in education_level:

                        candidate_level = "Degree"

                    elif "10TH" in education_level:

                        candidate_level = "10th Pass"

                    else:

                        candidate_level = "Degree"

                    # =============================================
                    # EDUCATION HIERARCHY
                    # =============================================

                    education_order = {
                        "10th Pass": 1,
                        "12th Pass": 2,
                        "Diploma": 3,
                        "Degree": 4,
                        "B.Tech / Engineering": 5
                    }

                    candidate_rank = education_order[
                        candidate_level
                    ]

                    # =============================================
                    # SHOW JOBS SUITABLE FOR LEVEL
                    #
                    # Example:
                    # B.Tech candidate can see:
                    # B.Tech + Degree + 12th + 10th jobs
                    #
                    # But we will prioritize higher-level jobs.
                    # =============================================

                    matched_jobs = []

                    for job in government_jobs:

                        job_rank = education_order[
                            job["education"]
                        ]

                        if job_rank <= candidate_rank:

                            matched_jobs.append(job)

                    # Put candidate's own level first,
                    # followed by lower qualification levels.

                    matched_jobs.sort(
                        key=lambda job: education_order[
                            job["education"]
                        ],
                        reverse=True
                    )

                    # Store in session
                    st.session_state[
                        "government_jobs"
                    ] = matched_jobs

                    st.session_state[
                        "government_education_level"
                    ] = candidate_level

                except Exception as e:

                    st.error(
                        f"Government job matching error: {e}"
                    )

        # =====================================================
        # DISPLAY RESULTS
        # =====================================================

        government_jobs = st.session_state.get(
            "government_jobs",
            []
        )

        candidate_level = st.session_state.get(
            "government_education_level",
            ""
        )

        if government_jobs:

            st.success(
                f"🎓 Your education level: "
                f"{candidate_level}"
            )

            st.info(
                "Showing government job categories that "
                "match your education level or below. "
                "Always verify the exact eligibility in "
                "the latest recruitment notification."
            )

            # =================================================
            # GROUP BY EDUCATION LEVEL
            # =================================================

            education_levels = [
                "B.Tech / Engineering",
                "Degree",
                "Diploma",
                "12th Pass",
                "10th Pass"
            ]

            for level in education_levels:

                level_jobs = [
                    job
                    for job in government_jobs
                    if job["education"] == level
                ]

                if not level_jobs:
                    continue

                # ---------------------------------------------
                # SECTION HEADING
                # ---------------------------------------------

                if level == "B.Tech / Engineering":

                    st.markdown(
                        "## 🎓 B.Tech / Engineering Level"
                    )

                elif level == "Degree":

                    st.markdown(
                        "## 🎓 Degree Level"
                    )

                elif level == "Diploma":

                    st.markdown(
                        "## 🔧 Diploma Level"
                    )

                elif level == "12th Pass":

                    st.markdown(
                        "## 📚 12th Pass Level"
                    )

                elif level == "10th Pass":

                    st.markdown(
                        "## 📝 10th Pass Level"
                    )

                # ---------------------------------------------
                # JOB CARDS
                # ---------------------------------------------

                for job in level_jobs:

                    with st.container(border=True):

                        st.markdown(
                            f"### 🏛️ {job['role']}"
                        )

                        st.write(
                            f"**Job Category:** "
                            f"{job['category']}"
                        )

                        st.write(
                            f"**Organization:** "
                            f"{job['organization']}"
                        )

                        st.write(
                            f"**Work Details:** "
                            f"{job['work']}"
                        )

                        st.write(
                            f"**Location:** "
                            f"{job['location']}"
                        )

                        st.write(
                            f"**Education:** "
                            f"{job['qualification']}"
                        )

                        st.link_button(
                            "🔗 Official Recruitment Website",
                            job["url"],
                            use_container_width=True
                        )

        # =====================================================
        # OFFICIAL SOURCES
        # =====================================================

        st.divider()

        st.markdown(
            "## 🇮🇳 Official Government Recruitment Sources"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.link_button(
                "📢 Employment News",
                "https://employmentnews.gov.in/",
                use_container_width=True
            )

        with col2:

            st.link_button(
                "🚆 Railway (RRB)",
                "https://www.rrbapply.gov.in/",
                use_container_width=True
            )

        with col3:

            st.link_button(
                "📋 SSC",
                "https://ssc.gov.in/",
                use_container_width=True
            )

        st.caption(
            "⚠️ Job categories are shown for discovery. "
            "Before applying, verify the latest official "
            "notification, exact qualification, age limit, "
            "branch requirements, vacancies, location and "
            "application deadline."
        )
# =========================================================
# TAB 3: FREELANCING
# =========================================================

with tab_freelance:

    st.subheader("🌐 Freelancing & Remote Opportunities")

    st.write(
        "Find freelance-style and remote opportunities "
        "matched with your resume skills."
    )

    # -----------------------------------------------------
    # CHECK RESUME
    # -----------------------------------------------------

    if not st.session_state.get("resume_text"):

        st.warning(
            "📄 Please upload your resume first so we can "
            "find opportunities matching your skills."
        )

    else:

        resume_text = st.session_state.resume_text

        # -------------------------------------------------
        # FIND FREELANCE / REMOTE JOBS
        # -------------------------------------------------

        if st.button(
            "🔎 Find Freelance Jobs For Me",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Finding freelance and remote opportunities "
                "matching your resume..."
            ):

                try:

                    # =============================================
                    # ASK GEMINI FOR SEARCH TAGS
                    # =============================================

                    skill_prompt = f"""
Analyze this resume and identify the candidate's
most useful technical skills for freelance and
remote jobs.

RESUME:
{resume_text[:12000]}

Return ONLY a comma-separated list of up to 6
short English skill keywords.

Examples:
python, sql, web development, javascript, machine learning

Do not add explanations.
"""

                    ai_response = generate_ai(
                        skill_prompt
                    )

                    skills_text = ai_response.strip()

                    skills = [
                        skill.strip().lower()
                        for skill in skills_text.split(",")
                        if skill.strip()
                    ]

                    # Keep only first 6 skills
                    skills = skills[:6]

                    if not skills:

                        skills = [
                            "python",
                            "software",
                            "web development"
                        ]

                    # =============================================
                    # REMOTE OK PUBLIC API
                    # =============================================

                    api_url = "https://remoteok.com/api"

                    response = requests.get(
                        api_url,
                        timeout=30,
                        headers={
                            "User-Agent":
                            "AI Job Search Assistant"
                        }
                    )

                    response.raise_for_status()

                    data = response.json()

                    freelance_jobs = []

                    # =============================================
                    # MATCH JOBS USING SKILLS
                    # =============================================

                    for item in data:

                        # Skip metadata object
                        if not isinstance(item, dict):
                            continue

                        title = item.get(
                            "position",
                            ""
                        )

                        company = item.get(
                            "company",
                            "Company not specified"
                        )

                        description = item.get(
                            "description",
                            ""
                        )

                        tags = item.get(
                            "tags",
                            []
                        )

                        job_url = item.get(
                            "url",
                            ""
                        )

                        combined_text = (
                            f"{title} "
                            f"{company} "
                            f"{description} "
                            f"{' '.join(tags)}"
                        ).lower()

                        matched_skills = [
                            skill
                            for skill in skills
                            if skill in combined_text
                        ]

                        if matched_skills:

                            freelance_jobs.append(
                                {
                                    "title": title,
                                    "company": company,
                                    "description": description,
                                    "tags": tags,
                                    "url": job_url,
                                    "matched_skills":
                                    matched_skills
                                }
                            )

                    # Limit results
                    freelance_jobs = freelance_jobs[:20]

                    # =============================================
                    # SAVE RESULTS
                    # =============================================

                    st.session_state[
                        "freelance_jobs"
                    ] = freelance_jobs

                    st.session_state[
                        "freelance_skills"
                    ] = skills

                except Exception as e:

                    st.error(
                        f"Freelance job search error: {e}"
                    )

        # -----------------------------------------------------
        # DISPLAY RESULTS
        # -----------------------------------------------------

        freelance_jobs = st.session_state.get(
            "freelance_jobs",
            []
        )

        freelance_skills = st.session_state.get(
            "freelance_skills",
            []
        )

        if freelance_skills:

            st.info(
                "🔎 Searching based on your skills: "
                + ", ".join(freelance_skills)
            )

        if freelance_jobs:

            st.success(
                f"Found {len(freelance_jobs)} "
                "matching freelance/remote opportunities."
            )

            for job in freelance_jobs:

                with st.container(border=True):

                    st.markdown(
                        f"### 💻 {job['title']}"
                    )

                    st.write(
                        f"**Company:** {job['company']}"
                    )

                    if job["matched_skills"]:

                        st.success(
                            "🎯 Skill Match: "
                            + ", ".join(
                                job["matched_skills"]
                            )
                        )

                    if job["tags"]:

                        st.write(
                            "**Skills/Tags:** "
                            + ", ".join(
                                job["tags"][:10]
                            )
                        )

                    description = (
                        job["description"]
                        .replace("<p>", "")
                        .replace("</p>", "")
                    )

                    if description:

                        st.write(
                            description[:600]
                            + (
                                "..."
                                if len(description) > 600
                                else ""
                            )
                        )

                    if job["url"]:

                        st.link_button(
                            "🔗 View & Apply",
                            job["url"],
                            use_container_width=True
                        )

        elif st.session_state.get(
            "freelance_jobs"
        ) == []:

            st.warning(
                "No matching freelance/remote opportunities "
                "were found for the detected skills right now."
            )

        # -----------------------------------------------------
        # OFFICIAL FREELANCE PLATFORMS
        # -----------------------------------------------------

        st.divider()

        st.markdown(
            "## 🌐 Freelance Platforms"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "💻 Freelancer.com",
                "https://www.freelancer.com/jobs/",
                use_container_width=True
            )

        with col2:

            st.link_button(
                "🌐 Upwork",
                "https://www.upwork.com/freelance-jobs/",
                use_container_width=True
            )

        st.caption(
            "💡 Opportunities shown above are matched using "
            "skills detected from your uploaded resume. "
            "Always verify the project and client details "
            "before applying."
        )


# =========================================================
# TAB 4 - AI APPLICATION
# =========================================================

with tab_application:

    st.subheader(
        "✉️ AI Job Application Assistant"
    )


    job_data = st.session_state.job_data


    if job_data:

        # ---------------------------------------------
        # BUILD JOB OPTIONS
        # ---------------------------------------------

        job_options = []


        for i, job in enumerate(
            job_data,
            start=1
        ):

            title = job.get(
                "title",
                "Unknown Job"
            )


            company_data = job.get(
                "company",
                {}
            )


            if isinstance(
                company_data,
                dict
            ):

                company = company_data.get(
                    "display_name",
                    "Unknown Company"
                )

            else:

                company = str(
                    company_data
                )


            job_options.append(
                f"JOB {i} — {title} — {company}"
            )


        selected_job_text = st.selectbox(
            "Choose a job",
            job_options
        )


        selected_index = (
            job_options.index(
                selected_job_text
            )
        )


        selected_job = job_data[
            selected_index
        ]


        application_type = st.selectbox(
            "Choose what you want to generate",
            [
                "Job Application Email",
                "Cover Letter",
                "Recruiter Message"
            ]
        )


        if st.button(
            "✨ Generate Application",
            key="generate_application"
        ):

            with st.spinner(
                "🤖 Gemini is preparing your application..."
            ):

                try:

                    selected_title = (
                        selected_job.get(
                            "title",
                            "Unknown Job"
                        )
                    )


                    company_data = (
                        selected_job.get(
                            "company",
                            {}
                        )
                    )


                    if isinstance(
                        company_data,
                        dict
                    ):

                        selected_company = (
                            company_data.get(
                                "display_name",
                                "Unknown Company"
                            )
                        )

                    else:

                        selected_company = str(
                            company_data
                        )


                    selected_description = (
                        selected_job.get(
                            "description",
                            "Not specified"
                        )
                    )


                    selected_description = (
                        selected_description[:2500]
                    )


                    resume_for_application = (
                        st.session_state.resume_text[:9000]
                    )


                    application_prompt = f"""
You are an AI Job Application Assistant.

CANDIDATE RESUME:

{resume_for_application}

JOB DETAILS:

Job Title:
{selected_title}

Company:
{selected_company}

Job Description:
{selected_description}

TASK:

Generate a professional {application_type}
for the candidate applying to this job.

IMPORTANT RULES:

- Use ONLY information available in the resume.
- Do NOT invent skills.
- Do NOT invent experience.
- Do NOT invent qualifications.
- Do NOT invent achievements.
- Do NOT invent projects.
- If the candidate is a fresher, write the application
  appropriately for a fresher.
- Mention relevant skills, projects and education only
  when they actually appear in the resume.
- Keep the content concise and professional.
- Make it suitable for the selected job.
- Do not mention that AI generated the content.

Return ONLY the {application_type}.
"""


                    response = generate_ai(
                        application_prompt
                    )


                    # Gemini returns plain text
                    application_result = response


                    st.session_state.application_result = (
                        application_result
                    )


                    st.success(
                        "Application generated successfully! ✅"
                    )


                except Exception as e:

                    st.error(
                        f"Gemini error: {e}"
                    )


    else:

        st.info(
            "🔎 Find private jobs first. "
            "Then you can select a job here "
            "and generate an application."
        )


    # =====================================================
    # DISPLAY GENERATED APPLICATION
    # =====================================================
    if st.session_state.application_result:

        st.markdown(
            "### 📝 Generated Application"
        )


        st.text_area(
            "You can copy and edit this before sending.",
            st.session_state.application_result,
            height=400
        )


    elif job_data:

        st.info(
            "Select a job and application type, "
            "then click ✨ Generate Application."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💡 AI features are powered by Google Gemini. "
    "Always verify job details and eligibility on the "
    "official recruitment website before applying."
)
