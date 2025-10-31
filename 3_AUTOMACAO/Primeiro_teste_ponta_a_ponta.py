import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- CONFIGURAÇÃO E FUNÇÃO PARA ESPERA EXPLÍCITA ---
# Tempo máximo de espera para um elemento específico
MAX_WAIT_TIME = 15 

def iniciar_e_configurar_driver():
    """Configura e abre o navegador Google Chrome."""
    try:
        servico = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=servico)
        # NOTA: O implicitly_wait (espera implícita) ainda está aqui, mas o WebDriverWait é mais eficaz.
        driver.implicitly_wait(5) 
        driver.get("http://analista-teste.seatecnologia.com.br/")
        driver.maximize_window()
        print("1. NAVEGADOR INICIADO E PRONTO.")
        return driver
    except Exception as e:
        print(f"ERRO: Não foi possível iniciar o navegador. Erro: {e}")
        return None

def esperar_e_clicar(driver, by, seletor):
    """
    INSERÇÃO DE CÓDIGO CRÍTICO: Função para Espera Explícita.
    
    Esta função espera até que o elemento esteja VISÍVEL e CLICÁVEL 
    (por até {MAX_WAIT_TIME} segundos) antes de interagir, resolvendo problemas de lentidão.
    Se o elemento não aparecer no tempo limite, lança uma exceção.
    """
    wait = WebDriverWait(driver, MAX_WAIT_TIME)
    try:
        # Espera que o elemento seja visível e clicável, depois clica.
        elemento = wait.until(EC.element_to_be_clickable((by, seletor)))
        elemento.click()
        return True
    except TimeoutException:
        print(f"\033[91mFALHA DE TEMPO: O elemento '{seletor}' demorou mais de {MAX_WAIT_TIME}s para ser clicável. (Causa da lentidão).\033[0m")
        return False
    except NoSuchElementException:
        print(f"\033[91mFALHA DE LOCALIZAÇÃO: O elemento '{seletor}' não foi encontrado.\033[0m")
        return False

# --- FUNÇÕES DE TESTE ---
def testar_fluxo_cadastro(driver):
    """Testa a principal funcionalidade de cadastro (CRUD: Create)."""
    print("\n2. INICIANDO TESTE DE CADASTRO (Caminho Feliz)...")
    
    NOME_TESTE = f"Antonio Teste Automatizado - {time.time()}" 
    CPF_TESTE = "12345678910"
    DATA_NASC_TESTE = "01011990"
    
    try:
        # AÇÃO 1: Clicar no botão para ADICIONAR NOVO FUNCIONÁRIO
        # CHAVE: Usamos a função robusta 'esperar_e_clicar' aqui.
        if not esperar_e_clicar(driver, By.ID, "btnAdicionarFuncionario"):
            return # Sai da função se o botão não abrir
        print("   -> Formulário de cadastro aberto após espera.")
        
        # AÇÃO 2: Preencher os campos, esperando que eles estejam VISÍVEIS antes de digitar.
        wait = WebDriverWait(driver, MAX_WAIT_TIME)
        
        campo_nome = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='nome']")))
        campo_nome.send_keys(NOME_TESTE)
        
        driver.find_element(By.XPATH, "//input[@name='cpf']").send_keys(CPF_TESTE)
        driver.find_element(By.XPATH, "//input[@name='dataNascimento']").send_keys(DATA_NASC_TESTE)
        
        # AÇÃO 3: Clicar no botão 'SALVAR'
        if not esperar_e_clicar(driver, By.ID, "btnSalvar"):
            return # Sai se o botão Salvar não aparecer
        print("   -> Dados submetidos (Salvar) após espera.")

        # VERIFICAÇÃO (CRUD: Read): Espera a lista carregar e verifica o nome.
        # Espera até que o nome do teste esteja visível no código da página.
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), NOME_TESTE))
        
        print(f"\033[92mSUCESSO: Cadastro realizado. '{NOME_TESTE}' encontrado na lista.\033[0m")

    except TimeoutException:
        print("\033[91mFALHA DE TEMPO: A verificação final demorou muito. O cadastro pode ter falhado.\033[0m")
    except Exception as e:
        print(f"\033[91mERRO INESPERADO: {e}\033[0m")

def testar_navegacao_sidebar(driver):
    """Testa se a navegação lateral está funcional (Bug BF010)."""
    print("\n3. INICIANDO TESTE DE NAVEGAÇÃO LATERAL (Sidebar)...")
    try:
        # AÇÃO: Localizamos e clicamos no ícone da Sidebar usando a função robusta.
        # ATENÇÃO: XPATH ajustado para o segundo item da barra lateral (exemplo).
        if not esperar_e_clicar(driver, By.XPATH, "//a[@href='/fluxograma']"): 
            return # Sai do teste se o ícone não for clicável
        
        time.sleep(1) # Pequena pausa após o clique
        
        # VERIFICAÇÃO: Espera que o texto "Em Breve" apareça na tela.
        wait = WebDriverWait(driver, MAX_WAIT_TIME)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Em Breve"))
        
        print("\033[92mSUCESSO: O link da Sidebar redireciona para a tela 'Em Breve' após espera.\033[0m")
            
    except TimeoutException:
        print("\033[91mFALHA DE TEMPO: A mensagem 'Em Breve' não apareceu. (Bug BF010) O teste parou.\033[0m")
    except Exception as e:
        print(f"\033[91mERRO: {e}\033[0m")


# --- FLUXO PRINCIPAL DO PROGRAMA ---
def executar_teste_e2e_simples():
    """Função principal que organiza a execução dos testes."""
    driver = None
    try:
        driver = iniciar_e_configurar_driver()
        if driver is None:
            return

        # Execução dos testes
        testar_fluxo_cadastro(driver)
        testar_navegacao_sidebar(driver)
        
    finally:
        if driver:
            print("\n4. TESTES CONCLUÍDOS. Fechando navegador.")
            driver.quit()

# Ponto de entrada do script
if __name__ == "__main__":
    executar_teste_e2e_simples()