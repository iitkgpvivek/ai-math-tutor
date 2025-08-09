from local_llm_integration import LocalLLMGenerator

def test_variations():
    llm = LocalLLMGenerator()
    
    test_cases = [
        # Direct proportion
        "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?",
        
        # Inverse proportion
        "If 5 workers can complete a project in 12 days, how many days will it take for 8 workers?",
        
        # Ratio problem
        "The ratio of boys to girls in a class is 3:2. If there are 15 boys, how many girls are there?",
        
        # Work rate problem
        "Pipe A can fill a tank in 6 hours, and pipe B can fill it in 4 hours. How long will it take to fill the tank if both pipes are used together?",
        
        # Percentage problem
        "A shirt costs $40 after a 20% discount. What was the original price?"
    ]
    
    for problem in test_cases:
        print("\n" + "="*80)
        print("ORIGINAL PROBLEM:")
        print(problem)
        
        print("\nGENERATING VARIATIONS...")
        for i in range(2):  # Generate 2 variations per problem
            variation = llm.generate_math_variation(problem)
            print(f"\nVARIATION {i+1}:")
            print(variation["variation"])
            print("\nExplanation:")
            print(variation["explanation"])
            print("-" * 40)
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_variations()
