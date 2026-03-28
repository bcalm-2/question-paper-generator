"""
Dependency Injection container — single wiring point for the entire application.

All services and repositories are constructed **once** here (singleton pattern)
and imported by route modules.  This eliminates scattered object instantiation
and makes the dependency graph explicit and testable.

Design patterns applied
-----------------------
* **Factory / Service Locator**: this module is the one place that knows
  how to assemble every concrete type.
* **Dependency Injection**: every class receives its dependencies via its
  constructor rather than creating them internally.
* **Singleton** (module-level): Python module caching ensures each object
  is built only once per process.
"""

# ---------------------------------------------------------------------------
# Repositories
# ---------------------------------------------------------------------------
from repositories.user_repository    import UserRepository
from repositories.paper_repository   import PaperRepository
from repositories.subject_repository import SubjectRepository, TopicRepository

user_repo    = UserRepository()
paper_repo   = PaperRepository()
subject_repo = SubjectRepository()
topic_repo   = TopicRepository()

# ---------------------------------------------------------------------------
# Core domain components (NLP / PDF)
# ---------------------------------------------------------------------------
from core.text_extractor   import TextExtractor
from core.nlp_analyzer     import NLPAnalyzer
from core.bloom_classifier import BloomClassifier
from core.pdf_generator    import PDFGenerator

extractor  = TextExtractor()
analyzer   = NLPAnalyzer()
classifier = BloomClassifier()
pdf_gen    = PDFGenerator()

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
from infrastructure.file_service import FileService
from core.question_strategy import QuestionStrategy
from services.auth_service       import AuthService
from services.paper_service      import PaperService
from services.app_config_service import AppConfigService
from services.subject_service    import SubjectService

file_service       = FileService()
question_strategy  = QuestionStrategy()
auth_service       = AuthService(user_repo)
paper_service      = PaperService(
    paper_repo,
    subject_repo,
    extractor,
    analyzer,
    classifier,
    pdf_gen,
    file_service,
    question_strategy,
)
app_config_service = AppConfigService(subject_repo)
subject_service    = SubjectService(subject_repo, topic_repo)
