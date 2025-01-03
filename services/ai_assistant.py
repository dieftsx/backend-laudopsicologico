from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Any


class AIAssistant:
    def __init__(self):
        # Carregar modelo e tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            "neuralmind/bert-base-portuguese-cased"
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "neuralmind/bert-base-portuguese-cased",
            num_labels=10
        )

        # Carregar spaCy
        self.nlp = spacy.load("pt_core_news_sm")

        # Categorias de diagnóstico
        self.categories = [
            'Depressão',
            'Ansiedade',
            'Transtorno Bipolar',
            'TEPT',
            'Transtorno de Pânico',
            'TOC',
            'Transtorno de Personalidade',
            'Transtorno Alimentar',
            'TDAH',
            'Sem Indicação Específica'
        ]

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        # Tokenização e inferência
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = self.model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

        # Extrair entidades
        doc = self.nlp(text)
        entities = {
            'sintomas': [],
            'comportamentos': [],
            'emocoes': []
        }

        for ent in doc.ents:
            if ent.label_ in ['SYMPTOM', 'BEHAVIOR', 'EMOTION']:
                entities[ent.label_.lower() + 's'].append(ent.text)

        # Gerar diagnósticos
        diagnostics = [
            {
                'categoria': cat,
                'probabilidade': prob.item(),
                'confianca': 'Alta' if prob.item() > 0.7 else 'Média' if prob.item() > 0.4 else 'Baixa'
            }
            for cat, prob in zip(self.categories, probs[0])
        ]

        # Ordenar por probabilidade
        diagnostics.sort(key=lambda x: x['probabilidade'], reverse=True)

        # Gerar recomendações
        recommendations = self.generate_recommendations(diagnostics[:3])

        return {
            'diagnosticos': diagnostics[:3],
            'entidades': entities,
            'recomendacoes': recommendations
        }

    def generate_recommendations(self, top_diagnostics: List[Dict]) -> List[str]:
        recommendations = []

        for diag in top_diagnostics:
            if diag['probabilidade'] > 0.4:
                if diag['categoria'] == 'Depressão':
                    recommendations.extend([
                        "Considerar avaliação psiquiátrica para possível tratamento medicamentoso",
                        "Recomendar psicoterapia regular",
                        "Sugerir atividades físicas e exposição solar"
                    ])
                elif diag['categoria'] == 'Ansiedade':
                    recommendations.extend([
                        "Indicar técnicas de respiração e relaxamento",
                        "Considerar terapia cognitivo-comportamental",
                        "Sugerir prática de mindfulness"
                    ])
                # Adicionar mais recomendações para outras categorias

        return list(set(recommendations))  # Remover duplicatas