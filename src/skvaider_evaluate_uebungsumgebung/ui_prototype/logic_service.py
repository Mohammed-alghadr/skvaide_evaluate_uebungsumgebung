import time
import uuid


class EvaluationLogicService:
    def __init__(self):
        self._evaluations = {}

    def start_evaluation(self, prompt_text):
        if not prompt_text or not prompt_text.strip():
            raise ValueError("Input text must not be empty.")

        cleaned_prompt = prompt_text.strip()
        eval_id = str(uuid.uuid4())[:8]
        self._evaluations[eval_id] = {
            "id": eval_id,
            "prompt": cleaned_prompt,
            "status": "queued",
            "started_at": time.perf_counter(),
            "metrics": None,
        }
        return {"id": eval_id, "status": "queued"}

    def get_status(self, eval_id):
        record = self._evaluations.get(eval_id)
        if not record:
            raise KeyError("Evaluation ID not found.")

        if record["status"] == "queued":
            record["status"] = "running"
        elif record["status"] == "running":
            elapsed = round(time.perf_counter() - record["started_at"], 2)
            word_count = len(record["prompt"].split())
            estimated_tokens = max(1, int(word_count * 1.3))

            record["status"] = "done"
            record["metrics"] = {
                "Relevanz": 0.92,
                "Halluzination": 0.05,
                "Korrektheit": 0.89,
                "Tokens": estimated_tokens,
                "Laufzeit": f"{elapsed}s",
            }

        return {
            "id": record["id"],
            "prompt": record["prompt"],
            "status": record["status"],
            "metrics": record["metrics"],
        }
