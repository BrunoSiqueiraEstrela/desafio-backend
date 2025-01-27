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


# Rota de health check
@app.get("/health-check", tags=["HELPERS"], include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


def registrar_rotas():
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import rota as usuario
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import auth
    from contexto.usuario.pontos_de_entrada.conta_de_usuario import admin
    from contexto.calculo_de_valores.pontos_de_entrada.carteira import rota as carteira
    from contexto.calculo_de_valores.pontos_de_entrada.transferencia_de_valores import (
        rota as transferencia,
    )

    app.include_router(auth)
    app.include_router(usuario)
    app.include_router(admin)
    app.include_router(transferencia)
    app.include_router(carteira)


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

    from contexto.calculo_de_valores.servicos.executores.carteira import (
        criar_carteira_do_usuario,
        atualizar_carteira_do_usuario,
    )
    from contexto.calculo_de_valores.servicos.visualizadores.carteira import (
        listar_carteiras_do_usuario,
    )
    from contexto.calculo_de_valores.dominio.comandos.carteira import (
        CriarCarteira,
        AtualizarCarteira,
        ListarCarteiras,
    )
    from contexto.calculo_de_valores.dominio.comandos.transferencia_de_valores import (
        RealizarTransferencia,
        ListarTransferenciasDeUmUsuarioPorPeriodo,
    )

    from contexto.calculo_de_valores.servicos.executores.transferencia_de_valores import (
        realizar_transferencia,
    )

    from contexto.calculo_de_valores.servicos.visualizadores.transferencia_de_valores import (
        listar_transferencias_do_usuario,
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

    # carteira
    barramento.registrar_comando(CriarCarteira, criar_carteira_do_usuario)
    barramento.registrar_comando(AtualizarCarteira, atualizar_carteira_do_usuario)
    barramento.registrar_comando(ListarCarteiras, listar_carteiras_do_usuario)

    # transferencia
    barramento.registrar_comando(RealizarTransferencia, realizar_transferencia)
    barramento.registrar_comando(
        ListarTransferenciasDeUmUsuarioPorPeriodo, listar_transferencias_do_usuario
    )


carregar_tabelas()
registrar_rotas()
registrar_eventos_e_comandos()
app
