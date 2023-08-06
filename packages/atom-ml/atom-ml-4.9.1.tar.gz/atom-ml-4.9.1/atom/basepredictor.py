# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Module containing the BasePredictor class.

"""

# Standard packages
import numpy as np
import pandas as pd
from typeguard import typechecked
from typing import Union, Optional

# Own modules
from .branch import Branch
from .models import MODEL_LIST
from .ensembles import Voting, Stacking
from .utils import (
    SEQUENCE_TYPES, X_TYPES, Y_TYPES, DF_ATTRS, flt, lst,
    check_is_fitted, divide, get_best_score, delete,
    method_to_log, composed, crash,
)


class BasePredictor:
    """Properties and shared methods for the trainers."""

    # Tracking parameters for mlflow
    _tracking_params = dict(
        log_bo=True,
        log_model=True,
        log_plots=True,
        log_data=False,
        log_pipeline=False,
    )

    def __getattr__(self, item):
        """Get attributes from the current branch."""
        if self.__dict__.get("_branches").get(item):
            return self._branches[item]  # Get branch
        elif item in self.branch._get_attrs():
            return getattr(self.branch, item)  # Get attr from branch
        elif self.__dict__.get("_models").get(item.lower()):
            return self._models[item.lower()]  # Get model subclass
        elif item in self.branch.columns:
            return self.branch.dataset[item]  # Get column
        elif item in DF_ATTRS:
            return getattr(self.branch.dataset, item)  # Get attr from dataset
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{item}'."
            )

    def __setattr__(self, item, value):
        """Set some properties to the current branch."""
        if isinstance(getattr(Branch, item, None), property):
            setattr(self.branch, item, value)
        else:
            super().__setattr__(item, value)

    def __delattr__(self, item):
        """Call appropriate methods for model and branch deletion."""
        # To delete branches, call the appropriate method
        if item == "branch":
            self.branch.delete()
        else:
            try:
                self.delete(item)
            except ValueError:
                del self.__dict__[item]

    # Tracking properties ========================================== >>

    @property
    def log_bo(self):
        return self._tracking_params["log_bo"]

    @log_bo.setter
    @typechecked
    def log_bo(self, value: bool):
        self._tracking_params["log_bo"] = value

    @property
    def log_model(self):
        return self._tracking_params["log_model"]

    @log_model.setter
    @typechecked
    def log_model(self, value: bool):
        self._tracking_params["log_model"] = value

    @property
    def log_plots(self):
        return self._tracking_params["log_plots"]

    @log_plots.setter
    @typechecked
    def log_plots(self, value: bool):
        self._tracking_params["log_plots"] = value

    @property
    def log_data(self):
        return self._tracking_params["log_data"]

    @log_data.setter
    @typechecked
    def log_data(self, value: bool):
        self._tracking_params["log_data"] = value

    @property
    def log_pipeline(self):
        return self._tracking_params["log_pipeline"]

    @log_pipeline.setter
    @typechecked
    def log_pipeline(self, value: bool):
        self._tracking_params["log_pipeline"] = value

    # Utility properties =========================================== >>

    @property
    def branch(self):
        """Return the current branch."""
        return self._branches[self._current]

    @property
    def models(self):
        """Return the names of the models in the pipeline."""
        return flt([getattr(model, "name", model) for model in self._models])

    @property
    def metric(self):
        """Return the names of the metrics in the pipeline."""
        return flt([getattr(metric, "name", metric) for metric in self._metric])

    @property
    def errors(self):
        """Return the errors encountered during model training."""
        return self._errors

    @property
    def winner(self):
        """Return the best performing model."""
        if self._models:  # Returns None if not fitted
            return self._models[np.argmax([get_best_score(m) for m in self._models])]

    @property
    def results(self):
        """Return the results as a pd.DataFrame."""

        def frac(m):
            """Return the fraction of the train set used for the model."""
            n_models = m.branch.idx[0] / m._train_idx
            if n_models == int(n_models):
                return round(1.0 / n_models, 2)
            else:
                return round(m._train_idx / m.branch.idx[0], 2)

        df = pd.DataFrame(
            data=[m.results for m in self._models],
            columns=self._models[0].results.index if self._models else [],
            index=lst(self.models),
        ).dropna(axis=1, how="all")

        # For sh and ts runs, include the fraction of training set
        if any(m._train_idx != len(m.branch.train) for m in self._models):
            df = df.set_index(
                pd.MultiIndex.from_arrays(
                    [[frac(m) for m in self._models], self.models],
                    names=["frac", "model"],
                )
            ).sort_index(level=0, ascending=True)

        return df

    # Prediction methods =========================================== >>

    @composed(crash, method_to_log)
    def reset_predictions(self):
        """Clear the prediction attributes from all models."""
        for m in self._models:
            m._pred_attrs = [None] * 10

    @composed(crash, method_to_log, typechecked)
    def predict(self, X: X_TYPES, **kwargs):
        """Get the winning model's predictions on new data."""
        check_is_fitted(self, attributes="_models")
        return self.winner.predict(X, **kwargs)

    @composed(crash, method_to_log, typechecked)
    def predict_proba(self, X: X_TYPES, **kwargs):
        """Get the winning model's probability predictions on new data."""
        check_is_fitted(self, attributes="_models")
        return self.winner.predict_proba(X, **kwargs)

    @composed(crash, method_to_log, typechecked)
    def predict_log_proba(self, X: X_TYPES, **kwargs):
        """Get the winning model's log probability predictions on new data."""
        check_is_fitted(self, attributes="_models")
        return self.winner.predict_log_proba(X, **kwargs)

    @composed(crash, method_to_log, typechecked)
    def decision_function(self, X: X_TYPES, **kwargs):
        """Get the winning model's decision function on new data."""
        check_is_fitted(self, attributes="_models")
        return self.winner.decision_function(X, **kwargs)

    @composed(crash, method_to_log, typechecked)
    def score(
        self,
        X: X_TYPES,
        y: Y_TYPES,
        metric: Optional[Union[str, callable]] = None,
        sample_weight: Optional[SEQUENCE_TYPES] = None,
        **kwargs,
    ):
        """Get the winning model's score on new data."""
        check_is_fitted(self, attributes="_models")
        return self.winner.score(X, y, metric, sample_weight, **kwargs)

    # Utility methods ============================================== >>

    def _get_model_name(self, model):
        """Return a model's name.

        If there are multiple models that start with the same
        acronym, all are returned. If the input is a number,
        select all models that end with that number. The input
        is case-insensitive.

        """
        if model.lower() == "winner":
            return [self.winner.name]

        if model in self._models:
            return [self._models[model].name]

        to_return = []
        for key, value in self._models.items():
            key, model = key.lower(), model.lower()
            condition_1 = key.startswith(model)
            condition_2 = model.replace(".", "").isdigit() and key.endswith(model)
            if condition_1 or condition_2:
                to_return.append(value.name)

        if to_return:
            return to_return
        else:
            raise ValueError(
                f"Model {model} not found in the pipeline! The "
                f"available models are: {', '.join(self.models)}."
            )

    def _get_models(self, models=None):
        """Return models in the pipeline. Duplicate inputs are ignored."""
        if not models:
            return lst(self.models).copy()
        elif isinstance(models, str):
            return self._get_model_name(models.lower())
        else:
            to_return = []
            for m1 in models:
                for m2 in self._get_model_name(m1.lower()):
                    to_return.append(m2)

            return list(dict.fromkeys(to_return))  # Avoid duplicates

    @crash
    def available_models(self):
        """Give an overview of the available predefined models.

        Returns
        -------
        overview: pd.DataFrame
            Information about the predefined models available for the
            current task. Columns include:
                - acronym: Model's acronym (used to call the model).
                - name: Full name of the model.
                - estimator: The model's underlying estimator.
                - module: The estimator's module.
                - needs_scaling: Whether the model requires feature scaling.

        """
        overview = pd.DataFrame()
        for model in MODEL_LIST:
            m = model(self)
            est = m.get_estimator()
            if m.task[:3] == self.goal[:3] or m.task == "both":
                overview = overview.append(
                    {
                        "acronym": m.acronym,
                        "name": m.fullname,
                        "estimator": est.__class__.__name__,
                        "module": est.__module__,
                        "needs_scaling": str(m.needs_scaling),
                    },
                    ignore_index=True,
                )

        return overview

    @composed(crash, method_to_log, typechecked)
    def delete(self, models: Optional[Union[str, SEQUENCE_TYPES]] = None):
        """Delete models from the trainer's pipeline.

        Removes a model from the trainer. If the winning model is
        removed, the next best model (through `metric_test` or
        `mean_bootstrap`) is selected as winner. If all models are
        removed, the metric and training approach are reset. Use this
        method to drop unwanted models from the pipeline or to free
        some memory before saving. The model is not removed from any
        active mlflow experiment.

        Parameters
        ----------
        models: str, sequence or None, optional (default=None)
            Models to delete. If None, delete them all.

        """
        models = self._get_models(models)
        delete(self, models)
        self.log(f"Model{'' if len(models) == 1 else 's'} deleted successfully!", 1)

    @composed(crash, typechecked)
    def evaluate(
        self,
        metric: Optional[Union[str, callable, SEQUENCE_TYPES]] = None,
        dataset: str = "test",
    ):
        """Get all models' scores for the provided metrics.

        Parameters
        ----------
        metric: str, func, scorer, sequence or None, optional (default=None)
            Metric to calculate. If None, it returns an overview of
            the most common metrics per task.

        dataset: str, optional (default="test")
            Data set on which to calculate the metric. Options are
            "train" or "test".

        Returns
        -------
        scores: pd.DataFrame
            Scores of the models.

        """
        check_is_fitted(self, attributes="_models")

        scores = pd.DataFrame()
        for m in self._models:
            scores = scores.append(m.evaluate(metric, dataset=dataset))

        return scores

    @composed(crash, typechecked)
    def get_class_weight(self, dataset: str = "train"):
        """Return class weights for a balanced dataset.

        Statistically, the class weights re-balance the data set so
        that the sampled data set represents the target population
        as closely as possible. The returned weights are inversely
        proportional to the class frequencies in the selected data set.

        Parameters
        ----------
        dataset: str, optional (default="train")
            Data set from which to get the weights. Choose between
            "train", "test" or "dataset".

        Returns
        -------
        class_weights: dict
            Classes with the corresponding weights.

        """
        if self.goal != "class":
            raise PermissionError(
                "The balance method is only available for classification tasks!"
            )

        if dataset not in ("train", "test", "dataset"):
            raise ValueError(
                "Invalid value for the dataset parameter. "
                "Choose between 'train', 'test' or 'dataset'."
            )

        y = self.classes[dataset]
        return {idx: round(divide(sum(y), value), 3) for idx, value in y.iteritems()}

    @composed(crash, method_to_log, typechecked)
    def stacking(
        self,
        models: Optional[Union[str, SEQUENCE_TYPES]] = None,
        estimator: Optional[Union[str, callable]] = None,
        stack_method: str = "auto",
        passthrough: bool = False,
    ):
        """Add a Stacking instance to the models in the pipeline.

        Parameters
        ----------
        models: sequence or None, optional (default=None)
            Models that feed the stacking. If None, it selects all
            models depending on the current branch.

        estimator: str, callable or None, optional (default=None)
            The final estimator, which is used to combine the base
            estimators. If str, choose from ATOM's predefined models.
            If None, a default estimator is selected:
                - LogisticRegression for classification tasks.
                - Ridge for regression tasks.

        stack_method: str, optional (default="auto")
            Methods called for each base estimator. If "auto", it
            will try to invoke `predict_proba`, `decision_function`
            or `predict` in that order.

        passthrough: bool, optional (default=False)
            When False, only the predictions of estimators are used
            as training data for the final estimator. When True, the
            estimator is trained on the predictions as well as the
            original training data.

        """
        check_is_fitted(self, attributes="_models")

        if not models:
            models = self.branch._get_depending_models()
        if not estimator:
            estimator = "LR" if self.goal == "class" else "Ridge"

        self._models["stack"] = Stacking(
            self,
            models=self._get_models(models),
            estimator=estimator,
            stack_method=stack_method,
            passthrough=passthrough,
        )
        self.log(f"{self.stack.fullname} added to the models!", 1)

    @composed(crash, method_to_log, typechecked)
    def voting(
        self,
        models: Optional[Union[str, SEQUENCE_TYPES]] = None,
        weights: Optional[SEQUENCE_TYPES] = None,
    ):
        """Add a Voting instance to the models in the pipeline.

        Parameters
        ----------
        models: sequence or None, optional (default=None)
            Models that feed the voting. If None, it selects all models
            depending on the current branch.

        weights: sequence or None, optional (default=None)
            Sequence of weights (int or float) to weight the
            occurrences of predicted class labels (hard voting)
            or class probabilities before averaging (soft voting).
            If None, it uses uniform weights.

        """
        check_is_fitted(self, attributes="_models")

        if not models:
            models = self.branch._get_depending_models()

        self._models["vote"] = Voting(
            self,
            models=self._get_models(models),
            weights=weights,
        )
        self.log(f"{self.vote.fullname} added to the models!", 1)
