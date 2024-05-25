from fastapi import APIRouter, Query, Depends, HTTPException
from auth import get_current_user, authorize_user
from utils.Scraper.site_producao import SiteProducaoScraper
from utils.Scraper.site_processamento import SiteProcessamentoScraper
from utils.Scraper.site_comercializacao import SiteComercializacaoScraper
from utils.Scraper.site_importacao import SiteImportacaoScraper
from utils.Scraper.site_exportacao import SiteExportacaoScraper
from utils.constants import opcoes_botoes_processamento, opcoes_botoes_importacao, opcoes_botoes_exportacao
from utils.utils import check_site_availability
from utils.csv.download_csv import download_and_process_csv
from requests.exceptions import ConnectionError, RequestException
import time

router = APIRouter()

def get_data(scraper_class, start_year: int, end_year: int, botao=None):
    data = scraper_class(range(start_year, end_year + 1), botao)
    url = data.url
    csv_url = data.csv_url
    tipo = data.tipo # Verificar qual site é

    # Verificação de quais dados estão disponíveis, primeiro há tentativa do site, depois do csv
    try:
        if check_site_availability(url):
            print('Tentativa de pegar pelo Site')
            attempt = 0
            retries = 3  # Número de tentativas
            while attempt < retries:
                try:
                    data.run()
                    return data.dados.to_dict(orient="records")
                except ConnectionError as e:
                    print(f"Tentativa {attempt + 1} falhou: {str(e)}")
                    attempt += 1
                    time.sleep(2)  # Espera 2 segundos antes de tentar novamente
                    if attempt == retries:
                        raise e
        else:
            raise RequestException("Site não disponível")
    except (ConnectionError, RequestException) as e:
        print('Erro ao conectar ao site, tentando pegar CSV')
        
        try:
            data = download_and_process_csv(csv_url, tipo)
            data_filtered = data[(data['Ano'] >= start_year) & (data['Ano'] <= end_year)]
            
            if botao is not None: 
                classificacao_botao = botao['classificacao_botao']
                data_filtered = data_filtered[data_filtered['Botao'] == classificacao_botao] # Filtrando botao

            return data_filtered.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao baixar e processar o CSV: {str(e)}")


@router.get("/producao-data", 
        tags=["Produção"], 
        summary='Obter dados de Produção', 
        description='Retorna os dados de Produção de um intervalo de anos especificado'
        )
async def get_producao_data(start_year: int = 2020, end_year: int = 2024, current_user: dict = Depends(get_current_user)) -> list: #Travei nessas datas padrão, para nao sobrecarregar
    authorize_user(current_user, "GET", "/producao-data")
    return get_data(SiteProducaoScraper, start_year, end_year)


@router.get("/processamento-data", 
        tags=["Processamento"], 
        summary='Obter dados de Processamento', 
        description='Retorna os dados de Processamento de um intervalo de anos especificado e de forma opcional com as opções no site.')
async def get_processamento_data(
    start_year: int = 2020, 
    end_year: int = 2024,
    botao_opcao: str = Query(None, description="Opção do botão (VINIFERA, AMERICANAS_E_HIBRIDA, UVA_DE_MESA, SEM_CLASSIFICACAO)"),
    current_user: dict = Depends(get_current_user)
) -> list: 
    authorize_user(current_user, "GET", "/processamento-data")
    botao = opcoes_botoes_processamento.get(botao_opcao)
    return get_data(SiteProcessamentoScraper, start_year, end_year, botao)


@router.get("/comercializacao-data", 
        tags=["Comercialização"], 
        summary='Obter dados de Comercialização', 
        description='Retorna os dados de Comercialização de um intervalo de anos especificado')
async def get_comercializacao_data(start_year: int = 2020, end_year: int = 2024, current_user: dict = Depends(get_current_user)) -> list:
    authorize_user(current_user, "GET", "/comercializacao-data")
    return get_data(SiteComercializacaoScraper, start_year, end_year)


@router.get("/importacao-data", 
        tags=["Importação"], 
        summary='Obter dados de Importação', 
        description='Retorna os dados de Importação de um intervalo de anos especificado e de forma opcional com as opções no site.')
async def get_importacao_data(
    start_year: int = 2020, 
    end_year: int = 2024,
    botao_opcao: str = Query(None, description="Opção do botão (VINHOS_DE_MESA, ESPUMANTES, UVAS_FRESCAS, UVAS_PASSAS, SUCO_DE_UVA)"),
    current_user: dict = Depends(get_current_user)
) -> list: 
    
    authorize_user(current_user, "GET", "/importacao-data")
    botao = opcoes_botoes_importacao.get(botao_opcao)
    return get_data(SiteImportacaoScraper, start_year, end_year, botao)


@router.get("/exportacao-data", 
        tags=["Exportação"], 
        summary='Obter dados de Exportação', 
        description='Retorna os dados de Exportação de um intervalo de anos especificado e de forma opcional com as opções no site.')
async def get_exportacao_data(
    start_year: int = 2020, 
    end_year: int = 2024,
    botao_opcao: str = Query(None, description="Opção do botão (VINHOS_DE_MESA, ESPUMANTES, UVAS_FRESCAS, SUCO_DE_UVA)"),
    current_user: dict = Depends(get_current_user)
) -> list: 

    authorize_user(current_user, "GET", "/exportacao-data")
    botao = opcoes_botoes_exportacao.get(botao_opcao)
    return get_data(SiteExportacaoScraper, start_year, end_year, botao)
