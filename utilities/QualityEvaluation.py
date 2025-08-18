import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityMetric(Enum):
    """Enumeration of quality metrics"""
    RELEVANCE = "relevance"
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    COHERENCE = "coherence"
    SIMILARITY = "similarity"


@dataclass
class EvaluationResult:
    """Data class to store evaluation results"""
    overall_score: float
    relevance_score: float
    accuracy_score: float
    completeness_score: float
    coherence_score: float
    similarity_score: float
    detailed_feedback: str
    suggestions: List[str]

    def to_dict(self) -> Dict:
        """Convert evaluation result to dictionary"""
        return {
            "overall_score": self.overall_score,
            "metrics": {
                "relevance": self.relevance_score,
                "accuracy": self.accuracy_score,
                "completeness": self.completeness_score,
                "coherence": self.coherence_score,
                "similarity": self.similarity_score
            },
            "detailed_feedback": self.detailed_feedback,
            "suggestions": self.suggestions
        }


class ResponseQualityEvaluator:
    """
    A class to evaluate the quality of chatbot responses using Ollama LLM.

    This evaluator compares actual responses against expected responses and
    paragraph context to provide comprehensive quality metrics.
    """

    def __init__(
            self,
            ollama_host: str = "http://localhost:11434",
            model_name: str = "llama2",
            temperature: float = 0.1,
            max_retries: int = 3
    ):
        """
        Initialize the Response Quality Evaluator.

        Args:
            ollama_host: URL of the Ollama server
            model_name: Name of the Ollama model to use (e.g., 'llama2', 'mistral', 'phi')
            temperature: Temperature for LLM responses (lower = more deterministic)
            max_retries: Maximum number of retry attempts for API calls
        """
        self.ollama_host = ollama_host
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.api_endpoint = f"{ollama_host}/api/generate"

        # Verify Ollama connection
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verify connection to Ollama server"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            if response.status_code == 200:
                logger.info(f"Successfully connected to Ollama at {self.ollama_host}")
            else:
                raise ConnectionError(f"Failed to connect to Ollama: {response.status_code}")
        except Exception as e:
            logger.error(f"Error connecting to Ollama: {e}")
            raise

    def _call_ollama(self, prompt: str) -> str:
        """
        Make a call to Ollama API.

        Args:
            prompt: The prompt to send to the model

        Returns:
            The model's response as a string
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": self.temperature,
            "stream": False
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    return response.json().get("response", "")
                else:
                    logger.warning(f"Attempt {attempt + 1} failed: {response.status_code}")

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed with error: {e}")

        raise RuntimeError(f"Failed to get response from Ollama after {self.max_retries} attempts")

    def _create_evaluation_prompt(
            self,
            actual_response: str,
            expected_response: str,
            paragraph_context: str,
            question: Optional[str] = None
    ) -> str:
        """
        Create a comprehensive evaluation prompt for the LLM.

        Args:
            actual_response: The response from the chatbot
            expected_response: The expected/ideal response
            paragraph_context: The context paragraph containing the answer
            question: Optional original question

        Returns:
            A formatted prompt string
        """
        prompt = f"""You are an expert evaluator assessing the quality of a chatbot's response.

CONTEXT PARAGRAPH:
{paragraph_context}

{f"ORIGINAL QUESTION: {question}" if question else ""}

EXPECTED RESPONSE:
{expected_response}

ACTUAL RESPONSE FROM CHATBOT:
{actual_response}
あなたは日本語の専門家です。以下の基準に基づいて、回答の品質を評価してください。
  関連性：質問と回答の内容、文脈、および期待される回答との適合性を評価し、0〜10点で採点する。
  正確性：質問と文脈に基づいた回答の正確さを評価する（不必要に短すぎたり、長すぎて要点から外れる回答を避ける）。0〜10点で採点する。
  網羅性：回答が文脈内の重要なポイントをすべてカバーしているかを評価し、0〜10点で採点する。
  明確さ：回答が分かりやすく、構造が明確であるかを評価し、0〜10点で採点する。
  期待回答との類似度：回答が期待される回答とどの程度類似しているか（同義語の使用は許容する）。0〜10点で採点する。

回答の品質を評価は JSON format:
{{
    "関連性なスコア": <スコア>,
    "正確性なスコア": <スコア>,
    "網羅性なスコア": <スコア>,
    "明確さスコア": <スコア>,
    "期待回答との類似度なスコア": <スコア>,
    "詳細なフィードバック": "<強みと弱みの詳細な説明>",
    "お勧め": ["<お勧め 1>", "<お勧め 2>", ...]
}}

評価は客観的かつ正確に行ってください. 有効なJSONのみを返してください。"""

        return prompt

    def _parse_evaluation_response(self, response: str) -> Dict:
        """
        Parse the LLM's evaluation response.

        Args:
            response: Raw response from the LLM

        Returns:
            Parsed evaluation dictionary
        """
        try:
            # Try to extract JSON from the response
            # Sometimes LLMs add extra text before/after JSON
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Return default scores if parsing fails
            return {
                "relevance_score": 5.0,
                "accuracy_score": 5.0,
                "completeness_score": 5.0,
                "coherence_score": 5.0,
                "similarity_score": 5.0,
                "detailed_feedback": "Error parsing evaluation response",
                "suggestions": ["Unable to parse LLM response"]
            }

    def evaluate(
            self,
            actual_response: str,
            expected_response: str,
            paragraph_context: str,
            question: Optional[str] = None,
            weights: Optional[Dict[str, float]] = None
    ) -> EvaluationResult:
        """
        Evaluate the quality of a chatbot response.

        Args:
            actual_response: The response from the chatbot
            expected_response: The expected/ideal response
            paragraph_context: The context paragraph containing the answer
            question: Optional original question
            weights: Optional dictionary of weights for each metric (default: equal weights)

        Returns:
            EvaluationResult object containing scores and feedback
        """
        # Default weights if not provided
        if weights is None:
            weights = {
                "relevance": 0.25,
                "accuracy": 0.25,
                "completeness": 0.2,
                "coherence": 0.15,
                "similarity": 0.15
            }

        # Create and send evaluation prompt
        prompt = self._create_evaluation_prompt(
            actual_response,
            expected_response,
            paragraph_context,
            question
        )

        logger.info("Sending evaluation request to Ollama...")
        llm_response = self._call_ollama(prompt)

        # Parse the response
        evaluation = self._parse_evaluation_response(llm_response)

        # Extract scores (normalize to 0-1 range)
        relevance = evaluation.get("relevance_score", 5) / 10
        accuracy = evaluation.get("accuracy_score", 5) / 10
        completeness = evaluation.get("completeness_score", 5) / 10
        coherence = evaluation.get("coherence_score", 5) / 10
        similarity = evaluation.get("similarity_score", 5) / 10

        # Calculate weighted overall score
        overall_score = (
                weights["relevance"] * relevance +
                weights["accuracy"] * accuracy +
                weights["completeness"] * completeness +
                weights["coherence"] * coherence +
                weights["similarity"] * similarity
        )

        # Create evaluation result
        result = EvaluationResult(
            overall_score=round(overall_score, 3),
            relevance_score=round(relevance, 3),
            accuracy_score=round(accuracy, 3),
            completeness_score=round(completeness, 3),
            coherence_score=round(coherence, 3),
            similarity_score=round(similarity, 3),
            detailed_feedback=evaluation.get("detailed_feedback", ""),
            suggestions=evaluation.get("suggestions", [])
        )

        logger.info(f"Evaluation completed. Overall score: {result.overall_score}")

        return result

    def batch_evaluate(
            self,
            evaluations: List[Dict[str, str]],
            weights: Optional[Dict[str, float]] = None
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple responses in batch.

        Args:
            evaluations: List of dictionaries containing actual_response,
                        expected_response, paragraph_context, and optionally question
            weights: Optional dictionary of weights for each metric

        Returns:
            List of EvaluationResult objects
        """
        results = []

        for i, eval_data in enumerate(evaluations, 1):
            logger.info(f"Evaluating response {i}/{len(evaluations)}...")

            result = self.evaluate(
                actual_response=eval_data["actual_response"],
                expected_response=eval_data["expected_response"],
                paragraph_context=eval_data["paragraph_context"],
                question=eval_data.get("question"),
                weights=weights
            )

            results.append(result)

        return results

    def get_improvement_suggestions(
            self,
            actual_response: str,
            expected_response: str,
            paragraph_context: str
    ) -> List[str]:
        """
        Get specific improvement suggestions for a response.

        Args:
            actual_response: The response from the chatbot
            expected_response: The expected/ideal response
            paragraph_context: The context paragraph

        Returns:
            List of improvement suggestions
        """
        prompt = f"""Compare the actual response with the expected response and context.

CONTEXT: {paragraph_context}

EXPECTED: {expected_response}

ACTUAL: {actual_response}

Provide 3-5 specific, actionable suggestions to improve the actual response.
Format as a JSON array of strings: ["suggestion1", "suggestion2", ...]"""

        response = self._call_ollama(prompt)

        try:
            # Extract JSON array from response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1

            if start_idx != -1 and end_idx > start_idx:
                suggestions = json.loads(response[start_idx:end_idx])
                return suggestions
            else:
                return ["Unable to generate suggestions"]

        except Exception as e:
            logger.error(f"Error parsing suggestions: {e}")
            return ["Error generating suggestions"]


# Example usage
if __name__ == "__main__":
    # Initialize evaluator
    evaluator = ResponseQualityEvaluator(
        ollama_host="http://localhost:11434",
        model_name="mistral:7b",  # Change to your preferred model
        temperature=0.1
    )

    # Example evaluation
    paragraph_context = """
    Python is a high-level, interpreted programming language known for its 
    simplicity and readability. It was created by Guido van Rossum and first 
    released in 1991. Python supports multiple programming paradigms including 
    procedural, object-oriented, and functional programming. It has a large 
    standard library and is widely used in web development, data science, 
    artificial intelligence, and automation.
    """

    expected_response = """
    Python is a high-level, interpreted programming language created by 
    Guido van Rossum in 1991. It's known for its simplicity, readability, 
    and support for multiple programming paradigms. Python is widely used 
    in web development, data science, and AI.
    """

    actual_response = """
    Python is a programming language that is easy to learn. It can be used 
    for many things like making websites and analyzing data.
    """

    question = "What is Python and what are its main characteristics?"

    # Evaluate the response
    result = evaluator.evaluate(
        actual_response=actual_response,
        expected_response=expected_response,
        paragraph_context=paragraph_context,
        question=question
    )

    # Print results
    print("\n=== EVALUATION RESULTS ===")
    print(f"Overall Score: {result.overall_score:.2%}")
    print(f"\nDetailed Metrics:")
    print(f"  - Relevance: {result.relevance_score:.2%}")
    print(f"  - Accuracy: {result.accuracy_score:.2%}")
    print(f"  - Completeness: {result.completeness_score:.2%}")
    print(f"  - Coherence: {result.coherence_score:.2%}")
    print(f"  - Similarity: {result.similarity_score:.2%}")
    print(f"\nFeedback: {result.detailed_feedback}")
    print(f"\nSuggestions:")
    for i, suggestion in enumerate(result.suggestions, 1):
        print(f"  {i}. {suggestion}")