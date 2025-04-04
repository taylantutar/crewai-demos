from crewai_tools import BaseTool
import os

class FileWriteTool(BaseTool):
    name: str = "File Write Tool"
    description: str = "Writes provided text content to a specified file. Overwrites the file if it exists."

    def _run(self, file_path: str, text_content: str) -> str:
        """
        Writes the given text content to the specified file path.
        Args:
            file_path (str): The path to the file where the content will be written.
            text_content (str): The text content to write to the file.
        Returns:
            str: A confirmation message indicating success or failure.
        """
        try:
            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            return f"Content successfully written to {file_path}"
        except Exception as e:
            return f"Error writing to file {file_path}: {e}"
