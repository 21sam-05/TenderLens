
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rag_service import answer_question

question="What is the minimum annual turnover required"

result=answer_question(
    question=question,
    tender_id=4,
    top_k=5
)

print("\n==========RAG ANSWER===========\n")
print(result["answer"])

print("\n==============SOURCES===========\n")
for source in result["sources"]:
    print(source)

