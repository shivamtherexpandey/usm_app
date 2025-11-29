from langchain_community.document_loaders import WebBaseLoader
from langchain_classic.chains import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential
from config import Config


class SummaryTool:
    def __init__(self, url: str):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.SUMMARIZATION_LLM_MODEL,
            temperature=0,
            api_key=Config.LLM_API_KEY,
        )
        self.method = "map_reduce"
        self.document = self.document_loader(url)
        self.summarizer = load_summarize_chain

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def document_loader(self, url: str):
        loader = WebBaseLoader(url)
        return loader.load()

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def summarize(self):
        summary = self.summarizer(
            self.llm, chain_type=self.method, token_max=1000
        ).invoke(self.document)
        return summary["output_text"]
