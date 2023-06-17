import re

class Formatter:
    def __init__(self, book_info, cleaned, book_suggestions):
        self.book_info = book_info
        self.cleaned = cleaned
        self.book_suggestions = book_suggestions
    
    def format_link(self):
        pass

    def format_header(self):
        pass

    def format_description(self):
        pass

    def format_book_footer(self):
        pass

    def supports_long_version(self):
        return True
    
    def get_section_separator(self):
        return '\n\n'
class LiteFormatter(Formatter):
    def format_link(self):
        title = self.book_info["title"]
        url = self.book_info["url"]

        return "[**%s**](%s)" % (title, url)

    def format_header(self):
        year = self.book_info["pub_year"]
        authors = ", ".join(self.book_info["authors"])

        return self.get_section_separator() + "^(By: %s | Published: %s)" % (
            authors, year or "?")

    def format_book_footer(self):
        return ""
    
    def supports_long_version(self):
        return False
    
    def get_section_separator(self):
        return '\n'
class DefaultFormatter(Formatter):
    def format_link(self):
        title = self.book_info["title"]
        url = self.book_info["url"]

        return "[**%s**](%s)" % (title, url)

    def format_header(self):
        pages = self.book_info["num_pages"]
        year = self.book_info["pub_year"]
        shelves = ", ".join(self.book_info["shelves"])
        authors = ", ".join(self.book_info["authors"])

        return "^(By: %s | %s pages | Published: %s | Popular Shelves: %s)" % (
            authors, pages or "?", year or "?", shelves)

    def format_description(self):
        description = self.book_info["description"]
        if description is None:
            return ""
        description = re.sub('<.*?>', '', description.replace("<br />", "\n"))

        chunks = [">" + chunk for chunk in description.split("\n")]

        return "\n".join(chunks)

    def format_book_footer(self):
        s = "s" if self.book_suggestions > 1 else ""
        return "^(This book has been suggested %s time%s)" % (self.book_suggestions, s)

class FormatterFactory:
    @staticmethod
    def for_subreddit(subreddit_name, book_info, cleaned, book_suggestions):
        print("building formatter for: " + subreddit_name.lower())
        if subreddit_name.lower() == "romancebooks":
            return LiteFormatter(
                    book_info=book_info,
                    cleaned=cleaned)
        elif subreddit_name.lower() == "test":
            return LiteFormatter(
                book_info=book_info,
                cleaned=cleaned)
        else:
            return DefaultFormatter(
                    book_info=book_info,
                    cleaned=cleaned,
                   )