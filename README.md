# AI Question Paper Generator

An automated system to generate examination papers based on Bloom's Taxonomy, following a layered architecture with React and Flask.

---

## 🏢 Business Perspective

### Overview
This system empowers educators to generate high-quality, balanced question papers in seconds. By leveraging AI and NLP, it removes the manual toil of question selection while ensuring that exams adhere to pedagogical standards like Bloom's Taxonomy.

### User Flow
1.  **Authentication**: Educators register or log in to their personal workspace.
2.  **Dashboard**: View and manage previously generated papers. Access is strictly isolated to the creator.
3.  **Paper Creation**:
    *   **Subject Selection**: Choose the relevant academic subject.
    *   **Material Upload (Optional)**: Upload PDF or TXT files to provide specific context for the AI.
    *   **Configuration**: Select specific topics, Bloom's levels (Remember, Understand, Apply, etc.), and difficulty.
    *   **Generation**: The AI analyzes the provided context/subject knowledge and generates a mix of MCQ and Descriptive questions.
4.  **Review & Export**: View the generated paper in a clean UI and download a professional PDF for distribution.

### Key Benefits
*   **Cognitive Balance**: Automatically aligns questions with Bloom’s Taxonomy for varied assessment.
*   **Time Efficiency**: Reduces hours of manual question drafting to a few clicks.
*   **Data Isolation**: Secure workspaces ensure educators only see their own work.
*   **Quality Content**: Generates meaningful MCQs with distractors derived from context keywords.

---

## 🛠 Technical Perspective

### Technology Stack
*   **Frontend**: React (Vite), Axios, Vanilla CSS.
*   **Backend**: Flask (Python), MySQL.
*   **NLP & AI Engine**: **SpaCy** (Entity & Sentence extraction) and **NLTK** (WordNet Lemmatization for verb-based Bloom's classification).
*   **Text Extraction**: Support for PDF (`PyPDF2`), DOCX (`python-docx`), and TXT.
*   **Security & Auth**: **PyJWT** (Token-based authentication) and **Werkzeug** (Password hashing).
*   **PDF Generation**: **ReportLab**.

### System Architecture
The project follows a modular **Service-Repository** pattern:
*   **Routes**: Handles API endpoints and session verification.
*   **Services**: Orchestrates business logic (e.g., `PaperService` for generation logic).
*   **Repositories**: Direct data access layer for MySQL persistence.
*   **NLP Engine**: 
    *   `TextExtractor`: Handles PDF/TXT parsing.
    *   `NLPAnalyzer`: Uses SpaCy for sentence extraction, keyword mapping, and subject identification.
    *   `BloomClassifier`: Categorizes questions into cognitive levels.

### Database Schema
*   `users`: Name, email, hashed passwords.
*   `papers`: Subject, title, difficulty, linked to `user_id`.
*   `questions`: Text, bloom level, difficulty, type.
*   `question_options`: Meaningful distractors and correct answers for MCQs.
*   `paper_questions`: Junction table linking papers to their specific questions.

### Developer Setup
1.  **Database**: 
    *   Ensure MySQL is running.
    *   Run `python3 backend/db_config.py` to initialize the schema.
2.  **Backend**:
    *   Install dependencies: `pip install -r backend/requirements.txt`.
    *   Download SpaCy model: `python3 -m spacy download en_core_web_sm`.
    *   Download NLTK data: `python3 -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"`
    *   Run with `python3 backend/app.py`.
3.  **Frontend**:
    *   `cd frontend`
    *   `npm install`
    *   `npm run dev`

---

---

## 🚀 100% Free Deployment Masterclass (Academic Project)

This project is optimized for a zero-cost production deployment using professional-grade tools.

### 1. The Stack
*   **Database**: [Aiven](https://aiven.io/) (Free MySQL instance, no credit card required).
*   **Backend**: [Render](https://render.com/) (Free Web Service tier).
*   **Frontend**: [Vercel](https://vercel.com/) (Free tier for static sites).
*   **Secrets**: [Infisical](https://infisical.com/) (Free Developer tier for secret management).

### 2. Secret Vault Integration (Infisical)
Instead of insecure `.env` files, this project uses **Infisical** for centralized secret management.
1.  Create a free account on Infisical.
2.  Create a project and add your secrets (`DB_HOST`, `DB_PASSWORD`, `JWT_SECRET`, etc.).
3.  Generate a **Machine Identity** and get your `CLIENT_ID` and `CLIENT_SECRET`.
4.  Set `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`, and `INFISICAL_PROJECT_ID` in your Render environment variables.

### 3. Step-by-Step Deployment

#### A. Database (Aiven)
1. Sign up for **Aiven** and create a MySQL database.
2. Note down the URI or individual credentials (Host, User, Password, Port).
3. Whitelist `0.0.0.0/0` (or Render's outbound IPs) in Aiven's firewall.

#### B. Backend (Render)
1. Connect your GitHub repository.
2. Build Command: `pip install -r backend/requirements.txt && python3 -m spacy download en_core_web_sm && python3 -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"`
3. Start Command: `gunicorn backend.app:app` (or `python3 backend/app.py` for simplicity).
4. Add Environment Variables:
   * `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`, `INFISICAL_PROJECT_ID`
   * `FLASK_ENV`: `production`
   * `ALLOWED_ORIGINS`: Your Vercel URL.

#### C. Frontend (Vercel)
1. Import your repository into Vercel.
2. Framework Preset: `Vite`.
3. Build Command: `npm run build`.
4. Output Directory: `dist`.
5. Add Environment Variable:
   * `VITE_API_BASE_URL`: Your Render service URL (e.g., `https://your-api.onrender.com/api`).

### 4. Security Best Practices
*   **Zero Hardcoding**: All sensitive data is fetched at runtime from the Vault.
*   **CORS Protection**: The API only responds to requests from your authorized Vercel domain.
*   **HTTPS**: All platforms (Render, Vercel, Aiven) provide SSL encryption out of the box.

