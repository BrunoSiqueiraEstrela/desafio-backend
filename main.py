import uvicorn
from libs.variaveis.gerenciador_de_env import ENVS

if __name__ == "__main__":
    HOST: str = ENVS.HOST
    PORT: int = ENVS.PORT

    uvicorn.run("servidor.config:app", host=HOST, port=PORT, reload=True)
