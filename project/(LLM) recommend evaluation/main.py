from utils.evaluation import Evaluator
import pandas as pd

if __name__ == "__main__":
    evaluator = Evaluator()
    df = evaluator.get_test_data()
    evaluation_results = evaluator.run_evaluation(df, mode='test')