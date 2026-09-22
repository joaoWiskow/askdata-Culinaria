# askdata-NAVI
Destinado a o trabalho produzido ao longo da sprint 1    

Piloto A: Enzo  
Piloto B: João    
Piloto C: Matheus

  ## Dependências

O projeto utiliza Python 3 e as seguintes bibliotecas:

```txt
google-genai
chromadb
pypdf
python-dotenv
```

### Instalação

Recomenda-se utilizar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```powershell
.venv\Scripts\activate
```

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Ou diretamente:

```bash
pip install google-genai chromadb pypdf python-dotenv
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` não deve ser versionado no Git.

