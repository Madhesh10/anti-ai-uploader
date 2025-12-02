# C:\Anti AI Uploader\uploader\views.py

from django.shortcuts import render, redirect
from .forms import DocumentForm, QueryForm
from .models import Document
from .deepseek_utils import (
    extract_text_from_file,
    upload_file_to_deepseek,
    ask_deepseek,
)


def home(request):
    docs = Document.objects.order_by("-uploaded_at")[:10]
    return render(request, "uploader/home.html", {"docs": docs})


def upload(request):
    """
    Upload a document and (optionally) send the raw file bytes to DeepSeek
    for RAG indexing via upload_file_to_deepseek().
    """
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()

            # Optional: push file to DeepSeek RAG index
            try:
                f = doc.file
                f.open("rb")
                resp = upload_file_to_deepseek(
                    f.read(),
                    f.name,
                    metadata={"doc_id": doc.id},
                )
                f.close()
                print("DeepSeek upload response:", resp)
            except Exception as e:
                print("DeepSeek upload error:", e)

            return redirect("uploader:home")
    else:
        form = DocumentForm()

    return render(request, "uploader/upload.html", {"form": form})


def query(request):
    """
    Collect text from all uploaded documents, send as 'context' to DeepSeek,
    and display only the assistant's answer.
    """
    result = None

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]

            # 1) collect text from all documents
            docs = Document.objects.order_by("-uploaded_at")
            context_parts = []

            for doc in docs:
                try:
                    f = doc.file
                    f.open("rb")
                    text = extract_text_from_file(f)
                    f.close()
                    if text:
                        # limit per file to avoid huge payloads
                        context_parts.append(text[:4000])
                except Exception as e:
                    print("Error extracting text from document", doc.id, e)

            context = "\n\n".join(context_parts)

            # 2) ask DeepSeek with question + context
            try:
                ai_response = ask_deepseek(question, context=context)
            except Exception as e:
                ai_response = {"error": str(e)}

            # 3) only show answer text to user
            if isinstance(ai_response, dict) and "result" in ai_response:
                result = ai_response["result"]
            else:
                result = str(ai_response)
    else:
        form = QueryForm()

    return render(request, "uploader/query.html", {"form": form, "result": result})
