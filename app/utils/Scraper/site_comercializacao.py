from ..Scraper.scraper_base import ScraperBase
from unidecode import unidecode
import pandas as pd

class SiteComercializacaoScraper(ScraperBase):
    def __init__(self, anos=range(2020, 2024), botao=None):
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'  # Definindo a URL como um atributo de classe
        self.csv_url = ['http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv']
        self.tipo = 'Comerc' # tipo do site Comercio
        super().__init__(url, anos)
        self.botao = botao

    def get_params(self, ano, botao=None):
        return {'ano': ano}

    def get_botoes(self):
        return []
    
    def transform_dados(self):
        # Remover acentuação e caracteres especiais e converter para maiúsculas
        def normalize_text(text):
            if isinstance(text, str):
                if text.strip() == "-" or text.strip()=="*":
                    return "0"
                else:
                    return unidecode(text).upper()
            else:
                return text

        # Aplicar normalização a todas as colunas de texto
        for col in self.dados.select_dtypes(include='object'):
            self.dados[col] = self.dados[col].map(normalize_text)

        # Renomear a coluna 'Quantidade (L.)' para 'Quantidade'
        self.dados = self.dados.rename(columns={'Quantidade (L.)': 'Quantidade'})

        # Garantir que todos os valores na coluna 'Quantidade' sejam strings antes de remover os pontos
        self.dados['Quantidade'] = self.dados['Quantidade'].astype(str).str.replace('.', '')
        
        # Substituir valores não numéricos por zero antes de converter para inteiro
        self.dados['Quantidade'] = pd.to_numeric(self.dados['Quantidade'], errors='coerce').fillna(0).astype(int)


        # Ordenar as colunas
        colunas = ['Produto', 'Classificação', 'Ano', 'Quantidade']
        self.dados = self.dados[colunas]

        # Remover as linhas que possuem o total do ano no Web Scraping
        self.dados = self.dados.loc[(self.dados['Produto'] != 'TOTAL') | (self.dados['Classificação'] != 'TOTAL')]
    

    def run(self):
        super().run()  # Chama o método run da classe base
        self.transform_dados()  # Aplica as transformações nos dados