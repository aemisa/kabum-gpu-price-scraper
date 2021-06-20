import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def extract_gpu_prices():
    # Endereço base usado para buscar os preços
    url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?pagina=1&ordem=1&limite=1000&prime=false&marcas=[]&tipo_produto=[]&filtro=[[\"30\",\"31\"]]'

    # Requisita e analisa a página usando as libs 'requests' e 'BeautifulSoup'
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    # Procurar e armazena o texto da constante 'listagemDados' na variável 'data' usando uma regEx
    pattern = re.compile(r"const\slistagemDados\s=\s(\[.*?\])\n")
    script = soup.find("script", text=pattern)
    data = pattern.search(script.text).group(1)

    # Transforma o texto no formato JSON em um objeto do Python e, em seguida, em um data frame
    data = json.loads(data)
    df = pd.DataFrame(data)

    # Separa a lista dentro do campo 'fabricante' em colunas diferentes
    df_fabricante = df['fabricante'].apply(pd.Series).rename(columns={'nome': 'fabricante_nome',
                                                                    'codigo': 'fabricante_codigo',
                                                                    'img': 'fabricante_img'})

    # Separa a lsita dentro do campo 'brinde' em colunas diferentes
    df_brinde = df['brinde'].apply(pd.Series).rename(columns={'codigo': 'brinde_codigo',
                                                            'img': 'brinde_img'})

    # Concatena as novas colunas criadas com a tabela original
    df = pd.concat([df.drop(['fabricante', 'brinde'], axis=1), df_fabricante, df_brinde], axis=1)

    # Cria uma coluna adicional para armazenar a data e o horário em que a busca foi realizada
    df['data_hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Define a coluna 'codigo' como o índice do data frame
    df.set_index('codigo', inplace=True)

    # Adiciona o data frame que foi gerado ao arquivo 'kabum_precos_gpu.csv'
    df.to_csv('C:/Users/amisawa/programas/kabum_precos_gpu.csv', mode='a')

extract_gpu_prices()
