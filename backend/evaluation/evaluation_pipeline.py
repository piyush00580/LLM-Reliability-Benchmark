import inspect


class EvaluationPipeline:

    def __init__(self):
        self.metrics = []

    def add_metric(self, metric):
        self.metrics.append(metric)

    def evaluate(self, **kwargs):

        results = {}

        for metric in self.metrics:

            metric_name = metric.__class__.__name__

            parameters = inspect.signature(
                metric.evaluate
            ).parameters

            filtered_kwargs = {
                name: kwargs[name]
                for name in parameters
                if name in kwargs
            }

            results[metric_name] = metric.evaluate(
                **filtered_kwargs
            )

        return results