import requests
import json
from typing import Dict, Optional, List, Tuple
import time
import re
from collections import Counter


class OllamaChatbotScorer:
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initialize the scorer with Ollama settings.

        Args:
            model_name: The Ollama model to use (e.g., 'llama3.2', 'mistral', 'phi')
            base_url: The Ollama API base URL
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

        # Test connection
        self._test_connection()

    def _test_connection(self):
        """Test if Ollama is running and model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = [model['name'] for model in response.json().get('models', [])]
                if self.model_name not in models:
                    print(f"Warning: Model '{self.model_name}' not found. Available models: {models}")
                    print(f"Pull the model using: ollama pull {self.model_name}")
            else:
                print("Warning: Could not connect to Ollama. Make sure it's running.")
        except Exception as e:
            print(f"Warning: Ollama connection test failed: {e}")

    def _call_ollama(self, prompt: str) -> str:
        """Make a request to Ollama API."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")

    def extract_keywords(self, text: str, method: str = "auto") -> List[str]:
        """
        Extract keywords from text using various methods.

        Args:
            text: The text to extract keywords from
            method: "auto", "noun_phrases", "important_words", or "custom"

        Returns:
            List of keywords
        """
        if method == "auto":
            # Use Ollama to extract keywords
            prompt = f"""Extract the most important keywords and key phrases from the following text. 
            Return ONLY a JSON array of keywords, nothing else.

            Text: {text}

            Return format: ["keyword1", "keyword2", "key phrase 3", ...]"""

            try:
                response = self._call_ollama(prompt)
                keywords = json.loads(response)
                if isinstance(keywords, list):
                    return keywords
            except:
                pass

        # Fallback to simple extraction
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                      'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                      'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'it', 'this',
                      'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they'}

        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())

        # Filter out stop words and short words
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        # Get unique keywords while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords[:20]  # Return top 20 keywords

    def calculate_keyword_score(self,
                                actual_response: str,
                                expected_keywords: List[str],
                                case_sensitive: bool = False) -> Tuple[float, Dict]:
        """
        Calculate keyword matching score.

        Args:
            actual_response: The actual response text
            expected_keywords: List of expected keywords
            case_sensitive: Whether to do case-sensitive matching

        Returns:
            Tuple of (score, details)
        """
        if not expected_keywords:
            return 100.0, {"message": "No keywords to check"}

        # Prepare text for comparison
        if not case_sensitive:
            actual_lower = actual_response.lower()
            keywords_lower = [kw.lower() for kw in expected_keywords]
        else:
            actual_lower = actual_response
            keywords_lower = expected_keywords

        # Check keyword presence
        found_keywords = []
        missing_keywords = []
        partial_matches = []

        for i, keyword in enumerate(keywords_lower):
            original_keyword = expected_keywords[i]

            # Check for exact match
            if keyword in actual_lower:
                found_keywords.append(original_keyword)
            else:
                # Check for partial matches (e.g., singular/plural, substrings)
                partial_found = False
                for word in actual_lower.split():
                    if keyword in word or word in keyword:
                        partial_matches.append(f"{original_keyword} (partial: {word})")
                        partial_found = True
                        break

                if not partial_found:
                    missing_keywords.append(original_keyword)

        # Calculate score
        exact_matches = len(found_keywords)
        partial_match_count = len(partial_matches)
        total_keywords = len(expected_keywords)

        # Scoring: 100% for exact match, 50% for partial match
        score = (exact_matches * 100 + partial_match_count * 50) / total_keywords

        details = {
            "total_keywords": total_keywords,
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords,
            "partial_matches": partial_matches,
            "exact_match_count": exact_matches,
            "partial_match_count": partial_match_count,
            "coverage_percentage": (exact_matches / total_keywords) * 100
        }

        return score, details

    def score_response(self,
                       user_question: str,
                       actual_response: str,
                       expected_response: str,
                       criteria: Optional[Dict[str, float]] = None,
                       keywords: Optional[List[str]] = None,
                       auto_extract_keywords: bool = True,
                       keyword_matching_threshold: float = 80.0) -> Dict:
        """
        Score the actual response against the expected response using Ollama.

        Args:
            user_question: The original user question
            actual_response: The chatbot's actual response (P1)
            expected_response: The expected/ideal response (P2)
            criteria: Custom scoring criteria with weights (optional)
            keywords: List of important keywords that must be present
            auto_extract_keywords: If True and keywords not provided, extract from expected response
            keyword_matching_threshold: Minimum keyword score to pass (0-100)

        Returns:
            Dictionary containing scores and analysis
        """

        # Default scoring criteria with heavy weight on keywords
        if criteria is None:
            criteria = {
                "keyword_matching": 0.2,  # Heavy weight on keywords
                "accuracy": 0.4,
                "completeness": 0.15,
                "relevance": 0.1,
                "clarity": 0.05
            }
        elif "keyword_matching" not in criteria:
            # Add keyword matching if not present
            criteria["keyword_matching"] = 0.4
            # Normalize weights
            total = sum(criteria.values())
            criteria = {k: v / total for k, v in criteria.items()}

        # Extract keywords if not provided
        if keywords is None and auto_extract_keywords:
            keywords = self.extract_keywords(expected_response)

        # Calculate keyword score
        keyword_score = 100.0
        keyword_details = {}
        if keywords:
            keyword_score, keyword_details = self.calculate_keyword_score(
                actual_response, keywords
            )

        # Determine pass/fail based on keyword threshold
        keyword_pass = keyword_score >= keyword_matching_threshold

        # Create the scoring prompt
        prompt = f"""You are an expert evaluator for chatbot responses. Score the actual response against the expected response.

User Question: {user_question}

Expected Response (P2): {expected_response}

Actual Response (P1): {actual_response}

Keywords Found: {keyword_score:.1f}% (Required: {keyword_matching_threshold}%)
Keyword Test: {"PASS" if keyword_pass else "FAIL"}

Please evaluate the actual response based on these criteria:
1. Keyword Matching (weight: {criteria.get('keyword_matching', 0)}): Score is {keyword_score}/100
2. Accuracy (weight: {criteria.get('accuracy', 0)}): How factually correct is the response?
3. Completeness (weight: {criteria.get('completeness', 0)}): Does it cover key points?
4. Relevance (weight: {criteria.get('relevance', 0)}): How well does it address the question?
5. Clarity (weight: {criteria.get('clarity', 0)}): How clear and understandable is it?

Provide your evaluation as a valid JSON object with this exact structure:
{{
    "scores": {{
        "keyword_matching": {keyword_score},
        "accuracy": <number 0-100>,
        "completeness": <number 0-100>,
        "relevance": <number 0-100>,
        "clarity": <number 0-100>
    }},
    "weighted_total": <weighted average based on provided weights>,
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "suggestions": ["suggestion 1", "suggestion 2"],
    "summary": "brief overall assessment"
}}

Return ONLY valid JSON."""

        try:
            # Get response from Ollama
            response_text = self._call_ollama(prompt)

            # Parse JSON from response
            try:
                evaluation = json.loads(response_text)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    evaluation = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse JSON from Ollama response")

            # Ensure keyword score is included
            evaluation['scores']['keyword_matching'] = keyword_score

            # Recalculate weighted total
            scores = evaluation.get('scores', {})
            weighted_sum = sum(scores.get(k, 0) * v for k, v in criteria.items())
            evaluation['weighted_total'] = round(weighted_sum, 1)

            # Add test result
            evaluation['test_result'] = "PASS" if keyword_pass else "FAIL"
            evaluation['keyword_test_passed'] = keyword_pass

            # Add metadata
            evaluation['metadata'] = {
                'user_question': user_question,
                'actual_response_length': len(actual_response),
                'expected_response_length': len(expected_response),
                'criteria_weights': criteria,
                'model_used': self.model_name,
                'keywords_checked': keywords,
                'keyword_details': keyword_details,
                'keyword_threshold': keyword_matching_threshold
            }

            return evaluation

        except Exception as e:
            # Fallback error response
            return {
                "error": str(e),
                "scores": {
                    "keyword_matching": keyword_score,
                    **{k: 0 for k in criteria.keys() if k != 'keyword_matching'}
                },
                "weighted_total": keyword_score * criteria.get('keyword_matching', 0.5),
                "test_result": "PASS" if keyword_pass else "FAIL",
                "keyword_test_passed": keyword_pass,
                "strengths": [],
                "weaknesses": ["Error during evaluation"],
                "suggestions": ["Please check Ollama connection and try again"],
                "summary": f"Error during evaluation: {str(e)}",
                "metadata": {
                    'user_question': user_question,
                    'model_used': self.model_name,
                    'keyword_details': keyword_details
                }
            }

    def generate_report(self, evaluation: Dict) -> str:
        """Generate a human-readable report from evaluation results."""
        report = f"""
CHATBOT RESPONSE EVALUATION REPORT
================================

Model Used: {evaluation.get('metadata', {}).get('model_used', 'Unknown')}
Question: {evaluation.get('metadata', {}).get('user_question', 'N/A')}

TEST RESULT: {evaluation.get('test_result', 'UNKNOWN')}
{"=" * 30}

KEYWORD ANALYSIS:
-----------------"""

        keyword_details = evaluation.get('metadata', {}).get('keyword_details', {})
        if keyword_details:
            report += f"\n- Keywords Checked: {keyword_details.get('total_keywords', 0)}"
            report += f"\n- Keywords Found: {keyword_details.get('exact_match_count', 0)}"
            report += f"\n- Partial Matches: {keyword_details.get('partial_match_count', 0)}"
            report += f"\n- Coverage: {keyword_details.get('coverage_percentage', 0):.1f}%"
            report += f"\n- Threshold: {evaluation.get('metadata', {}).get('keyword_threshold', 80)}%"

            if keyword_details.get('found_keywords'):
                report += f"\n\nFound Keywords: {', '.join(keyword_details['found_keywords'])}"

            if keyword_details.get('missing_keywords'):
                report += f"\n\nMissing Keywords: {', '.join(keyword_details['missing_keywords'])}"

        report += "\n\nDETAILED SCORES:"
        report += "\n----------------"

        scores = evaluation.get('scores', {})
        weights = evaluation.get('metadata', {}).get('criteria_weights', {})

        for criterion, score in scores.items():
            weight = weights.get(criterion, 0)
            report += f"\n- {criterion.replace('_', ' ').title()}: {score}/100 (weight: {weight:.0%})"

        report += f"\n\nWEIGHTED TOTAL: {evaluation.get('weighted_total', 0):.1f}/100"

        report += "\n\nSTRENGTHS:"
        strengths = evaluation.get('strengths', [])
        if strengths:
            for strength in strengths:
                report += f"\n• {strength}"
        else:
            report += "\n• No strengths identified"

        report += "\n\nWEAKNESSES:"
        weaknesses = evaluation.get('weaknesses', [])
        if weaknesses:
            for weakness in weaknesses:
                report += f"\n• {weakness}"
        else:
            report += "\n• No weaknesses identified"

        report += "\n\nSUGGESTIONS FOR IMPROVEMENT:"
        suggestions = evaluation.get('suggestions', [])
        if suggestions:
            for suggestion in suggestions:
                report += f"\n• {suggestion}"
        else:
            report += "\n• No suggestions provided"

        report += f"\n\nSUMMARY: {evaluation.get('summary', 'N/A')}"

        if 'error' in evaluation:
            report += f"\n\nERROR: {evaluation['error']}"

        return report






if __name__ == "__main__":
    # Initialize the scorer
    scorer = OllamaChatbotScorer(model_name="llama3.2:latest")

    # Example 1: With manual keywords
    print("=== Example 1: Manual Keywords ===")
    user_question = "What are the benefits of regular exercise?"

    actual_response = """
    Regular exercise has several benefits including improved cardiovascular health,
    better mood, and increased energy levels. It can also help with weight management.
    """

    expected_response = """
    Regular exercise provides numerous benefits:
    1. Physical health: Improves cardiovascular fitness, strengthens muscles and bones,
       helps maintain healthy weight, and boosts immune system.
    2. Mental health: Reduces stress, anxiety, and depression; improves mood through
       endorphin release; enhances cognitive function and memory.
    3. Sleep quality: Promotes better sleep patterns and deeper rest.
    4. Energy levels: Increases overall energy and reduces fatigue.
    5. Longevity: Associated with reduced risk of chronic diseases and increased lifespan.
    """

    # Define important keywords that MUST be present
    keywords = [
        "cardiovascular", "muscles", "bones", "weight", "immune system",
        "stress", "anxiety", "depression", "mood", "cognitive",
        "sleep", "energy", "chronic diseases", "longevity"
    ]

    # Score with heavy keyword weighting
    evaluation = scorer.score_response(
        user_question=user_question,
        actual_response=actual_response,
        expected_response=expected_response,
        keywords=keywords,
        keyword_matching_threshold=70.0  # Must have at least 70% of keywords
    )

    # Print results
    print(scorer.generate_report(evaluation))

    # Example 2: Auto-extract keywords
    print("\n\n=== Example 2: Auto-extracted Keywords ===")

    test_case = {
        "question": "Explain the water cycle",
        "actual": "Water evaporates from oceans and lakes, forms clouds, and falls as rain.",
        "expected": "The water cycle involves evaporation from water bodies, condensation in the atmosphere forming clouds, precipitation as rain or snow, and collection in rivers, lakes, and oceans. This continuous process is driven by solar energy.",
    }

    # Let the system extract keywords automatically
    evaluation2 = scorer.score_response(
        user_question=test_case["question"],
        actual_response=test_case["actual"],
        expected_response=test_case["expected"],
        auto_extract_keywords=True,
        keyword_matching_threshold=60.0
    )

    print(scorer.generate_report(evaluation2))

    # Example 3: Team-style pass/fail with custom criteria
    print("\n\n=== Example 3: Team Criteria (Keyword-Heavy) ===")

    # Your team's custom criteria - keywords are most important!
    team_criteria = {
        "keyword_matching": 0.7,  # 70% weight on keywords!
        "accuracy": 0.15,
        "completeness": 0.1,
        "relevance": 0.05
    }

    actual = "Machine learning uses algorithms and data to make predictions."
    expected = "Machine learning is a subset of artificial intelligence that uses statistical algorithms to analyze data patterns and make predictions without explicit programming."

    # Keywords your team considers critical
    critical_keywords = ["artificial intelligence", "statistical", "algorithms", "data", "patterns", "predictions"]

    evaluation3 = scorer.score_response(
        user_question="What is machine learning?",
        actual_response=actual,
        expected_response=expected,
        criteria=team_criteria,
        keywords=critical_keywords,
        keyword_matching_threshold=80.0  # Strict: need 80% keywords to pass
    )

    print(scorer.generate_report(evaluation3))
    print(f"\n{'=' * 50}")
    print(f"FINAL VERDICT: {evaluation3['test_result']}")
    print(f"{'=' * 50}")