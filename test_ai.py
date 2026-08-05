from app.services.ai_service import analyze_complaint

response = analyze_complaint(
    "The tablets were broken inside the blister pack."
)

print(response)