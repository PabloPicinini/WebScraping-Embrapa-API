from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token, get_current_active_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from routes import router

tags_metadata = [
    {
        "name": "Auth",
        "description": "Endpoints relacionados à autenticação",
    },
    {
        "name": "Produção",
        "description": "Endpoints relacionados à produção de vinhos, sucos e derivados do Rio Grande do Sul",
    },
    {
        "name": "Processamento",
        "description": "Endpoints relacionados à quantidade de uvas processadas no Rio Grande do Sul",
    },
    {
        "name": "Comercialização",
        "description": "Endpoints relacionados à comercialização de vinhos e derivados no Rio Grande do Sul",
    },
    {
        "name": "Importação",
        "description": "Endpoints relacionados à importação de derivados de uva",
    },
    {
        "name": "Exportação",
        "description": "Endpoints relacionados à exportação de derivados de uva",
    },
    {   
        "name": "Página Inicial",
        "description": "Bem vindo à API da Vitivinicultura ",
    }
]

app = FastAPI(
    title="API de Dados de Vinhos",
    description="API para retornar dados sobre a vitivinicultura disponíveis no site [Embrapa Uva e Vinho](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).",
    version="0.0.1",
    openapi_tags=tags_metadata,
)


@app.get("/",
        response_model=dict, 
        tags=["Página Inicial"], 
        summary='Página Inicial', 
        description='Página Inicial')
def root():
    return f"Essa é a página inicial do app"

@app.post("/token", 
        response_model=dict, 
        tags=["Auth"], 
        summary='Autenticar usuário', 
        description='Gera um token JWT para autenticação'
        )

async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=dict, 
         tags=["Auth"], 
        summary='Obter informações do usuário autenticado', 
        description='Retorna as informações do usuário baseado no token JWT')
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
