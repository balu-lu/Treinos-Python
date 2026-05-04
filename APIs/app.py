from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


tarefas: list[Tarefa] = []


@app.post("/tarefas")
def adicionar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": tarefa}


@app.get("/tarefas")
def listar_tarefas():
    return tarefas


@app.put("/tarefas/{nome_da_tarefa}")
def concluir_tarefa(nome_da_tarefa: str):
    for t in tarefas:
        if t.nome == nome_da_tarefa:
            t.concluida = True
            return {"mensagem": "Tarefa marcada como concluída!", "tarefa": t}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")


@app.delete("/tarefas/{nome_da_tarefa}")
def remover_tarefa(nome_da_tarefa: str):
    for i, t in enumerate(tarefas):
        if t.nome == nome_da_tarefa:
            del tarefas[i]
            return {"mensagem": f"Tarefa '{nome_da_tarefa}' removida com sucesso!"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
