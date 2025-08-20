from utilities.QualityEvaluation import ResponseQualityEvaluator
import pandas as pd

def evaluate_score_for_chatbot(model_evaluate = "mistral:7b", input_file= "",output_file=""):
    evaluator = ResponseQualityEvaluator(
        ollama_host="http://localhost:11434",
        model_name= model_evaluate,  # Change to your preferred model
        temperature=0.1
    )
    df =  pd.read_excel(input_file)
    data = df.to_dict('records')
    ret = []
    for data_record in data:
        data_ret = data_record.copy()
        paragraph_context = data_record['context']
        expected_response = data_record['expected_result']
        actual_response = data_record['actual_answer']
        question = data_record['question']
        # Evaluate the response
        result = evaluator.evaluate(
            actual_response=actual_response,
            expected_response=expected_response,
            paragraph_context=paragraph_context,
            question=question
        )
        data_ret['overall_score'] = result.overall_score
        data_ret['relevant'] = result.relevance_score
        data_ret['accuracy'] = result.accuracy_score
        data_ret['completeness'] = result.coherence_score
        data_ret['similarity'] = result.similarity_score
        data_ret['feed_back'] = result.detailed_feedback
        suggestion_str = ""
        for i, suggestion in enumerate(result.suggestions, 1):
            suggestion_str = suggestion + str(i) + "." + suggestion
        data_ret['suggestion'] = suggestion
        ret.append(data_ret)
    df_ret = pd.DataFrame(ret)
    df_ret.to_excel(output_file)





