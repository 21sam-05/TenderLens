from generation_service import generate_answer
context="""
Financial capacity:
The bidder must have an annual turnover of at least INR 2 crore during the specific period"""

question="What is the minimum annual turnover required"

answer=generate_answer(
    question=question,
    context=context
)

print("ANSWER:")
print(answer)

