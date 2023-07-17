import os
import sys

# Altere o diretório atual para o local do arquivo 'main.py'
os.chdir(os.path.dirname(sys.argv[0]))

# Execute o arquivo 'app.py'
os.system('python app.py')