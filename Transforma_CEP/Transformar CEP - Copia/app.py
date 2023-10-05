from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
import tempfile

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/processar", methods=["POST"])
def processar():
    try:
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(file_path)

            df = pd.read_excel(file_path)

            if "ID" in df.columns and "CEP" in df.columns:
                dicionario_original = dict(zip(df["ID"], df["CEP"]))
                dicionario_modificado = {}

                for chave, valor in dicionario_original.items():
                    if len(str(valor)) == 7:
                        valor_modificado = "0" + str(valor)[:4] + "-" + str(valor)[4:]
                    elif len(str(valor)) == 8:
                        valor_modificado = str(valor)[:5] + "-" + str(valor)[5:]
                    else:
                        valor_modificado = valor

                    dicionario_modificado[chave] = valor_modificado

                df_modificado = pd.DataFrame(list(dicionario_modificado.items()), columns=["ID", "CEP Modificado"])

                output_file = os.path.join(app.config["UPLOAD_FOLDER"], "dicionario_modificado.xlsx")
                df_modificado.to_excel(output_file, index=False)

                return jsonify(
                    success=True,
                    result=df_modificado.to_dict(orient="records"),
                    download_link="/download/dicionario_modificado.xlsx",
                )
            else:
                return jsonify(success=False, message="O arquivo Excel deve conter colunas com cabeçalhos 'ID' e 'CEP'.")
        else:
            return jsonify(success=False, message="Por favor, selecione um arquivo Excel.")
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
