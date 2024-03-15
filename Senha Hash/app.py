import hashlib

def converter_senha_para_hash(senha):
    # Criar um objeto hash
    hasher = hashlib.sha256()

    # Converter a senha para bytes
    senha_bytes = senha.encode('utf-8')

    # Atualizar o objeto hash com a senha
    hasher.update(senha_bytes)

    # Obter a hash em formato hexadecimal
    senha_hash = hasher.hexdigest()

    return senha_hash

# Exemplo de uso
senha = input("Digite a senha: ")
senha_hash = converter_senha_para_hash(senha)
print("A senha convertida em hash é:", senha_hash)