from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class NovaTarefa(BaseModel):
    nome: str
    descricao: str


tarefas = []


@app.post("/tarefas")
def adicionar_tarefa(tarefa: NovaTarefa):
    nova_tarefa_dict = {
        "nome": tarefa.nome,
        "descricao": tarefa.descricao,
        "concluida": False
    }
    tarefas.append(nova_tarefa_dict)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": nova_tarefa_dict}


@app.get("/tarefas")
def listar_tarefas():
    return tarefas


@app.put("/tarefas/{nome_da_tarefa}")
def concluir_tarefa(nome_da_tarefa: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome_da_tarefa:
            tarefa["concluida"] = True
            return {"mensagem": "Tarefa marcada como concluída!", "tarefa": tarefa}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")


@app.delete("/tarefas/{nome_da_tarefa}")
def remover_tarefa(nome_da_tarefa: str):
    for i, tarefa in enumerate(tarefas):
        if tarefa["nome"] == nome_da_tarefa:
            del tarefas[i]
            return {"mensagem": f"Tarefa '{nome_da_tarefa}' removida com sucesso!"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
