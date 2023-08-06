# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Module containing the Voting and Stacking classes.

"""

# Standard packages
import numpy as np
import pandas as pd
from copy import copy
from typing import Optional, Union
from typeguard import typechecked

# Own modules
from .branch import Branch
from .basemodel import BaseModel
from .data_cleaning import Scaler
from .models import MODEL_LIST
from .utils import (
    SEQUENCE_TYPES, flt, arr, merge, get_acronym, get_best_score,
    get_scorer, custom_transform, composed, crash, CustomDict,
)


class BaseEnsemble:
    """Base class for all ensembles."""

    def _process_branches(self, X, y, verbose, method):
        """Transform data through all branches.

        This method transforms provided data through all the branches
        from the models in the ensemble. Shared transformations are
        not repeated. Note that a unique copy of the data is stored
        per branch, so this method can cause memory issues for many
        branches or large datasets.

        """
        for m in self._models:
            if not hasattr(m.estimator, method):
                raise AttributeError(
                    f"{m.estimator.__class__.__name__} doesn't have a {method} method!"
                )

        # Branches used by the models in the instance
        branch_names = set(m.branch.name for m in self._models)
        branches = {k: v for k, v in self.T._branches.items() if k in branch_names}

        data = {k: (copy(X), copy(y)) for k in branch_names}
        step = {}  # Current step in the pipeline per branch
        for b1, v1 in branches.items():
            _print = True
            for idx, est in enumerate([t for t in v1.pipeline if not t._train_only]):
                # Skip if the transformation was already applied
                if step.get(b1, -1) < idx:
                    if _print:  # Just print message once per branch
                        _print = False
                        self.T.log(f"Transforming data for branch {b1}:", 1)
                    data[b1] = custom_transform(self.T, est, v1, data[b1], verbose)

                    for b2, v2 in branches.items():
                        if b1 != b2 and v2.pipeline.get(idx) is est:
                            # Update the data and step for the other branch
                            data[b2] = copy(data[b1])
                            step[b2] = idx

        return data


class Voting(BaseModel, BaseEnsemble):
    """Class for voting with the models in the pipeline."""

    acronym = "Vote"
    fullname = "Voting"

    def __init__(self, *args, models, weights):
        super().__init__(*args)

        self.models = models
        self.weights = weights
        self._pred_attrs = [None] * 12  # With score_train and score_test
        self._models = CustomDict(
            {k: v for k, v in self.T._models.items() if v.name in self.models}
        )

        if len(self.models) < 2:
            raise ValueError(
                "Invalid value for the models parameter. A Voting "
                "class should contain at least two models."
            )

        if self.weights and len(self.models) != len(self.weights):
            raise ValueError(
                "Invalid value for the weights parameter. Length should "
                "be equal to the number of models, got len(models)="
                f"{len(self.models)} and len(weights)={len(self.weights)}."
            )

    def __repr__(self):
        out_1 = f"{self.fullname}"
        out_1 += f"\n --> Models: {self.models}"
        out_1 += f"\n --> Weights: {self.weights}"
        out_2 = [
            f"{m.name}: {round(get_best_score(self, i), 4)}"
            for i, m in enumerate(self.T._metric)
        ]
        return out_1 + f"\n --> Evaluation: {'   '.join(out_2)}"

    @composed(crash, typechecked)
    def evaluate(
        self,
        metric: Optional[Union[str, callable, SEQUENCE_TYPES]] = None,
        dataset: str = "test",
    ):
        """Get the model's evaluation for provided metrics.

        Parameters
        ----------
        metric: str, scorer or None, optional (default=None)
            Metrics to calculate. If None, a selection of the most
            common metrics per task are used.

        dataset: str, optional (default="test")
            Data set on which to calculate the metric. Options are
            "train" or "test".

        Returns
        -------
        score: pd.Series
            Model's evaluation.

        """
        scores = pd.Series(name=self.name, dtype=float)

        # Get the scores from all models in the ensemble
        results = [m.evaluate(metric, dataset) for m in self._models]

        # Calculate averages per metric
        for idx in results[0].index:
            values = [x[idx] for x in results]
            scores[idx] = np.average(values, axis=0, weights=self.weights)

        return scores

    def _prediction(
        self,
        X,
        y=None,
        metric=None,
        sample_weight=None,
        verbose=None,
        method="predict"
    ):
        """Get the mean of the prediction methods on new data.

        Transform the new data and apply the attribute on all the
        models. All models need to have the provided attribute.

        Parameters
        ----------
        X: dict, list, tuple, np.array, sps.matrix or pd.DataFrame
            Feature set with shape=(n_samples, n_features).

        y: int, str, sequence or None, optional (default=None)
            - If None: y is ignored.
            - If int: Index of the target column in X.
            - If str: Name of the target column in X.
            - Else: Target column with shape=(n_samples,).

        metric: str, func, scorer or None, optional (default=None)
            Metric to calculate. Choose from any of sklearn's SCORERS,
            a function with signature metric(y_true, y_pred) or a scorer
            object. If None, it returns mean accuracy for classification
            tasks and r2 for regression tasks. Only for method="score".

        sample_weight: sequence or None, optional (default=None)
            Sample weights for the score method.

        verbose: int or None, optional (default=None)
            Verbosity level for the transformers. If None, it uses the
            estimator's own verbosity.

        method: str, optional (default="predict")
            Prediction method to be applied to the estimator.

        Returns
        -------
        pred: np.ndarray
            Return of the attribute.

        """
        data = self._process_branches(X, y, verbose, method)

        if method == "predict":
            pred = []
            for m in self._models:
                pred.append(m.predict(data[m.branch.name][0]))

            return np.apply_along_axis(
                func1d=lambda x: np.argmax(np.bincount(x, weights=self.weights)),
                axis=0,
                arr=np.array(pred).astype("int"),
            )

        elif method in ("predict_proba", "predict_log_proba", "decision_function"):
            pred = []
            for m in self._models:
                pred.append(getattr(m, method)(data[m.branch.name][0]))

            return np.average(pred, axis=0, weights=self.weights)

        elif method == "score":
            pred = []
            for m in self._models:
                pred.append(m.score(*data[m.branch.name], metric, sample_weight))

            return np.average(pred, axis=0, weights=self.weights)

    # Prediction properties ======================================== >>

    @property
    def metric_train(self):
        if self._pred_attrs[0] is None:
            pred = np.array([m.metric_train for m in self._models])
            self._pred_attrs[0] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[0]

    @property
    def metric_test(self):
        if self._pred_attrs[1] is None:
            pred = np.array([m.metric_test for m in self._models])
            self._pred_attrs[1] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[1]

    @property
    def predict_train(self):
        if self._pred_attrs[2] is None:
            pred = np.array([m.predict_train for m in self._models])
            self._pred_attrs[2] = np.apply_along_axis(
                func1d=lambda x: np.argmax(np.bincount(x, weights=self.weights)),
                axis=0,
                arr=pred.astype("int"),
            )
        return self._pred_attrs[2]

    @property
    def predict_test(self):
        if self._pred_attrs[3] is None:
            pred = np.array([m.predict_test for m in self._models])
            self._pred_attrs[3] = np.apply_along_axis(
                func1d=lambda x: np.argmax(np.bincount(x, weights=self.weights)),
                axis=0,
                arr=pred.astype("int"),
            )
        return self._pred_attrs[3]

    @property
    def predict_proba_train(self):
        if self._pred_attrs[4] is None:
            pred = np.array([m.predict_proba_train for m in self._models])
            self._pred_attrs[4] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[4]

    @property
    def predict_proba_test(self):
        if self._pred_attrs[5] is None:
            pred = np.array([m.predict_proba_test for m in self._models])
            self._pred_attrs[5] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[5]

    @property
    def predict_log_proba_train(self):
        if self._pred_attrs[6] is None:
            pred = np.array([m.predict_log_proba_train for m in self._models])
            self._pred_attrs[6] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[6]

    @property
    def predict_log_proba_test(self):
        if self._pred_attrs[7] is None:
            pred = np.array([m.predict_log_proba_test for m in self._models])
            self._pred_attrs[7] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[7]

    @property
    def decision_function_train(self):
        if self._pred_attrs[8] is None:
            pred = np.array([m.decision_function_train for m in self._models])
            self._pred_attrs[8] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[8]

    @property
    def decision_function_test(self):
        if self._pred_attrs[9] is None:
            pred = np.array([m.decision_function_test for m in self._models])
            self._pred_attrs[9] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[9]

    @property
    def score_train(self):
        if self._pred_attrs[10] is None:
            pred = np.array([m.score_train for m in self._models])
            self._pred_attrs[10] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[10]

    @property
    def score_test(self):
        if self._pred_attrs[11] is None:
            pred = np.array([m.score_test for m in self._models])
            self._pred_attrs[11] = np.average(pred, axis=0, weights=self.weights)
        return self._pred_attrs[11]


class Stacking(BaseModel, BaseEnsemble):
    """Class for stacking the models in the pipeline."""

    acronym = "Stack"
    fullname = "Stacking"

    def __init__(self, *args, models, estimator, stack_method, passthrough):
        super().__init__(*args)

        self.models = models
        self.estimator = estimator
        self.stack_method = stack_method
        self.passthrough = passthrough
        self._models = CustomDict(
            {k: v for k, v in self.T._models.items() if v.name in self.models}
        )
        self._fxs_scaler = None

        if len(self.models) < 2:
            raise ValueError(
                "Invalid value for the models parameter. A Stacking "
                "class should contain at least two models."
            )

        # Create the dataset for the Stacking instance
        dataset = pd.DataFrame()
        for m in self._models:
            attr = self._get_stack_attr(m)
            pred = np.concatenate(
                [getattr(m, f"{attr}_train"), getattr(m, f"{attr}_test")]
            )
            if attr == "predict_proba" and self.T.task.startswith("bin"):
                pred = pred[:, 1]

            if pred.ndim == 1:
                dataset[f"{attr}_{m.name}"] = pred
            else:
                for i in range(pred.shape[1]):
                    dataset[f"{attr}_{m.name}_{i}"] = pred[:, i]

        # Add scaled features from the branch to the set
        if self.passthrough:
            fxs = self.T.X  # Doesn't point to the same id
            if any(m.needs_scaling for m in self._models) and not self.T.scaled:
                self._fxs_scaler = Scaler().fit(self.T.X_train)
                fxs = self._fxs_scaler.transform(fxs)

            dataset = pd.concat([dataset, fxs], axis=1, join="inner")

        # The instance has its own internal branch
        self.branch = Branch(self, "StackBranch")
        self.branch.data = merge(dataset, self.T.y)
        self.branch.idx = self.T.branch.idx
        self._train_idx = self.branch.idx[0]

        if isinstance(self.estimator, str):
            # Add goal, n_jobs and random_state from trainer for the estimator
            self.goal = self.T.goal
            self.n_jobs = self.T.n_jobs
            self.random_state = self.T.random_state

            # Get one of ATOM's predefined models
            model = MODEL_LIST[get_acronym(self.estimator)](self)
            self.estimator = model.get_estimator()

        self.estimator.fit(self.X_train, self.y_train)

        # Save metric scores on complete training and test set
        self.metric_train = flt(
            [
                metric(self.estimator, arr(self.X_train), self.y_train)
                for metric in self.T._metric
            ]
        )
        self.metric_test = flt(
            [
                metric(self.estimator, arr(self.X_test), self.y_test)
                for metric in self.T._metric
            ]
        )

    def __repr__(self):
        out_1 = f"{self.fullname}"
        out_1 += f"\n --> Models: {self.models}"
        out_1 += f"\n --> Estimator: {self.estimator.__class__.__name__}"
        out_1 += f"\n --> Stack method: {self.stack_method}"
        out_1 += f"\n --> Passthrough: {self.passthrough}"
        out_2 = [
            f"{m.name}: {round(get_best_score(self, i), 4)}"
            for i, m in enumerate(self.T._metric)
        ]
        return out_1 + f"\n --> Evaluation: {'   '.join(out_2)}"

    def _get_stack_attr(self, model):
        """Get the stack attribute for a specific model."""
        if self.stack_method == "auto":
            if hasattr(model.estimator, "predict_proba"):
                return "predict_proba"
            elif hasattr(model.estimator, "decision_function"):
                return "decision_function"
            else:
                return "predict"

        return self.stack_method

    # Prediction methods =========================================== >>

    def _prediction(
        self,
        X,
        y=None,
        metric=None,
        sample_weight=None,
        verbose=None,
        method="predict"
    ):
        """Get the mean of the prediction methods on new data.

        First transform the new data and apply the attribute on all
        the models. All models need to have the provided attribute.

        Parameters
        ----------
        X: dict, list, tuple, np.array, sps.matrix or pd.DataFrame
            Feature set with shape=(n_samples, n_features).

        y: int, str, sequence or None, optional (default=None)
            - If None: y is ignored.
            - If int: Index of the target column in X.
            - If str: Name of the target column in X.
            - Else: Target column with shape=(n_samples,).

        metric: str, func, scorer or None, optional (default=None)
            Metric to calculate. Choose from any of sklearn's SCORERS,
            a function with signature metric(y_true, y_pred) or a scorer
            object. If None, it returns mean accuracy for classification
            tasks and r2 for regression tasks. Only for method="score".

        sample_weight: sequence or None, optional (default=None)
            Sample weights for the score method.

        verbose: int or None, optional (default=None)
            Verbosity level for the transformers. If None, it uses the
            estimator's own verbosity.

        method: str, optional (default="predict")
            Prediction method to be applied to the estimator.

        Returns
        -------
        pred: np.ndarray
            Return of the attribute.

        """
        data = self._process_branches(X, y, verbose, method)

        # Create the feature set from which to make predictions
        fxs_set = pd.DataFrame()
        for m in self._models:
            attr = self._get_stack_attr(m)
            pred = getattr(m, attr)(data[m.branch.name][0])
            if attr == "predict_proba" and self.T.task.startswith("bin"):
                pred = pred[:, 1]

            # Add features to the dataset
            if pred.ndim == 1:
                fxs_set[f"{attr}_{m.name}"] = pred
            else:
                for i in range(pred.shape[1]):
                    fxs_set[f"{attr}_{m.name}_{i}"] = pred[:, i]

        # Add scaled features from the branch to the set
        if self.passthrough:
            fxs_pass = self.T.X
            if self._fxs_scaler:
                fxs_pass = self._fxs_scaler.transform(fxs_pass)

            fxs_set = pd.concat([fxs_set, fxs_pass], axis=1, join="inner")

        if y is None:
            return getattr(self.estimator, method)(fxs_set)
        else:
            if metric is None:
                if self.T.goal == "class":
                    metric = get_scorer("accuracy")
                else:
                    metric = get_scorer("r2")
            else:
                metric = get_scorer(metric)

            kwargs = {}
            if sample_weight is not None:
                kwargs["sample_weight"] = sample_weight

            return metric(self.estimator, fxs_set, self.T.y, **kwargs)
