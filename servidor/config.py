import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from libs.database.carregar_orm import carregar_tabelas
from libs.dominio.barramento import Barramento

app = FastAPI(title="API de Tarefas", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def docs():
    return RedirectResponse(url="/docs")


# Cadastrar middleware
@app.middleware("tempo_de_resposta")
async def add_tempo_de_resposta(request: Request, call_next):
    timer_inicial = time.time()
    resposta = await call_next(request)
    tempo_de_processamento = time.time() - timer_inicial
    resposta.headers["X-Process-Time"] = str(tempo_de_processamento)
    return resposta


def registrar_rotas():
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import rota as usuario
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import auth
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import admin
    from contexto.tarefa.pontos_de_entrada.gerencia_de_tarefa import rota as tarefa

    app.include_router(auth)
    app.include_router(usuario)
    app.include_router(tarefa)
    app.include_router(admin)


def registrar_eventos_e_comandos():
    barramento = Barramento()

    from contexto.usuario.servicos.executores.conta_de_usuario import (
        criar_usuario,
        atualizar_usuario,
        deletar_usuario,
        login_de_usuario,
        atualizar_nivel_de_acesso,
    )
    from contexto.usuario.servicos.visualizadores.conta_de_usuario import (
        obter_usuario_por_id,
        listar_todos_usuarios,
        obter_usuario_logado,
    )

    from contexto.usuario.dominio.comandos.conta_de_usuario import (
        CriarUsuario,
        AtualizarUsuario,
        ObterUsuario,
        ListarUsuarios,
        DeletarUsuario,
        LoginUsuario,
        AtualizarNivelDeAcesso,
        ObterPerfilUsuario,
        ObterUsuarioLogado,
    )
    from contexto.tarefa.dominio.comandos.gerencia_de_tarefa import (
        AtualizarTarefa,
        CriarTarefa,
        DeletarTarefa,
        BuscarTarefas,
        BuscarTodasTarefasPorIdDoUsuario,
        BuscarTarefaPorIdDeTarefa,
    )

    from contexto.tarefa.servicos.executores.gerencia_de_tarefa import (
        atualizar_tarefa,
        criar_tarefa,
        deletar_tarefa,
    )

    from contexto.tarefa.servicos.visualizadores.gerencia_de_tarefa import (
        obter_tarefas_por_status,
        obter_tarefas_por_id_do_usuario,
        obter_tarefas_por_id,
    )

    # usuario
    # executadores
    barramento.registrar_comando(CriarUsuario, criar_usuario)
    barramento.registrar_comando(AtualizarUsuario, atualizar_usuario)
    barramento.registrar_comando(DeletarUsuario, deletar_usuario)
    barramento.registrar_comando(AtualizarNivelDeAcesso, atualizar_nivel_de_acesso)

    # auth
    barramento.registrar_comando(LoginUsuario, login_de_usuario)
    barramento.registrar_comando(ObterUsuarioLogado, obter_usuario_logado)

    # visualizadores
    # VER USUARIO RANDOWM
    barramento.registrar_comando(ObterUsuario, obter_usuario_por_id)
    barramento.registrar_comando(ListarUsuarios, listar_todos_usuarios)
    barramento.registrar_comando(ObterPerfilUsuario, obter_usuario_logado)

    # tarefas
    # executadores
    barramento.registrar_comando(CriarTarefa, criar_tarefa)
    barramento.registrar_comando(AtualizarTarefa, atualizar_tarefa)
    barramento.registrar_comando(DeletarTarefa, deletar_tarefa)

    # visualizadores
    barramento.registrar_comando(BuscarTarefas, obter_tarefas_por_status)
    # Buscar Tarefa por id E Usuario por id
    barramento.registrar_comando(BuscarTarefaPorIdDeTarefa, obter_tarefas_por_id)
    # Todas tarefas por id do usuario
    barramento.registrar_comando(
        BuscarTodasTarefasPorIdDoUsuario, obter_tarefas_por_id_do_usuario
    )


carregar_tabelas()
registrar_rotas()
registrar_eventos_e_comandos()
app
