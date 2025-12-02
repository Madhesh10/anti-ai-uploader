from django.core.management.base import BaseCommand
from uploader.rag import RAGStore
from uploader.models import Document
from uploader.utils import extract_text_from_file
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Rebuilds FAISS index from all uploaded documents"

    def handle(self, *args, **options):
        index_path = os.path.join(settings.BASE_DIR, "faiss_index.index")
        meta_path = os.path.join(settings.BASE_DIR, "faiss_meta.npy")
        # create fresh RAGStore (drops previous memory)
        rag = RAGStore(dim=384, index_path=index_path, meta_path=meta_path)
        # reinitialize to empty
        rag.index = rag.index = rag.index = rag.index = rag.__class__(dim=rag.dim).__dict__.get('index', rag.index)
        rag.meta = []
        for doc in Document.objects.all():
            text = extract_text_from_file(doc.file.path)
            if text and text.strip():
                rag.add_document(doc.id, text)
        self.stdout.write(self.style.SUCCESS("Rebuilt FAISS index"))
