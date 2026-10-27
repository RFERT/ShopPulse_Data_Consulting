"""Tests du traitement Spark du clickstream (bonus)."""

from __future__ import annotations

import pytest
from spark.make_sample_clickstream import generate


def test_sample_generator(tmp_path) -> None:
    out = generate(tmp_path / "clickstream.csv")
    assert out.exists()
    content = out.read_text(encoding="utf-8").splitlines()
    assert content[0].startswith("event_time,event_type")
    assert len(content) > 100


def test_spark_funnel_and_aggregates(tmp_path) -> None:
    pytest.importorskip("pyspark")
    from spark.clickstream_job import (
        funnel,
        get_session,
        load_events,
        revenue_by_category,
        top_categories,
    )

    sample = generate(tmp_path / "clickstream.csv")
    spark = get_session()
    spark.sparkContext.setLogLevel("ERROR")
    try:
        events = load_events(spark, sample).cache()
        stages = {row["stage"]: row for row in funnel(events).collect()}
        assert set(stages) == {"view", "cart", "purchase"}
        assert stages["view"]["events"] >= stages["cart"]["events"]
        assert stages["cart"]["events"] >= stages["purchase"]["events"]
        assert 0.0 <= stages["purchase"]["rate_from_view"] <= 1.0
        assert len(top_categories(events).collect()) >= 1
        assert len(revenue_by_category(events).collect()) >= 1
    finally:
        spark.stop()
