import logging
import os
import uuid
import shutil
from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_text_splitters import CharacterTextSplitter
from langsmith import Client

from config.settings import Settings
from src.api.models.request import QuizRequest, QuizType
from src.api.models.response import QuizResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter()


@router.post("/create_quiz", response_model=QuizResponse)
async def create_quiz(quiz_request: QuizRequest):
    """
    ユーザーが入力した条件をもとにクイズを生成する。

    Args:
        type (str): 入力タイプ（テキストorURL）
        content (str): 読書メモまたはURL
        difficulty (str): クイズの難易度
        question_count (int): クイズの数

    Returns:
        QuizResponse: クイズのリスト（選択肢、解答、解説）
    """
    embeddings = OpenAIEmbeddings()

    if quiz_request.type == QuizType.TEXT:
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        texts = text_splitter.split_text(quiz_request.content)

        # ベクトルストア作成
        vectorstore = FAISS.from_texts(texts, embeddings)
    elif quiz_request.type == QuizType.URL:
        loader = FireCrawlLoader(
            url=quiz_request.content, mode="scrape", params={"onlyMainContent": True}
        )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        documents = text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(documents, embeddings)

    # UUIDを生成して、TMPディレクトリ内にユニークなサブディレクトリを作成する
    unique_id = uuid.uuid4().hex

    logger.info(unique_id)

    unique_dir = os.path.join(Settings.embeddings.TMP_VECTORDB_PATH, unique_id)

    logger.info(unique_dir)

    os.makedirs(unique_dir, exist_ok=True)

    vectorstore.save_local(unique_dir)
    new_vectorstore = FAISS.load_local(
        unique_dir,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = new_vectorstore.as_retriever(search_kwargs={"k": 8})

    client = Client()
    prompt = client.pull_prompt("langchain-ai/retrieval-qa-chat")

    # prompt = ChatPromptTemplate.from_template(prompt)

    llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL).with_structured_output(
        QuizResponse
    )

    rag_chain = {"input": RunnablePassthrough(), "context": retriever} | prompt | llm
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # プロンプトテンプレートを作成

    question = f"""
Based on the provided context information, please generate a quiz to assess comprehension of reading notes. The "context information" includes the text of reading notes, specific article content, annotations, and related descriptions.

**Important:**  
Generate the quiz in the same language as the provided context information. For example, if the context is in Japanese, generate the quiz in Japanese; if it is in English or any other language, generate the quiz in that same language.

Create {quiz_request.question_count} quiz questions at a difficulty level of {quiz_request.difficulty.value} (where difficulty can be "beginner", "intermediate", or "advanced"). Use the following guidelines for difficulty:
- **Beginner:** Questions should be very concise and basic, for example, asking "What is X?" in a straightforward manner.
- **Intermediate:** Questions should be moderately longer than beginner questions, covering fundamental content with additional context or clarifying details.
- **Advanced:** Questions should be relatively longer and more detailed, requiring a deep and nuanced understanding of the content, possibly involving multiple parts or detailed reasoning.

【Constraints】
- Each question must be in a multiple-choice format with options A through D.
- In the explanation, include not only the reason why the correct answer is correct but also explain why the other options are inappropriate by providing concrete evidence or quotes.
- The quiz content must be based on specific details and evidence found in the provided context information.
- Do NOT generate any questions related to the "purpose" or "impressions" of the reading notes, personal opinions, or any abstract/general statements.
  → These types of content must **never be generated**.

【Few-shot Examples】
Example 1 (General):
{{
  "content": "What does the idea 'Revolution is a result of accumulation' mean in a business context?",
  "options": {{
    "A": "To devise a unique strategy to avoid a single major failure",
    "B": "That small daily improvements eventually lead to significant change",
    "C": "That it is important to launch innovative products in a short period",
    "D": "That once a business plan is set, it should never be changed"
  }},
  "answer": "B",
  "explanation": "Option B is correct because the text states that revolution does not occur overnight but is the result of continuous, incremental improvements. Option A focuses on avoiding a major failure rather than cumulative improvement. Option C emphasizes rapid market introduction, which does not reflect continuous improvement. Option D contradicts the concept of revolution by implying rigidity in business planning."
}}

Example 2 (General):
{{
  "content": "What is meant by 'Digital Transformation'?",
  "options": {{
    "A": "Transforming the entire business model by adopting new technologies",
    "B": "Maintaining existing business processes as they are",
    "C": "Simply updating IT systems to the latest versions",
    "D": "Refusing change to protect the organization’s traditions"
  }},
  "answer": "A",
  "explanation": "Option A is correct because digital transformation involves adopting new technologies to fundamentally change the business model. Option B suggests maintaining the status quo, which does not involve transformation. Option C limits the change to IT systems only, and does not encompass overall business model transformation. Option D implies resistance to change, which is contrary to the essence of digital transformation."
}}

Example 3 (General):
{{
  "content": "What does the statement 'Innovation involves taking risks' imply?",
  "options": {{
    "A": "That new ideas should only be implemented in a safe manner",
    "B": "That not all innovations guarantee profit",
    "C": "That risk should be avoided by maintaining the status quo",
    "D": "That new ideas carry a possibility of failure, which can be a stepping stone to success"
  }},
  "answer": "D",
  "explanation": "Option D is correct because the text explains that innovation involves the risk of failure, but such risks provide valuable learning experiences that lead to success. Option A overemphasizes safety and denies the essence of risk-taking. Option C advocates for avoiding risk entirely, which does not reflect the innovative process. Option B focuses solely on profit guarantee and does not adequately address the value of risk-taking."
}}

【Additional Few-shot Examples by Difficulty】

- **Beginner Example:**
{{
  "content": "What is the main subject discussed in the provided reading note?",
  "options": {{
    "A": "A detailed analysis of financial data",
    "B": "The central theme of the reading note",
    "C": "A review of a novel",
    "D": "Personal opinions about a movie"
  }},
  "answer": "B",
  "explanation": "Option B is correct because the reading note focuses on presenting a central theme based on specific details in the text. Options A, C, and D are not supported by the context information."
}}

- **Intermediate Example:**
{{
  "content": "Based on the reading note, which statement best summarizes the author's perspective on digital innovation?",
  "options": {{
    "A": "Digital innovation is solely about upgrading technology.",
    "B": "Digital innovation involves integrating new technologies to transform business processes.",
    "C": "Digital innovation means keeping traditional methods while using new tech.",
    "D": "Digital innovation is irrelevant in today's market."
  }},
  "answer": "B",
  "explanation": "Option B is correct because the context indicates that digital innovation is about integrating new technologies to transform overall business processes. Option A oversimplifies the concept, Option C contradicts the transformative aspect, and Option D is clearly off-topic."
}}

- **Advanced Example:**
{{
  "content": "Considering the detailed nuances in the provided text, how does the concept of 'accumulated innovation' relate to risk management in business strategy?",
  "options": {{
    "A": "It suggests that innovation eliminates risk completely.",
    "B": "It implies that risk management is unnecessary when continuous improvements are made.",
    "C": "It indicates that incremental improvements help manage risks by learning from small failures.",
    "D": "It shows that risks should always be avoided in business."
  }},
  "answer": "C",
  "explanation": "Option C is correct because the concept of accumulated innovation implies that small, incremental improvements allow businesses to manage risks by learning from minor failures, rather than attempting to eliminate risk completely (as in Option A) or ignoring risk management altogether (as in Options B and D)."
}}

【NG Patterns (Do Not Generate)】
1. Questions like “What kind of person reads this book?” or those about the reader’s purpose should never be generated, as they do not provide meaningful assessments of comprehension.
2. Questions containing phrases such as “Thank you for reading until the end” or closing greetings should be excluded.
3. Do not generate questions based on subjective opinions or personal impressions.
4. Avoid generating abstract or general questions that are not directly based on specific evidence or details from the context information.
   → These types of content must **never be generated**.

Generate the quiz using the provided context information following the above constraints and examples.

    """

    try:
        res = rag_chain.invoke(question)
        print(res)

        quiz_response = res
    finally:
        shutil.rmtree(unique_dir)

    # TODO: 例外処理やエラーハンドリングを実装する

    return quiz_response


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
