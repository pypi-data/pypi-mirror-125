# coding: utf-8

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Unit tests for modeloptimizer.py

"""

# Standard packages
import glob

import numpy as np
import pytest
from unittest.mock import patch
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from skopt.learning import GaussianProcessRegressor

# Own modules
from atom import ATOMClassifier, ATOMRegressor
from atom.training import DirectClassifier
from .utils import FILE_DIR, X_bin, y_bin, X_reg, y_reg, bin_train, bin_test


# Test utilities =================================================== >>

def test_scaler():
    """Assert that a scaler is made for models that need scaling."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(["LGB", "LDA"])
    assert atom.lgb.scaler and not atom.lda.scaler


def test_repr_method():
    """Assert that the __repr__ method works as intended."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LDA")
    assert str(atom.lda).startswith("Linear Discriminant")


# Test training ==================================================== >>

def test_n_calls_lower_n_initial_points():
    """Assert than an error is raised when n_calls<n_initial_points."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(["LR", "LDA"], n_calls=(5, 2), n_initial_points=(2, 3))
    assert atom.errors.get("LDA")


def test_est_params_removed_from_bo():
    """Assert that all params in est_params are dropped from the BO."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LGB", n_calls=5, est_params={"n_estimators": 220})
    assert "n_estimators" not in atom.lgb.bo.params[0]


def test_no_hyperparameters_left():
    """Assert that the BO is skipped when there are no hyperparameters."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(models="BNB", n_calls=10, est_params={"alpha": 1.0, "fit_prior": True})
    assert atom.bnb.bo.empty


def test_est_params_unknown_param():
    """Assert that unknown parameters in est_params are caught."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(["LR", "LGB"], n_calls=5, est_params={"test": 220})
    assert list(atom.errors.keys()) == ["LR"]  # LGB passes since it accepts kwargs


def test_est_params_unknown_param_fit():
    """Assert that unknown parameters in est_params_fit are caught."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    pytest.raises(RuntimeError, atom.run, ["LR", "LGB"], est_params={"test_fit": 220})


def test_est_params_default_method():
    """Assert that custom parameters overwrite the default ones."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("RF", est_params={"n_jobs": 3})
    assert atom.rf.estimator.get_params()["n_jobs"] == 3
    assert atom.rf.estimator.get_params()["random_state"] == 1


@pytest.mark.parametrize("est", ["GP", "ET", "RF", "GBRT", GaussianProcessRegressor()])
def test_all_base_estimators(est):
    """Assert that the pipeline works for all base estimators."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LR", n_calls=5, bo_params={"base_estimator": est})


def test_sample_weights_fit():
    """Assert that sample weights can be used with the BO."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(
        models="LGB",
        n_calls=5,
        est_params={"sample_weight_fit": list(range(len(atom.y_train)))},
    )


@pytest.mark.parametrize("model", ["XGB", "LGB", "CatB"])
def test_early_stopping(model):
    """Assert than early stopping works."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(model, n_calls=5, bo_params={"early_stopping": 0.1, "cv": 1})
    assert getattr(atom, model).evals


@pytest.mark.parametrize("model", ["XGB", "LGB", "CatB"])
def test_est_params_for_fit(model):
    """Assert that est_params is used for fit if ends in _fit."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(model, est_params={"early_stopping_rounds_fit": 2})
    assert getattr(atom, model)._stopped != ("---", "---")


def test_skip_duplicate_calls():
    """Assert that calls with the same parameters skip the calculation."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("dummy", n_calls=5)
    assert atom.dummy.bo["score"].nunique() < len(atom.dummy.bo["score"])


@patch("mlflow.set_tag")
def test_nested_runs_to_mlflow(mlflow):
    """Assert that the BO is logged to mlflow as nested runs."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.log_bo = True
    atom.run("Tree", n_calls=5)
    assert mlflow.call_count == 5  # Only called at iterations


def test_verbose_is_1():
    """Assert that the pipeline works for verbose=1."""
    atom = ATOMClassifier(X_bin, y_bin, verbose=1, random_state=1)
    atom.run("LR", n_calls=5)
    assert not atom.errors


@patch("mlflow.set_tags")
def test_run_set_tags_to_mlflow(mlflow):
    """Assert that the mlflow run gets tagged."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("GNB")
    mlflow.assert_called_with(
        {
            "fullname": atom.gnb.fullname,
            "branch": atom.gnb.branch.name,
            "time": atom.gnb.time_fit,
        }
    )


@patch("mlflow.log_params")
def test_run_log_params_to_mlflow(mlflow):
    """Assert that model parameters are logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("GNB")
    assert mlflow.call_count == 1


@patch("mlflow.log_metric")
def test_run_log_metric_to_mlflow(mlflow):
    """Assert that metrics are logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("GNB", metric=["f1", "recall", "accuracy"])
    assert mlflow.call_count == 3


@patch("mlflow.log_metric")
def test_run_log_evals_to_mlflow(mlflow):
    """Assert that eval metrics are logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("CatB")
    assert mlflow.call_count > 10


@patch("mlflow.sklearn.log_model")
def test_run_log_models_to_mlflow(mlflow):
    """Assert that models are logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.log_model = True
    atom.run("LGB")
    mlflow.assert_called_with(atom.lgb.estimator, "LGBMClassifier")


@patch("mlflow.log_artifact")
def test_run_log_data_to_mlflow(mlflow):
    """Assert that train and test sets are logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.log_data = True
    atom.run("GNB")
    assert mlflow.call_count == 2  # Train and test set


@patch("mlflow.sklearn.log_model")
def test_run_log_pipeline_to_mlflow(mlflow):
    """Assert that renaming also changes the mlflow run."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.log_pipeline = True
    atom.run("GNB")
    assert mlflow.call_count == 2  # Model + Pipeline


def test_bootstrap_attribute_types():
    """Assert that the bootstrap attributes have python types (not numpy)."""
    # For single-metric
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LGB", n_calls=5, n_bootstrap=5)
    assert isinstance(atom.lgb.metric_bootstrap, np.ndarray)
    assert isinstance(atom.lgb.mean_bootstrap, float)

    # For multi-metric
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LGB", metric=("f1", "auc", "recall"), n_bootstrap=5)
    assert isinstance(atom.lgb.metric_bootstrap, np.ndarray)
    assert isinstance(atom.lgb.mean_bootstrap, list)


# Test utility methods ============================================= >>

def test_calibrate_invalid_task():
    """Assert than an error is raised when task="regression"."""
    atom = ATOMRegressor(X_reg, y_reg, random_state=1)
    atom.run("OLS")
    pytest.raises(PermissionError, atom.ols.calibrate)


def test_calibrate():
    """Assert that calibrate method works as intended."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("MNB")
    atom.mnb.calibrate(cv=3)
    assert isinstance(atom.mnb.estimator, CalibratedClassifierCV)


def test_calibrate_prefit():
    """Assert that calibrate method works as intended when cv="prefit"."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("MNB")
    atom.mnb.calibrate(cv="prefit")
    assert isinstance(atom.mnb.estimator, CalibratedClassifierCV)


def test_calibrate_reset_predictions():
    """Assert that the prediction attributes are reset after calibrating."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("MNB")
    atom.mnb.calibrate()
    assert atom.mnb._pred_attrs[9] is None


@patch("mlflow.sklearn.log_model")
def test_calibrate_to_mlflow(mlflow):
    """Assert that the CCV is logged to mlflow."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("GNB")
    atom.gnb.calibrate()
    mlflow.assert_called_with(atom.gnb.estimator, "CalibratedClassifierCV")


def test_cross_validate():
    """Assert that the cross_validate method works as intended."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LR")
    assert isinstance(atom.lr.cross_validate(), dict)
    assert isinstance(atom.lr.cross_validate(scoring="AP"), dict)


def test_export_pipeline_atom():
    """Assert that the pipeline can be retrieved from the model."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("LR")
    assert len(atom.lr.export_pipeline()) == 2


def test_export_pipeline_trainer():
    """Assert that the pipeline can be retrieved from the model."""
    trainer = DirectClassifier("LR", random_state=1)
    trainer.run(bin_train, bin_test)
    assert len(trainer.lr.export_pipeline()) == 2


def test_full_train():
    """Assert that the full_train method returns a fitted estimator."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(["Tree", "LGB"])
    assert isinstance(atom.tree.full_train(), DecisionTreeClassifier)
    assert atom.lgb.full_train() is not atom.lgb.estimator


def test_rename():
    """Assert that the model's tag can be changed."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run(["MNB", "MNB_2"])
    pytest.raises(PermissionError, atom.mnb.rename, name="_2")
    atom.mnb.rename("_3")
    assert atom.models == ["MNB_3", "MNB_2"]
    atom.mnb_2.rename()
    assert atom.models == ["MNB_3", "MNB"]


@patch("mlflow.tracking.MlflowClient.set_tag")
def test_rename_to_mlflow(mlflow):
    """Assert that renaming also changes the mlflow run."""
    atom = ATOMClassifier(X_bin, y_bin, experiment="test", random_state=1)
    atom.run("GNB")
    atom.gnb.rename("GNB2")
    mlflow.assert_called_with(atom.gnb2._run.info.run_id, "mlflow.runName", "GNB2")


def test_save_estimator():
    """Assert that the save_estimator saves a pickle file."""
    atom = ATOMClassifier(X_bin, y_bin, random_state=1)
    atom.run("MNB")
    atom.mnb.save_estimator(FILE_DIR + "auto")
    assert glob.glob(FILE_DIR + "MultinomialNB")
