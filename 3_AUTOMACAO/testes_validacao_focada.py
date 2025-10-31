import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- CONFIGURAÇÃO E INICIALIZAÇÃO DO DRIVER ---
MAX_WAIT_TIME = 10 

def iniciar_e_configurar_driver():
    """
    Função para configurar e abrir o navegador Google Chrome.
    Esta função está aqui para que os testes unitários possam rodar sozinhos.
    """
    try:
        servico = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=servico)
        driver.implicitly_wait(5) 
        driver.get("http://analista-teste.seatecnologia.com.br/")
        driver.maximize_window()
        print("1. NAVEGADOR INICIADO E PRONTO para Testes Focados.")
        return driver
    except Exception as e:
        print(f"ERRO: Não foi possível iniciar o navegador. Erro: {e}")
        return None

# --- TESTES UNITÁRIOS FOCADOS ---

def testar_regra_cpf_invalido(driver):
    """
    TESTE UNITÁRIO 1: Validação de CPF com números repetidos (Regra BF005).
    Verifica se o sistema BLOQUEIA o cadastro de um CPF inválido que falha na regra matemática.
    """
    print("\n--- TESTE 1: BLOQUEIO DE CPF REPETIDO (BF005) ---")
    
    CPF_INVALIDO = "11111111111"
    
    try:
        # Reabre o formulário (o ID deve ser o correto: 'btnAdicionarFuncionario')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnAdicionarFuncionario"))).click()
        
        # 1. Preenche Nome e CPF
        driver.find_element(By.XPATH, "//input[@name='nome']").send_keys("Teste Validação CPF")
        driver.find_element(By.XPATH, "//input[@name='cpf']").send_keys(CPF_INVALIDO)
        
        # 2. Tenta Salvar
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSalvar"))).click()
        time.sleep(2) 
        
        # 3. VERIFICAÇÃO: Se o nome aparecer na lista, o bug BF005 FOI CONFIRMADO.
        if "Teste Validação CPF" in driver.page_source:
            print(f"\033[91mFALHA UNITÁRIA (BF005): Sistema salvou o CPF inválido: {CPF_INVALIDO}.\033[0m")
        else:
            print("\033[92mSUCESSO UNITÁRIO: O CPF inválido foi bloqueado. (Regra correta).\033[0m")
            
    except Exception as e:
        print(f"\033[91mErro durante o Teste 1: {e}\033[0m")

def testar_limpeza_caracteres_nome(driver):
    """
    TESTE UNITÁRIO 2: Rejeição de caracteres especiais no campo Nome (Bug BF001).
    Verifica se o sistema aceita/salva caracteres não alfabéticos.
    """
    print("\n--- TESTE 2: VALIDAÇÃO DE NOME (BF001) ---")
    
    NOME_SUJO = "Nome@Invalido!123" 
    
    try:
        # Reabre o formulário
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnAdicionarFuncionario"))).click()
        
        # 1. Preenche Nome com caracteres inválidos
        driver.find_element(By.XPATH, "//input[@name='nome']").send_keys(NOME_SUJO)
        driver.find_element(By.XPATH, "//input[@name='cpf']").send_keys("00000000000") # CPF válido para permitir submissão
        
        # 2. Tenta Salvar
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSalvar"))).click()
        time.sleep(2) 

        # 3. VERIFICAÇÃO: O nome quebrado aparece na lista de funcionários?
        if NOME_SUJO in driver.page_source:
            print(f"\033[91mFALHA UNITÁRIA (BF001): Nome com caracteres especiais foi salvo: {NOME_SUJO}.\033[0m")
        else:
            print("\033[92mSUCESSO UNITÁRIO: O nome com caracteres inválidos foi rejeitado ou limpo.\033[0m")

    except Exception as e:
        print(f"\033[91mErro durante o Teste 2: {e}\033[0m")

# --- BLOCO DE EXECUÇÃO INDEPENDENTE ---

if __name__ == "__main__":
    """
    Este bloco garante que o código rode sozinho.
    Ele inicia o driver, executa os testes focados e depois fecha o navegador.
    """
    driver = iniciar_e_configurar_driver()
    
    if driver is None:
        print("Execução interrompida.")
    else:
        try:
            # Executa os testes unitários
            testar_regra_cpf_invalido(driver)
            testar_limpeza_caracteres_nome(driver)
            
        finally:
            # Garante que o navegador será fechado
            if driver:
                print("\nTestes Focados Concluídos. Fechando navegador.")
                driver.quit()