from typing import AnyStr
from gentopia.tools.basetool import *
from pypdf import PdfReader
import io
import requests

class PDFUrlArgs(BaseModel):
    pdf_url: str = Field(..., description="URL of the PDF file.")

class PDFReader(BaseTool):
    """Tool that extracts text from a PDF file given its URL."""
    
    name = "read_pdf"
    description = "A tool to extract text from a PDF file given its URL."

    args_schema: Optional[Type[BaseModel]] = PDFUrlArgs

    def _run(self, pdf_url: AnyStr) -> str:
        try:
            # Convert remote pdf to something we can work with (bytes)
            response = requests.get(pdf_url)
            pdf_content = response.content
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            text = ""

            # Scrape text out of pdf and concatenate on to text string
            for page_num in range(0, len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text
        
        except Exception as e:
            return f"Error: {e}\n Invalid PDF address."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = PDFReader()._run(" https://myperfectwords.com/blog/500-word-essay/500-word-essay-sample.pdf") # random pdf to read
    print(ans)
