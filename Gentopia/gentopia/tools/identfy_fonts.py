from typing import AnyStr
import requests
from bs4 import BeautifulSoup
from gentopia.tools.basetool import *


class URLArgs(BaseModel):
    url: str = Field(..., description="a web url to visit. You must make sure that the url is real and correct.")


class IDFonts(BaseTool):
    """Tool that adds the capability to name fonts on a webpage."""

    name = "identify_fonts"
    description = "A tool to identify what fonts are on a web page."

    args_schema: Optional[Type[BaseModel]] = URLArgs

    def _run(self, url: AnyStr) -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            #Create way to keep track of font types + counter
            font_counts: Dict[str, int] = {}

            # Find all elements with CSS attributes
            text_elements = soup.find_all(style=True)
           
            # Parse all text elements to get fonts
            for element in text_elements: 
                style = element['style']
                if 'font-family' in style:
                    # Extract font-family CSS attribute value
                    font_family = element.get('style').split('font-family:')[-1].split(';')[0].strip()
                
                    # Remove surrounding quotes
                    font_family = font_family.strip("'").strip('"')
                
                    # Count occurrences of font family
                    if font_family in font_counts:
                        font_counts[font_family] += 1
                    else:
                        font_counts[font_family] = 1
            response = ""
            return response.join(font_counts.keys())    
        except Exception as e:
            return f"Error: {e}\n Invalid URL"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = WebPage()._run("https://nlp.cs.gmu.edu/")
    print(ans)
