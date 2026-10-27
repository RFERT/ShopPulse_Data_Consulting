"""Orchestrateur d'entraînement : modèles de retard et de sentiment.

Exécute l'entraînement complet, sauvegarde les artefacts (``artifacts/models``) et
produit un rapport de performance (``docs/rapport_modeles.md``).

Usage : python -m shoppulse.models.train
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

from shoppulse.config import ROOT_DIR
from shoppulse.models import delay, equity, sentiment, tracking


def train_delay() -> dict:
    """Entraîne et évalue le modèle de retard ; renvoie les éléments de rapport."""
    from shoppulse.features.engineering import build_delay_features

    df = build_delay_features()
    cv = delay.cross_validate_models(df)
    pipe, metrics, test_df = delay.train_best(df, "random_forest")
    importances = delay.feature_importances(pipe)
    audit = equity.audit_by_region(pipe, test_df)
    gap = equity.equity_gap(audit)
    delay.save_model(pipe)

    with tracking.start_run("delay_random_forest") as run:
        run.log_params({"model": "random_forest", "n_observations": len(df)})
        run.log_metrics(
            {
                "roc_auc": metrics["roc_auc"],
                "pr_auc": metrics["pr_auc"],
                "recall_late": metrics["report"]["1"]["recall"],
                "f1_late": metrics["report"]["1"]["f1-score"],
                "equity_gap_recall": gap["ecart_rappel"],
                "equity_gap_fpr": gap["ecart_fpr"],
            }
        )
        run.log_artifact(delay.DELAY_MODEL_PATH)

    return {
        "n": len(df),
        "taux_retard": round(df[delay.TARGET].mean(), 4),
        "cv": cv,
        "metrics": metrics,
        "importances": importances,
        "audit": audit,
        "gap": gap,
    }


def train_sentiment() -> dict:
    """Entraîne baseline et réseau de neurones ; renvoie les éléments de rapport."""
    df = sentiment.load_reviews()
    tr, te = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

    base = sentiment.build_baseline()
    base.fit(tr["texte"], tr["label"])
    base_pred = base.predict(te["texte"])
    base_f1 = f1_score(te["label"], base_pred)
    sentiment.save_baseline(base)

    vocab = sentiment.build_vocab(tr["texte"].tolist())
    model, history = sentiment.train_nn(tr["texte"].tolist(), tr["label"].tolist(), vocab)
    nn_pred = sentiment.nn_predict(model, te["texte"].tolist(), vocab)
    nn_f1 = f1_score(te["label"], nn_pred)

    # Analyse d'erreurs : exemples mal classés par la baseline.
    err = te.loc[base_pred != te["label"], ["texte", "review_score", "label"]].head(5)

    with tracking.start_run("sentiment_baseline_vs_nn") as run:
        run.log_params({"n_observations": len(df), "nn_epochs": len(history)})
        run.log_metrics({"baseline_f1": base_f1, "nn_f1": nn_f1})

    return {
        "n": len(df),
        "pos_rate": round(df["label"].mean(), 4),
        "base_f1": round(base_f1, 4),
        "base_report": classification_report(te["label"], base_pred, output_dict=True),
        "nn_f1": round(nn_f1, 4),
        "history": history,
        "errors": err,
    }


def _report(delay_res: dict, sent_res: dict, path: Path) -> None:
    lines = ["# Rapport des modèles — ShopPulse\n"]

    lines.append("## 1. Modèle de retard de livraison\n")
    lines.append(
        f"- Observations : **{delay_res['n']}** commandes livrées — "
        f"taux de retard **{100 * delay_res['taux_retard']:.1f} %** (classes déséquilibrées).\n"
    )
    lines.append("### Validation croisée (5 plis)\n")
    lines.append(delay_res["cv"].to_markdown(index=False))
    m = delay_res["metrics"]
    lines.append(
        f"\n\n### Modèle retenu (Random Forest)\n"
        f"- ROC-AUC : **{m['roc_auc']}** · PR-AUC : **{m['pr_auc']}**\n"
        f"- Rappel classe « retard » : **{m['report']['1']['recall']:.3f}** · "
        f"F1 : **{m['report']['1']['f1-score']:.3f}**\n"
        "\n> **Interprétation** : la Random Forest offre le meilleur pouvoir de "
        "classement (ROC-AUC/PR-AUC), tandis que la régression logistique équilibrée "
        "maximise le rappel (~0,63). Au seuil par défaut de 0,5 le rappel est faible : "
        "en production, **le seuil de décision doit être abaissé** pour privilégier le "
        "rappel (anticiper un maximum de retards), au prix de la précision. L'API expose "
        "la **probabilité** afin de laisser le métier fixer ce seuil.\n"
    )
    lines.append("\n### Importance des variables\n")
    lines.append(delay_res["importances"].to_markdown(index=False))
    lines.append("\n\n### Audit d'équité par région\n")
    lines.append(
        f"Écart de rappel inter-régions : **{delay_res['gap']['ecart_rappel']}** · "
        f"écart de taux de faux positifs : **{delay_res['gap']['ecart_fpr']}**.\n"
    )
    lines.append(delay_res["audit"].head(10).to_markdown(index=False))

    lines.append("\n\n## 2. Modèle de sentiment (avis en portugais)\n")
    lines.append(
        f"- Observations : **{sent_res['n']}** avis textuels — "
        f"part d'avis positifs **{100 * sent_res['pos_rate']:.1f} %**.\n"
        f"- **Baseline TF-IDF + régression logistique** : F1 = **{sent_res['base_f1']}**\n"
        f"- **Réseau de neurones PyTorch** : F1 = **{sent_res['nn_f1']}**\n"
    )
    lines.append("\n### Courbes d'apprentissage (réseau de neurones)\n")
    hist = pd.DataFrame(sent_res["history"])
    hist.insert(0, "epoch", range(1, len(hist) + 1))
    lines.append(hist.to_markdown(index=False))
    lines.append("\n\n### Analyse d'erreurs (baseline) — exemples mal classés\n")
    lines.append(sent_res["errors"].to_markdown(index=False))

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    delay_res = train_delay()
    sent_res = train_sentiment()
    _report(delay_res, sent_res, ROOT_DIR / "docs" / "rapport_modeles.md")
    print("Modèle retard — ROC-AUC:", delay_res["metrics"]["roc_auc"])
    print("Sentiment — baseline F1:", sent_res["base_f1"], "| NN F1:", sent_res["nn_f1"])
    print("Artefacts et rapport générés.")


if __name__ == "__main__":
    main()
