import requests
import subprocess
import time

def check_and_pull_model(model_name="mistral"):
    """Check if the model is available, and pull it if not."""
    try:
        # Check if server is running
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                print("Starting Ollama server...")
                subprocess.Popen(["ollama", "serve"], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
                time.sleep(5)  # Give it time to start
                
                # Check again after starting
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code != 200:
                    print("❌ Failed to start Ollama server")
                    return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to Ollama server: {e}")
            return False
            
        # Check if model is available
        models = response.json().get('models', [])
        if any(model['name'].startswith(f"{model_name}:") for model in models):
            print(f"✅ Model '{model_name}' is already available")
            return True
            
        # Pull the model if not available
        print(f"Model '{model_name}' not found. Pulling... (This may take a few minutes)")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"✅ Successfully pulled model '{model_name}'")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to pull model: {e}")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False

if __name__ == "__main__":
    print("Checking for Mistral model...")
    if check_and_pull_model("mistral"):
        print("\nMistral is ready to use with the worksheet generator!")
        print("You can now run the worksheet generator with Mistral as the default model.")
    else:
        print("\nFailed to set up Mistral. Please check the error messages above.")
