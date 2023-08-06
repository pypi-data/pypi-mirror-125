"""Sample size calculation module 

"""

from __future__ import annotations

import math

from typing import Optional, Union

import numpy as np
import pandas as pd

from scipy.stats import nct
from scipy.stats import norm as normal
from scipy.stats import t as student

from samplics.utils.formats import convert_numbers_to_dicts, dict_to_dataframe, numpy_array
from samplics.utils.types import Array, DictStrNum, Number, StringNumber


class SampleSize:
    """*SampleSize* implements sample size calculation methods"""

    def __init__(
        self, parameter: str = "proportion", method: str = "wald", stratification: bool = False
    ) -> None:

        self.parameter = parameter.lower()
        self.method = method.lower()
        if self.method not in ("wald", "fleiss"):
            raise AssertionError("Sample size calculation method not valid.")
        self.stratification = stratification
        self.target: Union[DictStrNum, Number]
        self.samp_size: Union[DictStrNum, Number] = 0
        self.deff_c: Union[DictStrNum, Number] = 1.0
        self.deff_w: Union[DictStrNum, Number] = 1.0
        self.half_ci: Union[DictStrNum, Number]
        self.resp_rate: Union[DictStrNum, Number] = 1.0
        self.pop_size: Optional[Union[DictStrNum, Number]] = None

    def icc(self) -> Union[DictStrNum, Number]:
        pass

    def deff(
        self,
        cluster_size: Union[DictStrNum, Number],
        icc: Union[DictStrNum, Number],
    ) -> Union[DictStrNum, Number]:

        if isinstance(cluster_size, (int, float)) and isinstance(icc, (int, float)):
            return max(1 + (cluster_size - 1) * icc, 0)
        elif isinstance(cluster_size, dict) and isinstance(icc, dict):
            if cluster_size.keys() != icc.keys():
                raise AssertionError("Parameters do not have the same dictionary keys.")
            deff_c: DictStrNum = {}
            for s in cluster_size:
                deff_c[s] = max(1 + (cluster_size[s] - 1) * icc[s], 0)
            return deff_c
        else:
            raise ValueError("Combination of types not supported.")

    def _calculate_wald(
        self,
        target: Union[DictStrNum, Number],
        half_ci: Union[DictStrNum, Number],
        pop_size: Optional[Union[DictStrNum, Number]],
        stratum: Optional[Array],
    ) -> Union[DictStrNum, Number]:

        z_value = normal().ppf(1 - self.alpha / 2)

        if (
            isinstance(target, dict)
            and isinstance(half_ci, dict)
            and isinstance(self.deff_c, dict)
            and stratum is not None
        ):
            samp_size: DictStrNum = {}
            for s in stratum:
                sigma_s = target[s] * (1 - target[s])
                if isinstance(pop_size, dict):
                    samp_size[s] = math.ceil(
                        self.deff_c[s]
                        * pop_size[s]
                        * z_value ** 2
                        * sigma_s
                        / ((pop_size[s] - 1) * half_ci[s] ** 2 + z_value * sigma_s)
                    )
                else:
                    samp_size[s] = math.ceil(
                        self.deff_c[s] * z_value ** 2 * sigma_s / half_ci[s] ** 2
                    )
            return samp_size
        elif (
            isinstance(target, (int, float))
            and isinstance(half_ci, (int, float))
            and isinstance(self.deff_c, (int, float))
        ):
            sigma = target * (1 - target)
            if isinstance(pop_size, (int, float)):
                return math.ceil(
                    self.deff_c
                    * pop_size
                    * z_value ** 2
                    * sigma
                    / ((pop_size - 1) * half_ci ** 2 + z_value * sigma)
                )
            else:
                return math.ceil(self.deff_c * z_value ** 2 * sigma / half_ci ** 2)
        else:
            raise TypeError("target and half_ci must be numbers or dictionnaires!")

    def _calculate_fleiss(
        self,
        target: Union[DictStrNum, Number],
        half_ci: Union[DictStrNum, Number],
        # pop_size: Optional[Union[DictStrNum, Number]],
        stratum: Optional[Array],
    ) -> Union[DictStrNum, Number]:

        z_value = normal().ppf(1 - self.alpha / 2)

        def fleiss_factor(p: float, d: float) -> float:

            if 0 <= p < d or 1 - d < p <= 1:
                return 8 * d * (1 - 2 * d)
            elif d <= p < 0.3:
                return 4 * (p + d) * (1 - p - d)
            elif 0.7 < p <= 1 - d:
                return 4 * (p - d) * (1 - p + d)
            elif 0.3 <= p <= 0.7:
                return 1
            else:
                raise ValueError("Parameters p or d not valid.")

        if (
            self.stratification
            and isinstance(target, dict)
            and isinstance(half_ci, dict)
            and isinstance(self.deff_c, dict)
            and stratum is not None
        ):
            samp_size: DictStrNum = {}
            for s in stratum:
                fct = fleiss_factor(target[s], half_ci[s])
                samp_size[s] = math.ceil(
                    self.deff_c[s]
                    * (
                        fct * (z_value ** 2) / (4 * half_ci[s] ** 2)
                        + 1 / half_ci[s]
                        - 2 * z_value ** 2
                        + (z_value + 2) / fct
                    )
                )
            return samp_size
        elif (
            not self.stratification
            and isinstance(target, (int, float))
            and isinstance(half_ci, (int, float))
            and isinstance(self.deff_c, (int, float))
        ):
            fct = fleiss_factor(target, half_ci)
            return math.ceil(
                self.deff_c
                * (
                    fct * (z_value ** 2) / (4 * half_ci ** 2)
                    + 1 / half_ci
                    - 2 * z_value ** 2
                    + (z_value + 2) / fct
                )
            )
        else:
            raise TypeError("target and half_ci must be numbers or dictionnaires!")

    def calculate(
        self,
        target: Union[DictStrNum, Number],
        half_ci: Union[DictStrNum, Number],
        deff: Union[DictStrNum, Number, Number] = 1.0,
        resp_rate: Union[DictStrNum, Number] = 1.0,
        number_strata: Optional[int] = None,
        pop_size: Optional[Union[DictStrNum, Number]] = None,
        alpha: float = 0.05,
    ) -> None:
        """calculate the sample allocation.

        Args:
            target (Union[dict[Any, Number], Number]): the expected proportion used to calculate
                the sample size. It can be a single number for non-stratified designs or if all the strata have the same targeted proportion. Use a dictionary for stratified designs.
            half_ci (Union[dict[Any, Number], Number]): level of half_ci or half confidence
                interval. It can be a single number for non-stratified designs or if all the strata have the same targeted proportion. Use a dictionary for stratified designs.
            deff (Union[dict[Any, float], float], optional): design effect. It can be a single
                number for non-stratified designs or if all the strata have the same targeted proportion. Use a dictionary for stratified designs.. Defaults to 1.0.
            resp_rate (Union[dict[Any, float], float], optional): expected response rate. It can
                be a single number for non-stratified designs or if all the strata have the same targeted proportion. Use a dictionary for stratified designs.. Defaults to 1.0.
            number_strata (Optional[int], optional): number of strata. Defaults to None.
            alpha (float, optional): level of significance. Defaults to 0.05.

        Raises:
            AssertionError: when a dictionary is provided for a non-stratified design.
            AssertionError: when the dictionaries have different keys.
        """

        is_target_dict = isinstance(target, dict)
        is_half_ci_dict = isinstance(half_ci, dict)
        is_deff_dict = isinstance(deff, dict)
        is_resp_rate_dict = isinstance(resp_rate, dict)
        is_pop_size_dict = isinstance(resp_rate, dict)

        number_dictionaries = (
            is_target_dict + is_half_ci_dict + is_deff_dict + is_resp_rate_dict + is_pop_size_dict
        )

        stratum: Optional[list[StringNumber]] = None
        if not self.stratification and (
            isinstance(target, dict)
            or isinstance(half_ci, dict)
            or isinstance(deff, dict)
            or isinstance(resp_rate, dict)
            or isinstance(pop_size, dict)
        ):
            raise AssertionError("No python dictionary needed for non-stratified sample.")
        elif (
            not self.stratification
            and isinstance(target, (int, float))
            and isinstance(half_ci, (int, float))
            and isinstance(deff, (int, float))
            and isinstance(resp_rate, (int, float))
        ):
            self.deff_c = deff
            self.target = target
            self.half_ci = half_ci
            self.resp_rate = resp_rate
        elif (
            self.stratification
            and isinstance(target, (int, float))
            and isinstance(half_ci, (int, float))
            and isinstance(deff, (int, float))
            and isinstance(resp_rate, (int, float))
        ):
            if number_strata is not None:
                stratum = ["_stratum_" + str(i) for i in range(1, number_strata + 1)]
                self.target = dict(zip(stratum, np.repeat(target, number_strata)))
                self.half_ci = dict(zip(stratum, np.repeat(half_ci, number_strata)))
                self.deff_c = dict(zip(stratum, np.repeat(deff, number_strata)))
                self.resp_rate = dict(zip(stratum, np.repeat(resp_rate, number_strata)))
                if isinstance(pop_size, (int, float)):
                    self.pop_size = dict(zip(stratum, np.repeat(pop_size, number_strata)))
            else:
                raise ValueError("Number of strata not specified!")
        elif self.stratification and number_dictionaries > 0:
            dict_number = 0
            for ll in [target, half_ci, deff, resp_rate]:
                if isinstance(ll, dict):
                    dict_number += 1
                    if dict_number == 1:
                        stratum = list(ll.keys())
                    elif dict_number > 0:
                        if stratum != list(ll.keys()):
                            raise AssertionError("Python dictionaries have different keys")
            number_strata = len(stratum) if stratum is not None else 0
            if not is_target_dict and isinstance(target, (int, float)) and stratum is not None:
                self.target = dict(zip(stratum, np.repeat(target, number_strata)))
            elif isinstance(target, dict):
                self.target = target
            if not is_half_ci_dict and isinstance(half_ci, (int, float)) and stratum is not None:
                self.half_ci = dict(zip(stratum, np.repeat(half_ci, number_strata)))
            elif isinstance(half_ci, dict):
                self.half_ci = half_ci
            if not is_deff_dict and isinstance(deff, (int, float)) and stratum is not None:
                self.deff_c = dict(zip(stratum, np.repeat(deff, number_strata)))
            elif isinstance(deff, dict):
                self.deff_c = deff
            if (
                not is_resp_rate_dict
                and isinstance(resp_rate, (int, float))
                and stratum is not None
            ):
                self.resp_rate = dict(zip(stratum, np.repeat(resp_rate, number_strata)))
            elif isinstance(resp_rate, dict):
                self.resp_rate = resp_rate
            if (
                not isinstance(pop_size, dict)
                and isinstance(pop_size, (int, float))
                and stratum is not None
            ):
                self.resp_rate = dict(zip(stratum, np.repeat(pop_size, number_strata)))
            elif isinstance(pop_size, dict):
                self.resp_rate = pop_size

        target_values: Union[np.ndarray, Number]
        half_ci_values: Union[np.ndarray, Number]
        resp_rate_values: Union[np.ndarray, Number]
        pop_size_values: Union[np.ndarray, Number]
        if (
            isinstance(self.target, dict)
            and isinstance(self.half_ci, dict)
            and isinstance(self.resp_rate, dict)
        ):
            target_values = np.array(list(self.target.values()))
            half_ci_values = np.array(list(self.half_ci.values()))
            resp_rate_values = np.array(list(self.resp_rate.values()))
            if isinstance(self.pop_size, dict):
                pop_size_values = np.array(list(self.pop_size.values()))
        elif (
            isinstance(self.target, (int, float))
            and isinstance(self.half_ci, (int, float))
            and isinstance(self.resp_rate, (int, float))
        ):
            target_values = self.target
            half_ci_values = self.half_ci
            resp_rate_values = self.resp_rate
            if isinstance(self.pop_size, (int, float)):
                pop_size_values = self.pop_size
        else:
            raise TypeError("Wrong type for self.target, self.half_ci, or self.resp_rate")

        if self.parameter == "proportion" and (
            np.asarray(0 > target_values).any()
            or np.asarray(target_values > 1).any()
            or np.asarray(0 > half_ci_values).any()
            or np.asarray(half_ci_values > 1).all()
        ):
            raise ValueError("Proportion values must be between 0 and 1.")

        self.alpha = alpha

        samp_size: Union[DictStrNum, Number]
        if self.method == "wald":
            samp_size = self._calculate_wald(
                target=self.target,
                half_ci=self.half_ci,
                pop_size=self.pop_size,
                stratum=stratum,
            )
        elif self.method == "fleiss":
            samp_size = self._calculate_fleiss(
                target=self.target,
                half_ci=self.half_ci,
                # pop_size=self.pop_size,
                stratum=stratum,
            )

        if np.asarray(0 < resp_rate_values).all() and np.asarray(resp_rate_values <= 1).all():
            if isinstance(samp_size, dict) and isinstance(self.resp_rate, dict):
                for s in samp_size:
                    samp_size[s] = math.ceil(samp_size[s] / self.resp_rate[s])
            elif isinstance(samp_size, (int, float)) and isinstance(self.resp_rate, (int, float)):
                samp_size = math.ceil(samp_size / self.resp_rate)

        else:
            raise ValueError("Response rates must be between 0 and 1 (proportion).")

        self.samp_size = samp_size

    def to_dataframe(self, col_names: Optional[list[str]] = None) -> pd.DataFrame:
        """Coverts the dictionaries to a pandas dataframe

        Args:
            col_names (list[str], optional): column names for the dataframe. Defaults to
                ["_stratum", "_target", "_half_ci", "_samp_size"].

        Raises:
            AssertionError: when sample size is not calculated.

        Returns:
            pd.DataFrame: output pandas dataframe.
        """

        if self.samp_size is None:
            raise AssertionError("No sample size calculated.")
        elif col_names is None:
            col_names = ["_parameter", "_stratum", "_target", "_half_ci", "_samp_size"]
            if not self.stratification:
                col_names.pop(1)
        else:
            ncols = len(col_names)
            if (ncols != 5 and self.stratification) or (ncols != 4 and not self.stratification):
                raise AssertionError("col_names must have 5 values")
        if self.stratification:
            est_df = dict_to_dataframe(
                col_names,
                self.target,
                self.half_ci,
                self.samp_size,
            )
        else:
            est_df = dict_to_dataframe(
                col_names,
                self.target,
                self.half_ci,
                self.samp_size,
            )
        est_df.iloc[:, 0] = self.parameter

        return est_df


def allocate(
    method: str,
    stratum: Array,
    pop_size: DictStrNum,
    samp_size: Optional[Number] = None,
    constant: Optional[Number] = None,
    rate: Optional[Union[DictStrNum, Number]] = None,
    stddev: Optional[DictStrNum] = None,
) -> tuple[DictStrNum, DictStrNum]:
    """Reference: Kish(1965), page 97"""

    stratum = list(numpy_array(stratum))

    if method.lower() == "equal":
        if isinstance(constant, (int, float)):
            sample_sizes = dict(zip(stratum, np.repeat(constant, len(stratum))))
        else:
            raise ValueError("Parameter 'target_size' must be a valid integer!")
    elif method.lower() == "proportional":
        if isinstance(pop_size, dict) and stddev is None and samp_size is not None:
            total_pop = sum(list(pop_size.values()))
            samp_size_h = [math.ceil((samp_size / total_pop) * pop_size[k]) for k in stratum]
            sample_sizes = dict(zip(stratum, samp_size_h))
        elif isinstance(pop_size, dict) and stddev is not None and samp_size is not None:
            total_pop = sum(list(pop_size.values()))
            samp_size_h = [
                math.ceil((samp_size / total_pop) * pop_size[k] * stddev[k]) for k in stratum
            ]
            sample_sizes = dict(zip(stratum, samp_size_h))
        else:
            raise ValueError(
                "Parameter 'pop_size' must be a dictionary and 'samp_size' an integer!"
            )
    elif method.lower() == "fixed_rate":
        if isinstance(rate, (int, float)) and pop_size is not None:
            samp_size_h = [math.ceil(rate * pop_size[k]) for k in stratum]
        else:
            raise ValueError(
                "Parameter 'pop_size' and 'rate' must be a dictionary and number respectively!"
            )
        sample_sizes = dict(zip(stratum, samp_size_h))
    elif method.lower() == "proportional_rate":
        if isinstance(rate, (int, float)) and pop_size is not None:
            samp_size_h = [math.ceil(rate * pop_size[k] * pop_size[k]) for k in stratum]
        else:
            raise ValueError("Parameter 'pop_size' must be a dictionary!")
        sample_sizes = dict(zip(stratum, samp_size_h))
    elif method.lower() == "equal_errors":
        if isinstance(constant, (int, float)) and stddev is not None:
            samp_size_h = [math.ceil(constant * stddev[k] * stddev[k]) for k in stratum]
        else:
            raise ValueError(
                "Parameter 'stddev' and 'constant' must be a dictionary and number, respectively!"
            )
        sample_sizes = dict(zip(stratum, samp_size_h))
    elif method.lower() == "optimum_mean":
        if isinstance(rate, (int, float)) and pop_size is not None and stddev is not None:
            samp_size_h = [math.ceil(rate * pop_size[k] * stddev[k]) for k in stratum]
        else:
            raise ValueError(
                "Parameter 'pop_size' and 'rate' must be a dictionary and number respectively!"
            )
        sample_sizes = dict(zip(stratum, samp_size_h))
    elif method.lower() == "optimum_comparison":
        if isinstance(rate, (int, float)) and stddev is not None:
            samp_size_h = [math.ceil(rate * stddev[k]) for k in stratum]
        else:
            raise ValueError(
                "Parameter 'stddev' and 'rate' must be a dictionary and number respectively!"
            )
        sample_sizes = dict(zip(stratum, samp_size_h))
    elif method.lower() == "variable_rate" and isinstance(rate, dict) and pop_size is not None:
        samp_size_h = [math.ceil(rate[k] * pop_size[k]) for k in stratum]
        sample_sizes = dict(zip(stratum, samp_size_h))
    else:
        raise ValueError(
            "Parameter 'method' is not valid. Options are 'equal', 'proportional', 'fixed_rate', 'proportional_rate', 'equal_errors', 'optimun_mean', and 'optimun_comparison'!"
        )

    if (list(sample_sizes.values()) > np.asarray(list(pop_size.values()))).any():
        raise ValueError(
            "Some of the constants, rates, or standard errors are too large, resulting in sample sizes larger than population sizes!"
        )

    sample_rates = {}
    if isinstance(pop_size, dict):
        for k in pop_size:
            sample_rates[k] = sample_sizes[k] / pop_size[k]

    return sample_sizes, sample_rates


def calculate_clusters() -> None:
    pass


class OneMeanSampleSize:
    """*OneMeanSample* implements sample size calculation methods for a mean for one single population."""

    def __init__(
        self, stratification: bool = False, two_side: bool = True, estimated_mean: bool = True
    ) -> None:

        self.stratification = stratification
        self.test_type = "two-side" if two_side else "one-side"
        self.estimated_mean = estimated_mean

        self.alpha = Number
        self.beta = Number
        self.samp_size: Union[DictStrNum, Number] = 0
        self.power: Union[DictStrNum, Number] = 0
        self.targeted_mean: Union[DictStrNum, Number]
        self.reference_mean: Union[DictStrNum, Number]
        self.stddev: Union[DictStrNum, Number]
        self.deff_c: Union[DictStrNum, Number] = 1.0
        self.deff_w: Union[DictStrNum, Number] = 1.0
        self.resp_rate: Union[DictStrNum, Number] = 1.0
        self.pop_size: Optional[Union[DictStrNum, Number]] = None

    def calculate(
        self,
        targeted_mean: Union[DictStrNum, Number],
        reference_mean: Union[DictStrNum, Number],
        stddev: Union[DictStrNum, Number],
        deff: Union[DictStrNum, Number, Number] = 1.0,
        resp_rate: Union[DictStrNum, Number] = 1.0,
        number_strata: Optional[int] = None,
        pop_size: Optional[Union[DictStrNum, Number]] = None,
        alpha: float = 0.05,
        beta: float = 0.20,
    ) -> None:

        is_targeted_mean_dict = isinstance(targeted_mean, dict)
        is_reference_mean_dict = isinstance(reference_mean, dict)
        is_stddev_dict = isinstance(stddev, dict)
        is_deff_dict = isinstance(deff, dict)
        is_resp_rate_dict = isinstance(resp_rate, dict)
        is_pop_size_dict = isinstance(pop_size, dict)

        number_dictionaries = (
            is_targeted_mean_dict
            + is_reference_mean_dict
            + is_stddev_dict
            + is_deff_dict
            + is_resp_rate_dict
            + is_pop_size_dict
        )

        if (
            self.stratification
            and (number_strata is None or number_strata <= 0)
            and number_dictionaries == 0
        ):
            raise AssertionError("Stratified designs ")

        if not self.stratification and number_dictionaries >= 1:
            raise ValueError("Dictionaries must NOT be provided for non stratified designs!")

        number_strata = 1 if not self.stratification else number_strata

        [mean1, mean0, std_dev] = convert_numbers_to_dicts(
            number_strata, targeted_mean, reference_mean, stddev
        )

        self.alpha = alpha
        self.beta = beta

        prob_alpha = (
            normal.ppf(1 - self.alpha / 2)
            if self.test_type == "two-side"
            else normal.ppf(1 - self.alpha)
        )
        prob_beta = normal.ppf(1 - self.beta)
        if self.stratification:
            self.samp_size = {}
            self.power = {}
            for key in mean1:
                self.samp_size[key] = math.ceil(
                    pow(
                        (prob_alpha + prob_beta) * std_dev[key] / (mean1[key] - mean0[key]),
                        2,
                    )
                )

                if self.estimated_mean:
                    t_prob_alpha = (
                        student.ppf(1 - self.alpha / 2, self.samp_size[key] - 1)
                        if self.test_type == "two-side"
                        else student.ppf(1 - self.alpha, self.samp_size[key] - 1)
                    )
                    t_prob_beta = student.ppf(1 - self.beta, self.samp_size[key] - 1)
                    self.samp_size[key] = math.ceil(
                        pow(
                            (t_prob_alpha + t_prob_beta)
                            * std_dev[key]
                            / (mean1[key] - mean0[key]),
                            2,
                        )
                    )

                adj_fct = (mean0[key] - mean1[key]) / (
                    std_dev[key] / math.sqrt(self.samp_size[key])
                )
                self.power[key] = (
                    1 - normal.cdf(prob_alpha + adj_fct) + normal.cdf(-prob_alpha + adj_fct)
                )
        else:
            self.samp_size = math.ceil(
                pow(
                    (prob_alpha + prob_beta)
                    * std_dev["_stratum_1"]
                    / (mean1["_stratum_1"] - mean0["_stratum_1"]),
                    2,
                )
            )

            adj_fct = (mean0["_stratum_1"] - mean1["_stratum_1"]) / (
                std_dev["_stratum_1"] / math.sqrt(self.samp_size)
            )
            self.power = 1 - normal.cdf(prob_alpha + adj_fct) + normal.cdf(-prob_alpha + adj_fct)

            if self.estimated_mean:
                t_prob_alpha0 = (
                    student.ppf(1 - self.alpha / 2, self.samp_size - 1)
                    if self.test_type == "two-side"
                    else student.ppf(1 - self.alpha, self.samp_size - 1)
                )
                t_prob_beta0 = student.ppf(1 - self.beta, self.samp_size - 1)
                self.samp_size = math.ceil(
                    pow(
                        (t_prob_alpha0 + t_prob_beta0)
                        * std_dev["_stratum_1"]
                        / (mean1["_stratum_1"] - mean0["_stratum_1"]),
                        2,
                    )
                )
                t_prob_alpha1 = (
                    student.ppf(1 - self.alpha / 2, self.samp_size - 1)
                    if self.test_type == "two-side"
                    else student.ppf(1 - self.alpha, self.samp_size - 1)
                )

                t_adj_fct = (mean0["_stratum_1"] - mean1["_stratum_1"]) / (
                    std_dev["_stratum_1"] / math.sqrt(self.samp_size)
                )
                self.power = (
                    1
                    - nct.cdf(t_prob_alpha1, self.samp_size - 1, -t_adj_fct)
                    # + student.cdf(-t_prob_alpha1 + t_adj_fct)
                )


class TwoMeanSampleSize:
    pass
