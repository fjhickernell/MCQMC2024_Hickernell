import re
import os

def find_pdf_files_in_latex(latex_file):
    """
    Scans a LaTeX file to find PDF files included in the document.

    Args:
        latex_file (str): Path to the LaTeX file.

    Returns:
        list: A list of PDF file names found in the LaTeX file.
    """
    pdf_files = []

    # Regular expression to capture \includegraphics{file.pdf} or \includegraphics[options]{file.pdf}
    graphics_regex = re.compile(r"\\includegraphics(?:\[.*?\])?\{(.*?\.pdf)\}")

    try:
        with open(latex_file, 'r', encoding='utf-8') as file:
            for line in file:
                matches = graphics_regex.findall(line)
                if matches:
                    pdf_files.extend(matches)
    except FileNotFoundError:
        print(f"Error: File '{latex_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    #return pdf_files
    return sorted(pdf_files)

# Example usage
if __name__ == "__main__":
    # Specify the path to your LaTeX file
    latex_file_path = "HickernellMCQMC2024_QMCTutorial.tex"

    # Find and print the PDF files included in the LaTeX file
    pdf_files = find_pdf_files_in_latex(latex_file_path)
    if pdf_files:
        print("PDF files used in the LaTeX file:")
        for pdf in pdf_files:
            print(pdf)
    else:
        print("No PDF files found in the LaTeX file.")
