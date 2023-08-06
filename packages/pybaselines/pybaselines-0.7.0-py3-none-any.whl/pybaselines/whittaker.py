# -*- coding: utf-8 -*-
"""Whittaker-smoothing-based techniques for fitting baselines to experimental data.

Created on Sept. 13, 2019
@author: Donald Erb

"""

import warnings

import numpy as np
from scipy.linalg import solve_banded, solveh_banded
from scipy.special import expit

from ._algorithm_setup import _diff_1_diags, _setup_whittaker, _yx_arrays
from ._compat import _HAS_PENTAPY, _pentapy_solve
from .utils import (
    ParameterWarning, _mollifier_kernel, _pentapy_solver, _safe_std, pad_edges,
    padded_convolve, relative_difference
)


def _shift_rows(matrix, diagonals=2):
    """
    Shifts the rows of a matrix with equal number of upper and lower off-diagonals.

    Parameters
    ----------
    matrix : numpy.ndarray
        The matrix to be shifted. Note that all modifications are done in-place.
    diagonals : int
        The number of upper or lower (same for symmetric matrix) diagonals, not
        including the main diagonal. For example, a matrix with five diagonal rows
        would use a `diagonals` of 2.

    Returns
    -------
    matrix : numpy.ndarray
        The shifted matrix.

    Notes
    -----
    Necessary to match the diagonal matrix format required by SciPy's solve_banded
    function.

    Performs the following transformation (left is input, right is output):

        [[a b c ... d 0 0]        [[0 0 a ... b c d]
         [e f g ... h i 0]         [0 e f ... g h i]
         [j k l ... m n o]   -->   [j k l ... m n o]
         [0 p q ... r s t]         [p q r ... s t 0]
         [0 0 u ... v w x]]        [u v w ... x 0 0]]

    The right matrix would be directly obtained when using SciPy's sparse diagonal
    matrices, but when using multiplication with NumPy arrays, the result is the
    left matrix, which has to be shifted to match the desired format.

    """
    for row, shift in enumerate(range(-diagonals, 0)):
        matrix[row, -shift:] = matrix[row, :shift]
        matrix[row, :-shift] = 0

    for row, shift in enumerate(range(1, diagonals + 1), diagonals + 1):
        matrix[row, :-shift] = matrix[row, shift:]
        matrix[row, -shift:] = 0

    return matrix


def asls(data, lam=1e6, p=1e-2, diff_order=2, max_iter=50, tol=1e-3, weights=None):
    """
    Fits the baseline using asymmetric least squares (AsLS) fitting.

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e6.
    p : float, optional
        The penalizing weighting factor. Must be between 0 and 1. Values greater
        than the baseline will be given p weight, and values less than the baseline
        will be given p-1 weight. Default is 1e-2.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    Raises
    ------
    ValueError
        Raised if p is not between 0 and 1.

    References
    ----------
    Eilers, P. A Perfect Smoother. Analytical Chemistry, 2003, 75(14), 3631-3636.

    Eilers, P., et al. Baseline correction with asymmetric least squares smoothing.
    Leiden University Medical Centre Report, 2005, 1(1).

    """
    if not 0 < p < 1:
        raise ValueError('p must be between 0 and 1')
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, not using_pentapy, using_pentapy
    )
    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    for i in range(max_iter + 1):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(diagonals, weight_array * y, True, True, _pentapy_solver())
        else:
            baseline = solveh_banded(
                diagonals, weight_array * y, overwrite_b=True, check_finite=False
            )
        mask = y > baseline
        new_weights = p * mask + (1 - p) * (~mask)
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i + 1]}

    return baseline, params


def iasls(data, x_data=None, lam=1e6, p=1e-2, lam_1=1e-4, max_iter=50, tol=1e-3, weights=None):
    """
    Fits the baseline using the improved asymmetric least squares (IAsLS) algorithm.

    The algorithm consideres both the first and second derivatives of the residual.

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    x_data : array-like, shape (N,), optional
        The x-values of the measured data. Default is None, which will create an
        array from -1 to 1 with N points.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e6.
    p : float, optional
        The penalizing weighting factor. Must be between 0 and 1. Values greater
        than the baseline will be given p weight, and values less than the baseline
        will be given p-1 weight. Default is 1e-2.
    lam_1 : float, optional
        The smoothing parameter for the first derivative. Default is 1e-4.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be set by fitting the data with a second order polynomial.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    Raises
    ------
    ValueError
        Raised if p is not between 0 and 1.

    References
    ----------
    He, S., et al. Baseline correction for raman spectra using an improved
    asymmetric least squares method, Analytical Methods, 2014, 6(12), 4402-4407.

    """
    if not 0 < p < 1:
        raise ValueError('p must be between 0 and 1')
    if weights is None:
        y, x = _yx_arrays(data, x_data)
        baseline = np.polynomial.Polynomial.fit(x, y, 2)(x)
        mask = y > baseline
        weights = p * mask + (1 - p) * (~mask)

        _, d2_diags, weight_array = _setup_whittaker(
            y, lam, 2, weights, False, not _HAS_PENTAPY, _HAS_PENTAPY
        )
    else:
        y, d2_diags, weight_array = _setup_whittaker(
            data, lam, 2, weights, False, not _HAS_PENTAPY, _HAS_PENTAPY
        )

    diagonals = (
        d2_diags
        + _diff_1_diags(y.shape[0], not _HAS_PENTAPY, True)[::-1 if _HAS_PENTAPY else 1]
    )
    main_diag_idx = 2 if _HAS_PENTAPY else -1
    main_diagonal = diagonals[main_diag_idx].copy()

    # lam_1 * D_1.T * D_1 * y
    d1_y = y.copy()
    d1_y[0] = y[0] - y[1]
    d1_y[-1] = y[-1] - y[-2]
    d1_y[1:-1] = 2 * y[1:-1] - y[:-2] - y[2:]
    d1_y = lam_1 * d1_y
    tol_history = np.empty(max_iter + 1)
    for i in range(max_iter + 1):
        weight_squared = weight_array * weight_array
        diagonals[main_diag_idx] = main_diagonal + weight_squared
        if _HAS_PENTAPY:
            baseline = _pentapy_solve(
                diagonals, weight_squared * y + d1_y, True, True, _pentapy_solver()
            )
        else:
            baseline = solveh_banded(
                diagonals, weight_squared * y + d1_y, overwrite_b=True, check_finite=False
            )
        mask = y > baseline
        new_weights = p * mask + (1 - p) * (~mask)
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i + 1]}

    return baseline, params


def airpls(data, lam=1e6, diff_order=2, max_iter=50, tol=1e-3, weights=None):
    """
    Adaptive iteratively reweighted penalized least squares (airPLS) baseline.

    Parameters
    ----------
    data : array-like
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e6.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    References
    ----------
    Zhang, Z.M., et al. Baseline correction using adaptive iteratively
    reweighted penalized least squares. Analyst, 2010, 135(5), 1138-1146.

    """
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, True, not using_pentapy, using_pentapy
    )
    y_l1_norm = np.abs(y).sum()
    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    # Have to have extensive error handling since the weights can all become
    # very small due to the exp(i) term if too many iterations are performed;
    # checking the negative residual length usually prevents any errors, but
    # sometimes not so have to also catch any errors from the solvers
    for i in range(1, max_iter + 2):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            output = _pentapy_solve(
                diagonals, weight_array * y, True, True, _pentapy_solver()
            )
            # if weights are all ~0, then pentapy sometimes outputs nan without
            # warnings or errors, so have to check
            if np.isfinite(output.dot(output)):
                baseline = output
            else:
                warnings.warn(
                    ('error occurred during fitting, indicating that "tol"'
                     ' is too low, "max_iter" is too high, or "lam" is too high'),
                    ParameterWarning
                )
                i -= 1  # reduce i so that output tol_history indexing is correct
                break
        else:
            try:
                output = solveh_banded(
                    diagonals, weight_array * y, overwrite_b=True, check_finite=False
                )
            except np.linalg.LinAlgError:
                warnings.warn(
                    ('error occurred during fitting, indicating that "tol"'
                     ' is too low, "max_iter" is too high, or "lam" is too high'),
                    ParameterWarning
                )
                i -= 1  # reduce i so that output tol_history indexing is correct
                break
            else:
                baseline = output

        residual = y - baseline
        neg_mask = residual < 0
        neg_residual = residual[neg_mask]
        if len(neg_residual) < 2:
            # exit if there are < 2 negative residuals since all points or all but one
            # point would get a weight of 0, which fails the solver
            warnings.warn(
                ('almost all baseline points are below the data, indicating that "tol"'
                 ' is too low and/or "max_iter" is too high'), ParameterWarning
            )
            i -= 1  # reduce i so that output tol_history indexing is correct
            break

        residual_l1_norm = abs(neg_residual.sum())
        calc_difference = residual_l1_norm / y_l1_norm
        tol_history[i - 1] = calc_difference
        if calc_difference < tol:
            break
        # only use negative residual in exp to avoid exponential overflow warnings
        # and accidently creating a weight of nan (inf * 0 = nan)
        weight_array[neg_mask] = np.exp(i * neg_residual / residual_l1_norm)
        weight_array[~neg_mask] = 0

    params = {'weights': weight_array, 'tol_history': tol_history[:i]}

    return baseline, params


def arpls(data, lam=1e5, diff_order=2, max_iter=50, tol=1e-3, weights=None):
    """
    Asymmetrically reweighted penalized least squares smoothing (arPLS).

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e5.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    References
    ----------
    Baek, S.J., et al. Baseline correction using asymmetrically reweighted
    penalized least squares smoothing. Analyst, 2015, 140, 250-257.

    """
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, not using_pentapy, using_pentapy
    )
    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    for i in range(max_iter + 1):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(
                diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solveh_banded(
                diagonals, weight_array * y, overwrite_b=True, check_finite=False
            )
        residual = y - baseline
        neg_residual = residual[residual < 0]
        std = _safe_std(neg_residual, ddof=1)  # use dof=1 since sampling subset
        # add a negative sign since expit performs 1/(1+exp(-input))
        new_weights = expit(-(2 / std) * (residual - (2 * std - np.mean(neg_residual))))
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i + 1]}

    return baseline, params


def drpls(data, lam=1e5, eta=0.5, max_iter=50, tol=1e-3, weights=None):
    """
    Doubly reweighted penalized least squares (drPLS) baseline.

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e5.
    eta : float
        A term for controlling the value of lam; should be between 0 and 1.
        Low values will produce smoother baselines, while higher values will
        more aggressively fit peaks. Default is 0.5.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    References
    ----------
    Xu, D. et al. Baseline correction method based on doubly reweighted
    penalized least squares, Applied Optics, 2019, 58, 3913-3920.

    """
    y, d2_diagonals, weight_array = _setup_whittaker(data, lam, 2, weights, False, False)
    d1_d2_diagonals = d2_diagonals + _diff_1_diags(y.shape[0], False, True)
    if _HAS_PENTAPY:
        d1_d2_diagonals = d1_d2_diagonals[::-1]
    # identity - eta * D_2.T * D_2; overwrite d2_diagonals since it's no longer needed;
    # reversed to match the original diagonal structure of the D_2.T * D_2 sparse matrix
    d2_diagonals = -eta * d2_diagonals[::-1]
    d2_diagonals[2] += 1.
    tol_history = np.empty(max_iter + 1)
    for i in range(1, max_iter + 2):
        d2_w_diagonals = d2_diagonals * weight_array
        if _HAS_PENTAPY:
            baseline = _pentapy_solve(
                d1_d2_diagonals + d2_w_diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solve_banded(
                (2, 2), d1_d2_diagonals + _shift_rows(d2_w_diagonals), weight_array * y,
                overwrite_b=True, overwrite_ab=True, check_finite=False
            )
        residual = y - baseline
        neg_residual = residual[residual < 0]
        std = _safe_std(neg_residual, ddof=1)  # use dof=1 since only sampling a subset
        inner = (np.exp(i) / std) * (residual - (2 * std - np.mean(neg_residual)))
        new_weights = 0.5 * (1 - (inner / (1 + np.abs(inner))))
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i - 1] = calc_difference
        if not np.isfinite(calc_difference):
            # catches nan, inf and -inf due to exp(i) being too high or if there
            # are too few negative residuals; no way to catch both conditions before
            # new_weights calculation since it is hard to estimate if
            # (exp(i) / std) * residual will overflow; check calc_difference rather
            # than checking new_weights since non-finite values rarely occur and
            # checking a scalar is faster; cannot use np.errstate since it is not 100% reliable
            warnings.warn(
                ('nan and/or +/- inf occurred in weighting calculation, likely meaning '
                 '"tol" is too low and/or "max_iter" is too high'), ParameterWarning
            )
            break
        elif calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i]}

    return baseline, params


def iarpls(data, lam=1e5, diff_order=2, max_iter=50, tol=1e-3, weights=None):
    """
    Improved asymmetrically reweighted penalized least squares smoothing (IarPLS).

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e5.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    References
    ----------
    Ye, J., et al. Baseline correction method based on improved asymmetrically
    reweighted penalized least squares for Raman spectrum. Applied Optics, 2020,
    59, 10933-10943.

    """
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, not using_pentapy, using_pentapy
    )
    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    for i in range(1, max_iter + 2):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(
                diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solveh_banded(
                diagonals, weight_array * y, overwrite_b=True, check_finite=False
            )
        residual = y - baseline
        std = _safe_std(residual[residual < 0], ddof=1)  # dof=1 since sampling a subset
        inner = (np.exp(i) / std) * (residual - 2 * std)
        new_weights = 0.5 * (1 - (inner / np.sqrt(1 + inner**2)))
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i - 1] = calc_difference
        if not np.isfinite(calc_difference):
            # catches nan, inf and -inf due to exp(i) being too high or if there
            # are too few negative residuals; no way to catch both conditions before
            # new_weights calculation since it is hard to estimate if
            # (exp(i) / std) * residual will overflow; check calc_difference rather
            # than checking new_weights since non-finite values rarely occur and
            # checking a scalar is faster; cannot use np.errstate since it is not 100% reliable
            warnings.warn(
                ('nan and/or +/- inf occurred in weighting calculation, likely meaning '
                 '"tol" is too low and/or "max_iter" is too high'), ParameterWarning
            )
            break
        elif calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i]}

    return baseline, params


def aspls(data, lam=1e5, diff_order=2, max_iter=100, tol=1e-3, weights=None, alpha=None):
    """
    Adaptive smoothness penalized least squares smoothing (asPLS).

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e5.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.
    alpha : array-like, shape (N,), optional
        An array of values that control the local value of `lam` to better
        fit peak and non-peak regions. If None (default), then the initial values
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'alpha': numpy.ndarray, shape (N,)
            The array of alpha values used for fitting the data in the final iteration.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    Raises
    ------
    ValueError
        Raised if `alpha` and `data` do not have the same shape.

    References
    ----------
    Zhang, F., et al. Baseline correction for infrared spectra using
    adaptive smoothness parameter penalized least squares method.
    Spectroscopy Letters, 2020, 53(3), 222-233.

    """
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, False, True
    )
    if alpha is None:
        alpha_array = np.ones_like(weight_array)
    else:
        alpha_array = np.asarray(alpha)
        if alpha_array.shape != y.shape:
            raise ValueError('alpha must have the same shape as the input data')

    lower_upper = (diff_order, diff_order)
    tol_history = np.empty(max_iter + 1)
    for i in range(1, max_iter + 2):
        alpha_diagonals = diagonals * alpha_array
        alpha_diagonals[diff_order] = alpha_diagonals[diff_order] + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(
                alpha_diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solve_banded(
                lower_upper, _shift_rows(alpha_diagonals, diff_order), weight_array * y,
                overwrite_ab=True, overwrite_b=True, check_finite=False
            )
        residual = y - baseline
        std = _safe_std(residual[residual < 0], ddof=1)  # use dof=1 since sampling a subset
        # add a negative sign since expit performs 1/(1+exp(-input))
        new_weights = expit(-(2 / std) * (residual - std))
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i - 1] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights
        abs_d = np.abs(residual)
        alpha_array = abs_d / abs_d.max()

    params = {
        'weights': weight_array, 'alpha': alpha_array, 'tol_history': tol_history[:i]
    }

    return baseline, params


def psalsa(data, lam=1e5, p=0.5, k=None, diff_order=2, max_iter=50, tol=1e-3, weights=None):
    """
    Peaked Signal's Asymmetric Least Squares Algorithm (psalsa).

    Similar to the asymmetric least squares (AsLS) algorithm, but applies an
    exponential decay weighting to values greater than the baseline to allow
    using a higher `p` value to better fit noisy data.

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e6.
    p : float, optional
        The penalizing weighting factor. Must be between 0 and 1. Values greater
        than the baseline will be given p weight, and values less than the baseline
        will be given p-1 weight. Default is 0.5.
    k : float, optional
        A factor that controls the exponential decay of the weights for baseline
        values greater than the data. Should be approximately the height at which
        a value could be considered a peak. Default is None, which sets `k` to
        one-tenth of the standard deviation of the input data. A large k value
        will produce similar results to :func:`.asls`.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    Raises
    ------
    ValueError
        Raised if p is not between 0 and 1.

    Notes
    -----
    The exit criteria for the original algorithm was to check whether the signs
    of the residuals do not change between two iterations, but the comparison of
    the l2 norms of the weight arrays between iterations is used instead to be
    more comparable to other Whittaker-smoothing-based algorithms.

    References
    ----------
    Oller-Moreno, S., et al. Adaptive Asymmetric Least Squares baseline estimation
    for analytical instruments. 2014 IEEE 11th International Multi-Conference on
    Systems, Signals, and Devices, 2014, 1-5.

    """
    if not 0 < p < 1:
        raise ValueError('p must be between 0 and 1')
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, not using_pentapy, using_pentapy
    )
    if k is None:
        k = np.std(y) / 10

    num_y = y.shape[0]
    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    for i in range(max_iter + 1):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(
                diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solveh_banded(
                diagonals, weight_array * y, overwrite_b=True, check_finite=False
            )
        residual = y - baseline
        # only use positive residual in exp to avoid exponential overflow warnings
        # and accidently creating a weight of nan (inf * 0 = nan)
        new_weights = np.full(num_y, 1 - p, dtype=float)
        mask = residual > 0
        new_weights[mask] = p * np.exp(-residual[mask] / k)
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i + 1]}

    return baseline, params


def derpsalsa(data, lam=1e6, p=0.01, k=None, diff_order=2, max_iter=50, tol=1e-3,
              weights=None, smooth_half_window=None, num_smooths=16, **pad_kwargs):
    """
    Derivative Peak-Screening Asymmetric Least Squares Algorithm (derpsalsa).

    Parameters
    ----------
    data : array-like, shape (N,)
        The y-values of the measured data, with N data points. Must not
        contain missing data (NaN) or Inf.
    lam : float, optional
        The smoothing parameter. Larger values will create smoother baselines.
        Default is 1e6.
    p : float, optional
        The penalizing weighting factor. Must be between 0 and 1. Values greater
        than the baseline will be given p weight, and values less than the baseline
        will be given p-1 weight. Default is 0.1.
    k : float, optional
        A factor that controls the exponential decay of the weights for baseline
        values greater than the data. Should be approximately the height at which
        a value could be considered a peak. Default is None, which sets `k` to
        one-tenth of the standard deviation of the input data. A large k value
        will produce similar results to :func:`.asls`.
    diff_order : int, optional
        The order of the differential matrix. Must be greater than 0. Default is 2
        (second order differential matrix). Typical values are 2 or 1.
    max_iter : int, optional
        The max number of fit iterations. Default is 50.
    tol : float, optional
        The exit criteria. Default is 1e-3.
    weights : array-like, shape (N,), optional
        The weighting array. If None (default), then the initial weights
        will be an array with size equal to N and all values set to 1.
    smooth_half_window : int, optional
        The half-window to use for smoothing the data before computing the first
        and second derivatives. Default is None, which will use ``len(data) / 200``.
    num_smooths : int, optional
        The number of times to smooth the data before computing the first
        and second derivatives. Default is 16.
    **pad_kwargs
        Additional keyword arguments to pass to :func:`.pad_edges` for padding
        the edges of the data to prevent edge effects from smoothing.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    params : dict
        A dictionary with the following items:

        * 'weights': numpy.ndarray, shape (N,)
            The weight array used for fitting the data.
        * 'tol_history': numpy.ndarray
            An array containing the calculated tolerance values for
            each iteration. The length of the array is the number of iterations
            completed. If the last value in the array is greater than the input
            `tol` value, then the function did not converge.

    Raises
    ------
    ValueError
        Raised if p is not between 0 and 1.

    References
    ----------
    Korepanov, V. Asymmetric least-squares baseline algorithm with peak screening for
    automatic processing of the Raman spectra. Journal of Raman Spectroscopy. 2020,
    51(10), 2061-2065.

    """
    if not 0 < p < 1:
        raise ValueError('p must be between 0 and 1')
    using_pentapy = _HAS_PENTAPY and diff_order == 2
    y, diagonals, weight_array = _setup_whittaker(
        data, lam, diff_order, weights, False, not using_pentapy, using_pentapy
    )
    if k is None:
        k = np.std(y) / 10
    num_y = y.shape[0]
    if smooth_half_window is None:
        smooth_half_window = num_y // 200
    # could pad the data every iteration, but it is ~2-3 times slower and only affects
    # the edges, so it's not worth it
    y_smooth = pad_edges(y, smooth_half_window, **pad_kwargs)
    if smooth_half_window > 0:
        smooth_kernel = _mollifier_kernel(smooth_half_window)
        for _ in range(num_smooths):
            y_smooth = padded_convolve(y_smooth, smooth_kernel)
    y_smooth = y_smooth[smooth_half_window:num_y + smooth_half_window]

    diff_y_1 = np.gradient(y_smooth)
    diff_y_2 = np.gradient(diff_y_1)
    # x.dot(x) is same as (x**2).sum() but faster
    rms_diff_1 = np.sqrt(diff_y_1.dot(diff_y_1) / num_y)
    rms_diff_2 = np.sqrt(diff_y_2.dot(diff_y_2) / num_y)

    diff_1_weights = np.exp(-((diff_y_1 / rms_diff_1)**2) / 2)
    diff_2_weights = np.exp(-((diff_y_2 / rms_diff_2)**2) / 2)
    partial_weights = diff_1_weights * diff_2_weights

    main_diag_idx = diff_order if using_pentapy else -1
    main_diagonal = diagonals[main_diag_idx].copy()
    tol_history = np.empty(max_iter + 1)
    for i in range(max_iter + 1):
        diagonals[main_diag_idx] = main_diagonal + weight_array
        if using_pentapy:
            baseline = _pentapy_solve(
                diagonals, weight_array * y, True, True, _pentapy_solver()
            )
        else:
            baseline = solveh_banded(
                diagonals, weight_array * y, overwrite_b=True, check_finite=False
            )
        residual = y - baseline
        # no need for caution since inner exponential is always negative, but still mask
        # since it's faster than performing the square and exp on the full residual
        new_weights = np.full(num_y, 1 - p, dtype=float)
        mask = residual > 0
        new_weights[mask] = p * np.exp(-((residual[mask] / k)**2) / 2)
        # reference is not clear as to how p and 1-p are applied; an alternative could
        # be that partial_weights are multiplied only where residual > 0 and that all
        # other weights are 1-p, but based on Figure 1c in the reference, total weights
        # are never greater than partial_weights, so that must mean the non-peak regions
        # have a weight of (1-p) * partial_weights rather than just 1-p; both weighting
        # systems give near identical results, so it is not a big deal
        new_weights *= partial_weights
        calc_difference = relative_difference(weight_array, new_weights)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break
        weight_array = new_weights

    params = {'weights': weight_array, 'tol_history': tol_history[:i + 1]}

    return baseline, params
