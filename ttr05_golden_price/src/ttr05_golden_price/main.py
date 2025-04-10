#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ttr05_golden_price.crew import Ttr05GoldenPrice

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    
    urls_input = input("Lütfen altın fiyatlarını çekmek istediğiniz web sitelerinin URL'lerini virgülle ayırarak girin:\n")
    website_urls = [url.strip() for url in urls_input.split(',')]

    inputs = {
        'website_urls': website_urls
    }
    
    try:
        Ttr05GoldenPrice().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

