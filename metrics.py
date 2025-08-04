import json
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM


class MiModeloLocal(DeepEvalBaseLLM):
    def __init__(self, chain):
        self.chain = chain

    def load_model(self):
        return self.chain

    def get_model_name(self):
        return "MiModeloLocalLangChain"

    def a_generate(self, prompt: str, **kwargs) -> str:
        return self.chain.invoke({"input": prompt}).strip()

    def generate(self, prompt: str, **kwargs) -> str:
        return self.a_generate(prompt, **kwargs)


def evaluar_respuestas(chain, threshold=0.8):
    print("\n[Evaluando el modelo con el dataset...]\n")
    with open("eval_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    resultados = []
    model = MiModeloLocal(chain)
    metric = AnswerRelevancyMetric(threshold=threshold, model=model)

    for i, entry in enumerate(dataset):
        query = entry["consulta"]
        expected = entry["esperada"]

        test_case = LLMTestCase(
            input=query,
            actual_output=model.a_generate(query),
            expected_output=expected
        )

        score = metric.measure(test_case)
        resultados.append({
            "id": i + 1,
            "consulta": query,
            "esperada": expected,
            "generada": test_case.actual_output,
            "score": round(score, 3),
            "cumple": score >= threshold
        })

        print(f"[{i+1}] Consulta: {query}")
        print(f"    ✅ Esperada: {expected}")
        print(f"    🤖 Generada: {test_case.actual_output}")
        print(f"    📊 Score relevancia: {round(score, 3)}")
        print()

    total = len(resultados)
    aprobadas = sum(1 for r in resultados if r["score"] >= threshold)
    promedio_score = round(sum(r["score"] for r in resultados) / total, 3) if total > 0 else 0

    with open("evaluacion_resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print("✅ Evaluación finalizada. Resultados guardados en evaluacion_resultados.json.\n")
    print("📋 Resumen:")
    print(f"   Total de respuestas evaluadas: {total}")
    print(f"   Respuestas que pasan el umbral ({threshold}): {aprobadas}")
    print(f"   Promedio de score: {promedio_score}")
