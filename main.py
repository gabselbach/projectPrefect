from src.flows.card_flows import project
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

if __name__ == "__main__":
    project(name="first-deployment")