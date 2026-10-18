# Roman Urdu E-Commerce Review Dataset

## Annotation method

Annotations were generated using Qwen3:14B.

These annotations are machine-generated silver labels. They have not
been independently verified by human annotators and should not be
treated as human-verified ground truth.

## Dataset splits

| Split | Records |
|---|---:|
| Train | 20,008 |
| Validation | 2,495 |
| Test | 2,503 |
| Total | 25,006 |

The test split should remain separate during model training and
hyperparameter selection.

## Intended use

Research on Roman Urdu e-commerce review classification, sentiment
analysis, and related natural language processing tasks.

Evaluation against these labels measures agreement with machine-
generated annotations, not necessarily human judgment.

## Privacy

These files are sanitized release copies. Email-like strings and
long numeric sequences in review text are masked conservatively.
This process cannot guarantee that every personal identifier has
been removed.

## Limitations

- Qwen3:14B annotations may contain errors and biases.
- The dataset may not represent all Pakistani consumers or products.
- Machine-label agreement does not establish human-level accuracy.
- Review-source terms and redistribution permissions must be respected.
