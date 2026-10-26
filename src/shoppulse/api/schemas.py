"""Schémas Pydantic de validation des entrées/sorties de l'API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DelayRequest(BaseModel):
    """Caractéristiques d'une commande pour prédire le risque de retard."""

    distance_km: float = Field(..., ge=0, description="Distance client-vendeur (km)")
    delai_estime_jours: float = Field(..., ge=0, description="Délai de livraison estimé (jours)")
    poids_total: float = Field(..., ge=0, description="Poids total des produits (g)")
    volume_moy: float = Field(..., ge=0, description="Volume moyen des produits (cm³)")
    fret_total: float = Field(..., ge=0, description="Frais de port totaux")
    prix_total: float = Field(..., ge=0, description="Prix total de la commande")
    n_items: int = Field(..., ge=1, description="Nombre d'articles")
    seller_order_count: int = Field(..., ge=0, description="Volume de commandes du vendeur")
    customer_state: str = Field(
        ..., min_length=2, max_length=2, description="État du client (ex. SP)"
    )
    seller_state: str = Field(
        ..., min_length=2, max_length=2, description="État du vendeur (ex. SP)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "distance_km": 450.0,
                "delai_estime_jours": 15,
                "poids_total": 1800,
                "volume_moy": 12000,
                "fret_total": 25.0,
                "prix_total": 180.0,
                "n_items": 1,
                "seller_order_count": 120,
                "customer_state": "RJ",
                "seller_state": "SP",
            }
        }
    }


class DelayResponse(BaseModel):
    probabilite_retard: float = Field(..., description="Probabilité estimée de retard [0,1]")
    risque_eleve: bool = Field(..., description="Vrai si la probabilité dépasse le seuil métier")
    seuil: float = Field(..., description="Seuil de décision appliqué")


class SentimentRequest(BaseModel):
    """Texte d'un avis client (en portugais) à analyser."""

    texte: str = Field(..., min_length=1, description="Texte de l'avis")

    model_config = {
        "json_schema_extra": {"example": {"texte": "Produto excelente, entrega rápida!"}}
    }


class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="'positif' ou 'négatif'")
    probabilite_positif: float = Field(..., description="Probabilité que l'avis soit positif")
