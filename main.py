from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from metrics import evaluar_respuestas


from rich.console import Console



console= Console()
llm= LlamaCpp(
    model_path="./model/mistral-7b-instruct-v0.1.Q3_K_S.gguf",
    temperature=0.7,
    max_tokens=512,
    top_p=0.95,
    n_ctx=1024
)
##cargamos el pront template
with open("prompt_template.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

template= PromptTemplate.from_template(prompt_template)
chain =LLMChain(llm=llm, prompt=template)

def run_chat():
    console.print("[bold green]Bot de atención al cliente - Fintech[/bold green]")
    while True:
        consulta = input("\nCliente: ")
        if consulta.lower() in ["salir", "exit", "q"]:
            break
        respuesta = chain.run({"input": consulta})
        console.print(f"[bold cyan]Bot:[/bold cyan] {respuesta.strip()}")





def generar_dataset():
    dataset = []
    print("\n[Generador de Dataset para Evaluación]")
    print("Escribe consultas y respuestas esperadas. Escribe 'fin' para terminar.\n")

    while True:
        consulta = input("Consulta del cliente: ")
        if consulta.lower() == "fin":
            break
        esperada = input("Respuesta esperada: ")
        dataset.append({"consulta": consulta, "esperada": esperada})

    with open("eval_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print("\n✅ Dataset generado y guardado como eval_dataset.json.")


if __name__ == "__main__":
    print("\n[1] Usar el chatbot")
    print("[2] Generar dataset de evaluación")
    print("[3] Evaluar modelo con dataset")
    opcion = input("\nElige una opción (1, 2 o 3): ")

    if opcion == "1":
        run_chat()
    elif opcion == "2":
        generar_dataset()
    elif opcion == "3":
        evaluar_respuestas(chain)
    else:
        print("Opción no válida.")
