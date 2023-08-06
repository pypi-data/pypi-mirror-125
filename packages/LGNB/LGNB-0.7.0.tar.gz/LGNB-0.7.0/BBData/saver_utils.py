#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   saver_utils.py    
@Contact :   wangcc@csc.com.cn
@License :   (C)Copyright 2017-2018, CSC

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/10/15 10:24   wangcc     1.0         None
'''


import json
import h5py
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from .config import data_path, cal_config
from .reader_utils import Cal, Inst
import os


class FeatureUpdater:

    def __init__(self, stk_univ="all", start_time=None, end_time=None, freq="Tday", is_alpha=False):
        start_time = cal_config[freq]["si"] if start_time is None else start_time
        end_time = cal_config[freq]["ei"] if end_time is None else end_time
        _, calendar_index = Cal._get_calendar(freq=freq)
        self.stk_univ = sorted(list(Inst.list_instruments(stk_univ, start_time, end_time).keys()))
        self.time_idx = Cal.calendar(start_time, end_time, freq=freq)
        self.cal_serr = pd.Series(calendar_index)
        self.multiidx = pd.MultiIndex.from_product([self.stk_univ, self.time_idx])
        self.freq = freq
        self.is_alpha = is_alpha

    @property
    def _uri_data(self):
        """Static feature file uri."""
        return os.path.join(data_path, "features", "{}", "{}.h5")

    @property
    def _uri_cfg(self):
        """Static feature file uri."""
        return os.path.join(data_path, "features", "{}", "{}_config.json")

    def _get_uri(self, freq, field):
        main_path = os.path.join(data_path, "features", f"{freq}")
        if not os.path.exists(main_path):
            os.mkdir(main_path)
        return self._uri_data.format(self.freq, field)

    def save_series(self, field: str, values: Series, config: dict):
        flname = self._get_uri(self.freq, field)
        with h5py.File(flname, "w") as h5:
            h5.create_dataset("data", data=values.values)
            if config:
                with open(self._uri_cfg.format(self.freq, field), "w") as f:
                    json.dump(config, f)

    def save_config(self, field, values: Series, uniq: np.ndarray, starts: np.ndarray,
                    rfstarts: np.ndarray, rfends: np.ndarray):
        assert cal_config[self.freq]["col_name"] == field
        if self.is_alpha:  # 存alpha的情况下不更新轴
            return
        flname = self._get_uri(self.freq, field)
        with h5py.File(flname, "w") as h5:
            h5.create_dataset("data", data=values.values)
            h5.create_dataset("instlist", data=uniq)
            h5.create_dataset("instloc", data=starts)
            h5.create_dataset("rsilist", data=rfstarts)
            h5.create_dataset("reilist", data=rfends)

    def save_values(self, Mdf: DataFrame, dtname: str, partition_by: str, config: dict= None):
        Mdf, insts, *locates = self._locate_partition(Mdf, self.cal_serr, dtname, partition_by)
        if isinstance(insts[0], (np.str_, str)):
            insts = insts.astype(np.dtype("|S12"))
        if config is None:
            config = {}
        value_dict = Mdf.to_dict("series")
        timeindex = value_dict.pop(dtname)
        self.save_config(dtname, timeindex, insts, *locates)
        for field, values in value_dict.items():
            config_i = config.get(field, None)
            self.save_series(field, values, config_i)

    def _locate_partition(self, Mdf: DataFrame, cal_serr, dtname: str, partition_by: str):
        """
        partition Mdf according to instruments
        :param Mdf:
        :param cal_serr:
        :param dtname:
        :param partition_by:
        :return:
        """
        order_by = [partition_by, dtname]
        self.multiidx.names = order_by
        Mdf = Mdf.set_index(order_by).reindex(self.multiidx).reset_index()  # 要改
        uniq, starts = np.unique(Mdf.loc[:, partition_by], return_index=True)
        tlst = Mdf.loc[:, dtname]
        rfstarts = cal_serr.loc[tlst[starts]].values  # location on time index
        ends = np.roll(starts, -1)
        ends[-1] = Mdf.shape[0]
        rfends = cal_serr.loc[tlst[ends - 1]].values  # location on time index
        return Mdf.set_index(partition_by), uniq, starts, rfstarts, rfends


def FeatureSaver(freq):
    return FeatureUpdater(freq=freq, is_alpha=True)
