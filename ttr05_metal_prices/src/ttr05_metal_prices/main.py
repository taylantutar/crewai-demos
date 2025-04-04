#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ttr05_metal_prices.crew import Ttr05MetalPrices

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# It will automatically interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    urls = []
    print("Lütfen altın ve gümüş fiyatlarını kontrol etmek istediğiniz web sitelerinin tam adreslerini (URL) girin.")
    print("Girişi bitirmek için boş bir satır bırakıp Enter'a basın.")
    while True:
        url = input("URL: ")
        if not url:
            break
        urls.append(url)

    if not urls:
        print("Hiç URL girilmedi. Çıkılıyor.")
        sys.exit(1)

    inputs = {
        'website_urls': urls,
        'output_filename': 'metal_prices_report.txt' # Define the output filename
    }
    
    try:
        Ttr05MetalPrices().crew().kickoff(inputs=inputs)
        print(f"\nİşlem tamamlandı. Rapor '{inputs['output_filename']}' dosyasına kaydedildi.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Ttr05MetalPrices().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Ttr05MetalPrices().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Ttr05MetalPrices().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
