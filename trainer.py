import os

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

from chat_core.trainer import embeddings, FAISSHelper


def scan_directory():
    directory = 'data'
    if not os.path.exists(directory):
        print(f"Thư mục '{directory}' không tồn tại.")
        return

    for root, dirs, files in os.walk(directory):
        return dirs


# Gọi hàm scan_d
# irectory với đường dẫn thư mục '/data'
all_dict = scan_directory()

for i in all_dict:
    pdf_loader = DirectoryLoader(f"data/{i}", glob="*.pdf", loader_cls=PyPDFLoader)
    FAISSHelper.create_db_from_files(loaders=[pdf_loader], embeddings_model=embeddings, character_name=i)
