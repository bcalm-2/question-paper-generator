from openai import OpenAI
from backend.config import Config

print("API KEY:", Config.OPENAI_API_KEY)
client = OpenAI(api_key=Config.OPENAI_API_KEY)

class QuestionGeneratorService:

    @staticmethod
    def generate_questions(processed_text: str, num_questions: int = 5):
        try:
            prompt = f"""
            Generate {num_questions} exam questions from the following content.
            Include Bloom's Taxonomy levels.
            Return response in JSON format like:
            [
                {{
                    "question": "...",
                    "level": "...",
                    "type": "short/long/mcq"
                }}
            ]

            Content:
            {processed_text}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert exam paper generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return {
                "success": True,
                "data": response.choices[0].message.content
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
print("API KEY:", Config.OPENAI_API_KEY)
