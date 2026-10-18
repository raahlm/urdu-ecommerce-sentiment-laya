# Roman Urdu annotation evaluation

## Evaluation caveat

All 100 reference records are marked `silver_unverified`. These scores measure agreement with the supplied silver labels, not verified human-annotation accuracy.

The primary quality comparison uses Qwen 3 14B, LAYA base (batch 4), and LAYA fine-tuned (batch 4). Batch-size-1 runs use the same respective checkpoints and are retained mainly for reproducibility and throughput comparison.

LAYA does not define `sentiment_evidence_present`; that field is scored only for Qwen. LAYA's binary `noul` outputs are thresholded at 0.5 as the probability of True. Aspect category scores use presence/absence; aspect sentiment scores also treat missing categories as `NOT_MENTIONED`.

## Classification metrics

```text\n                   system                            task    n  accuracy  macro_f1  classes
               Qwen 3 14B                       relevance  100  0.990000  0.961161        3
               Qwen 3 14B               overall_sentiment  100  0.880000  0.832085        6
               Qwen 3 14B                language_primary  100  0.850000  0.457673        4
               Qwen 3 14B                  code_switching  100  0.880000  0.539171        2
               Qwen 3 14B                  understandable  100  0.990000  0.497487        2
               Qwen 3 14B      sentiment_evidence_present  100  0.950000  0.899173        2
      LAYA base (batch 4)                       relevance  100  0.290000  0.205707        3
      LAYA base (batch 4)               overall_sentiment  100  0.420000  0.235042        6
      LAYA base (batch 4)                language_primary  100  0.000000  0.000000        6
      LAYA base (batch 4)                  code_switching  100  0.870000  0.465241        2
      LAYA base (batch 4)                  understandable  100  0.200000  0.173212        2
      LAYA base (batch 1)                       relevance  100  0.290000  0.205707        3
      LAYA base (batch 1)               overall_sentiment  100  0.420000  0.235042        6
      LAYA base (batch 1)                language_primary  100  0.000000  0.000000        6
      LAYA base (batch 1)                  code_switching  100  0.870000  0.465241        2
      LAYA base (batch 1)                  understandable  100  0.200000  0.173212        2
LAYA fine-tuned (batch 4)                       relevance  100  0.920000  0.634033        3
LAYA fine-tuned (batch 4)               overall_sentiment  100  0.740000  0.498506        6
LAYA fine-tuned (batch 4)                language_primary  100  0.860000  0.458701        4
LAYA fine-tuned (batch 4)                  code_switching  100  0.870000  0.465241        2
LAYA fine-tuned (batch 4)                  understandable  100  0.990000  0.497487        2
LAYA fine-tuned (batch 1)                       relevance  100  0.920000  0.634033        3
LAYA fine-tuned (batch 1)               overall_sentiment  100  0.740000  0.498506        6
LAYA fine-tuned (batch 1)                language_primary  100  0.860000  0.458701        4
LAYA fine-tuned (batch 1)                  code_switching  100  0.870000  0.465241        2
LAYA fine-tuned (batch 1)                  understandable  100  0.990000  0.497487        2
               Qwen 3 14B aspect_sentiment_all_categories 1500  0.948667  0.443223        6
      LAYA base (batch 4) aspect_sentiment_all_categories 1500  0.247333  0.105539        6
      LAYA base (batch 1) aspect_sentiment_all_categories 1500  0.247333  0.105539        6
LAYA fine-tuned (batch 4) aspect_sentiment_all_categories 1500  0.926000  0.406310        6
LAYA fine-tuned (batch 1) aspect_sentiment_all_categories 1500  0.926000  0.406310        6\n```

## Multilabel metrics

```text\n                   system              task   n  micro_precision  micro_recall  micro_f1  macro_f1  exact_set_match
               Qwen 3 14B    review_intents 100         0.721311      0.624113  0.669202  0.394180             0.43
               Qwen 3 14B aspect_categories 100         0.731707      0.756303  0.743802  0.681124             0.62
      LAYA base (batch 4)    review_intents 100         0.300000      0.085106  0.132597  0.101949             0.05
      LAYA base (batch 4) aspect_categories 100         0.087884      0.865546  0.159566  0.155073             0.01
      LAYA base (batch 1)    review_intents 100         0.300000      0.085106  0.132597  0.101949             0.05
      LAYA base (batch 1) aspect_categories 100         0.087884      0.865546  0.159566  0.155073             0.01
LAYA fine-tuned (batch 4)    review_intents 100         0.714286      0.567376  0.632411  0.249329             0.34
LAYA fine-tuned (batch 4) aspect_categories 100         0.592105      0.756303  0.664207  0.644792             0.41
LAYA fine-tuned (batch 1)    review_intents 100         0.714286      0.567376  0.632411  0.249329             0.34
LAYA fine-tuned (batch 1) aspect_categories 100         0.592105      0.756303  0.664207  0.644792             0.41\n```

## Inference speed

```text\n                   system  records  measured_loop_seconds_sum  seconds_per_record  records_per_second                                                      timing_note
               Qwen 3 14B      100                 163.990450            1.639905            0.609792 Sum of Qwen active loop times; excludes warmup and inter-run gap
      LAYA base (batch 4)      100                   1.462361            0.014624           68.382546        Reported LAYA inference loop; excludes initial model load
      LAYA base (batch 1)      100                   1.855443            0.018554           53.895479        Reported LAYA inference loop; excludes initial model load
LAYA fine-tuned (batch 4)      100                   1.460476            0.014605           68.470830        Reported LAYA inference loop; excludes initial model load
LAYA fine-tuned (batch 1)      100                   1.857288            0.018573           53.841937        Reported LAYA inference loop; excludes initial model load\n```

## Generated files

- `aspect_category_f1_by_label.png`
- `classification_accuracy.png`
- `classification_macro_f1.png`
- `classification_metrics.csv`
- `disagreements.csv`
- `inference_speed.csv`
- `inference_throughput.png`
- `intent_f1_by_label.png`
- `multilabel_metrics.csv`
- `multilabel_micro_f1.png`
- `normalized_predictions.csv`
- `per_label_metrics.csv`
- `seconds_per_record.png`
